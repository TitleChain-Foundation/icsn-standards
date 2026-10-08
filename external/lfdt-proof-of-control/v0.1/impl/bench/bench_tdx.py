#!/usr/bin/env python3
"""E6: the pipeline on real Intel TDX hardware.

Every latency in this paper so far excluded the cost of a hardware trust
boundary, because there was no hardware. This runs inside a TDX trust domain on
GCP and measures what that omission was worth, and -- more importantly --
establishes the binding the software stand-in could only assert.

  T1  Is this really a TD? Report what the hardware says about itself.
  T2  Bind the evidence signing key into a hardware quote and verify the
      binding holds. This is the claim the whole standard rests on.
  T3  What a quote costs to produce.
  T4  End-to-end per-step latency on this machine, with and without a fresh
      quote per action, against the same pipeline measured on a laptop.
  T5  Enumerate the trust chain: exactly whose signatures a verifier must
      accept. The tier definitions in the specification depend on this being
      an honest list rather than a slogan.

Run ON the confidential VM:
    python3 bench/bench_tdx.py
"""
from __future__ import annotations

import json
import platform
import statistics as st
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from poc import (Action, AttestingEnvironment, EvidenceStore, Gateway, Grant,
                 PolicyEngine, canonical, sha256)
from poc import tdx


def host_facts() -> dict:
    def sh(cmd):
        try:
            return subprocess.run(cmd, shell=True, capture_output=True,
                                  text=True, timeout=20).stdout.strip()
        except Exception:
            return ""
    return {
        "kernel": platform.release(),
        "cpu_model": sh("grep -m1 'model name' /proc/cpuinfo | cut -d: -f2-").strip(),
        "tdx_guest_device": Path("/dev/tdx_guest").exists(),
        "dmesg_tdx": [l for l in sh("dmesg 2>/dev/null | grep -i tdx").splitlines()][:6],
        "machine_type": sh("curl -s -H 'Metadata-Flavor: Google' "
                           "metadata.google.internal/computeMetadata/v1/instance/machine-type"
                           ).split("/")[-1],
        "confidential": sh("curl -s -H 'Metadata-Flavor: Google' "
                           "metadata.google.internal/computeMetadata/v1/instance/"
                           "confidential-instance-type") or "(unset)",
    }


def stack():
    g = Grant("user:alice", frozenset({"db.read", "http.post"}),
              frozenset({"customers", "api.partner.com"}),
              max_spend=1e9, max_sensitivity_egress="restricted")
    ae = AttestingEnvironment(PolicyEngine(g))
    store = EvidenceStore()
    return ae, store, Gateway(ae, store)


def main():
    out = {}

    # ---------------------------------------------------------------- T1
    print("T1  what the hardware says about itself\n")
    facts = host_facts()
    out["host"] = facts
    for k in ("kernel", "cpu_model", "machine_type", "confidential",
              "tdx_guest_device"):
        print(f"    {k:<20} {facts[k]}")
    for line in facts["dmesg_tdx"]:
        print(f"    dmesg              {line.strip()[:88]}")
    if not tdx.available():
        print("\n    NOT a TDX guest -- nothing below is meaningful. Stopping.")
        return 1

    # ---------------------------------------------------------------- T2
    print("\nT2  binding the evidence key into a hardware quote\n")
    ae, store, gw = stack()
    pk_bytes = ae.pk.public_bytes_raw()
    q = tdx.attest_key(pk_bytes)
    s = q.summary()
    out["quote"] = s
    print(f"    provider            {s['provider']}")
    print(f"    quote size          {s['quote_bytes']:,} bytes")
    print(f"    MRTD                {s['mrtd'][:64]}")
    print(f"                        {s['mrtd'][64:]}")
    print(f"    RTMR[0]             {s['rtmr'][0][:48]}...")
    print(f"    TD attributes       {s['tdattributes']}   XFAM {s['xfam']}")
    print(f"    REPORTDATA          {s['reportdata'][:64]}")
    print(f"    binds our key?      {q.binds_key(pk_bytes)}")

    # the check that gives the binding its teeth: a quote for a DIFFERENT key
    # must not validate against ours
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    other = Ed25519PrivateKey.generate().public_key().public_bytes_raw()
    print(f"    binds another key?  {q.binds_key(other)}  <- must be False")
    out["binding_sound"] = bool(q.binds_key(pk_bytes) and not q.binds_key(other))

    # ---------------------------------------------------------------- T3
    print("\nT3  what a quote costs\n")
    cost = tdx.measure_quote_cost(pk_bytes, n=20)
    out["quote_cost"] = cost
    print(f"    mean {cost['mean_us']:,.0f} us   median {cost['median_us']:,.0f} us"
          f"   p95 {cost['p95_us']:,.0f} us   max {cost['max_us']:,.0f} us")
    print(f"    ({cost['median_us']/1000:.1f} ms per quote -- this is the number"
          f" every earlier latency table omitted)")

    # ---------------------------------------------------------------- T4
    print("\nT4  per-step latency inside the TD\n")
    a = Action("db.read", "customers", {"row": 1}, classification="confidential")
    for _ in range(200):
        gw.submit(a)
    N = 3000
    t0 = time.perf_counter_ns()
    for _ in range(N):
        gw.submit(a)
    per_step = (time.perf_counter_ns() - t0) / 1000 / N

    samples = []
    for _ in range(N):
        t1 = time.perf_counter_ns()
        gw.submit(a)
        samples.append((time.perf_counter_ns() - t1) / 1000)
    samples.sort()
    step = {"mean_us": round(per_step, 2),
            "median_us": round(samples[len(samples)//2], 2),
            "p95_us": round(samples[int(N*0.95)], 2),
            "p99_us": round(samples[int(N*0.99)], 2),
            "throughput_per_s": round(1e6/per_step)}
    out["step_in_td"] = step
    print(f"    software pipeline   mean {step['mean_us']:.2f} us"
          f"   p95 {step['p95_us']:.2f}   p99 {step['p99_us']:.2f}")
    print(f"    throughput          {step['throughput_per_s']:,} steps/s (1 core)")

    # a fresh quote per action is the pessimistic deployment
    per_action_quote = step["mean_us"] + cost["median_us"]
    out["step_with_fresh_quote_us"] = round(per_action_quote, 1)
    out["quote_share"] = round(cost["median_us"] / per_action_quote, 4)
    print(f"    + fresh quote/action {per_action_quote:,.0f} us"
          f"  ({out['quote_share']:.1%} of the step is attestation)")
    print(f"    15 ms budget        {'MET' if per_action_quote < 15000 else 'BLOWN'}"
          f" at {per_action_quote/15000:.1%} of budget")

    # amortized: one quote per session, which is what the design actually does
    for n in (1, 10, 100, 1000):
        amort = step["mean_us"] + cost["median_us"] / n
        print(f"    quote per {n:>5} steps  {amort:>9,.1f} us/step")
    out["amortized_us"] = {str(n): round(step["mean_us"] + cost["median_us"]/n, 2)
                           for n in (1, 10, 100, 1000)}

    # ---------------------------------------------------------------- T5
    print("\nT5  who a verifier must still trust\n")
    chain = [
        ("Intel", "the TDX module and CPU behave as specified, and the "
                  "Provisioning Certification Key is not misissued"),
        ("Intel PCS / DCAP collateral", "the certificate chain and TCB info "
                                        "fetched to check the quote are authentic"),
        ("the Quoting Enclave", "signs TD reports honestly"),
        ("Google", "the host does not exfiltrate TD memory through a channel "
                   "outside the TDX threat model, and supplies the vTPM/firmware "
                   "measured into RTMRs"),
        ("whoever publishes reference values", "the MRTD you compare against "
                                               "is the MRTD of the code you think it is"),
    ]
    out["trust_chain"] = [{"party": p, "assumption": a} for p, a in chain]
    for p, a in chain:
        print(f"    {p:<32} {a}")
    print("\n    Anchoring the evidence log removes none of these. It makes the")
    print("    HISTORY publicly auditable; the MEASUREMENT is still established")
    print("    by the chain above. Tier definitions should say so.")

    p = Path(__file__).resolve().parent.parent / "results" / "tdx.json"
    p.write_text(json.dumps(out, indent=2) + "\n")
    print(f"\nwritten to {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
