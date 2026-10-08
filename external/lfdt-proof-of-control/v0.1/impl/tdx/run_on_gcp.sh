#!/usr/bin/env bash
# Run the evidence pipeline inside a real Intel TDX trust domain, and measure
# what the hardware costs.
#
# Everything else in impl/ models the enclave as an in-process object. This
# script is the version with actual hardware underneath it: a GCP C3 instance
# with --confidential-compute-type=TDX, plus an identical non-confidential
# instance as the control, so the trust-domain overhead is isolated rather than
# confounded with a change of CPU.
#
#   ./impl/tdx/run_on_gcp.sh [PROJECT] [ZONE]
#
# Requires gcloud, authenticated, with billing enabled. Creates two VMs and
# DELETES THEM at the end, including on failure. Cost is a few tens of cents.
#
# What it establishes:
#   * that /dev/tdx_guest is present and the CPU reports Intel TDX
#   * a real DCAP quote, with the evidence public key digest in REPORTDATA,
#     so the hardware signature covers the measurement AND the key
#   * the cost of producing a quote, which every other latency table here omits
#   * trust-domain overhead on the software pipeline, TDX on vs off, same shape

set -euo pipefail
PROJECT="${1:-$(gcloud config get-value project 2>/dev/null)}"
ZONE="${2:-us-central1-a}"
TD=poc-tdx-$$
CTL=poc-tdx-control-$$
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

cleanup() {
  echo
  echo "==> deleting instances"
  gcloud compute instances delete "$TD" "$CTL" --zone="$ZONE" --quiet \
    --project="$PROJECT" 2>/dev/null || true
}
trap cleanup EXIT

echo "==> packaging implementation"
TAR=$(mktemp -t poc-impl-XXXX).tgz
tar czf "$TAR" -C "$ROOT" impl schema

echo "==> creating TDX instance $TD"
gcloud compute instances create "$TD" --project="$PROJECT" --zone="$ZONE" \
  --machine-type=c3-standard-4 --confidential-compute-type=TDX \
  --maintenance-policy=TERMINATE \
  --image-family=ubuntu-2404-lts-amd64 --image-project=ubuntu-os-cloud \
  --boot-disk-size=50GB --quiet >/dev/null

echo "==> creating control instance $CTL (same shape, TDX off)"
gcloud compute instances create "$CTL" --project="$PROJECT" --zone="$ZONE" \
  --machine-type=c3-standard-4 \
  --image-family=ubuntu-2404-lts-amd64 --image-project=ubuntu-os-cloud \
  --boot-disk-size=50GB --quiet >/dev/null

SETUP='tar xzf poc-impl.tgz
sudo apt-get update -qq >/dev/null 2>&1
sudo apt-get install -y -qq python3-venv >/dev/null 2>&1
python3 -m venv ~/venv >/dev/null 2>&1
~/venv/bin/pip install -q cryptography >/dev/null 2>&1'

for host in "$TD" "$CTL"; do
  echo "==> provisioning $host"
  # SSH keys can take a moment to propagate on a fresh instance
  for i in 1 2 3 4 5; do
    if gcloud compute scp "$TAR" "$host:~/poc-impl.tgz" --zone="$ZONE" \
         --project="$PROJECT" --quiet >/dev/null 2>&1; then break; fi
    sleep 15
  done
  gcloud compute ssh "$host" --zone="$ZONE" --project="$PROJECT" --quiet \
    --command="$SETUP"
done

echo
echo "==> TDX instance: attestation and latency"
gcloud compute ssh "$TD" --zone="$ZONE" --project="$PROJECT" --quiet --command='
  sudo mount -t configfs none /sys/kernel/config 2>/dev/null || true
  cd ~/impl && sudo ~/venv/bin/python3 bench/bench_tdx.py'

echo
echo "==> control instance: same pipeline, TDX off"
gcloud compute ssh "$CTL" --zone="$ZONE" --project="$PROJECT" --quiet --command='
  cd ~/impl && ~/venv/bin/python3 bench/bench_tdx.py --control-only 2>/dev/null \
  || ~/venv/bin/python3 - <<PY
import sys, time, json; sys.path.insert(0, ".")
from poc import *
g = Grant("user:alice", frozenset({"db.read","http.post"}),
          frozenset({"customers","api.partner.com"}),
          max_spend=1e9, max_sensitivity_egress="restricted")
gw = Gateway(AttestingEnvironment(PolicyEngine(g)), EvidenceStore())
a = Action("db.read", "customers", {"row": 1}, classification="confidential")
for _ in range(200): gw.submit(a)
N = 3000
t0 = time.perf_counter_ns()
for _ in range(N): gw.submit(a)
mean = (time.perf_counter_ns() - t0) / 1000 / N
print(json.dumps({"control_mean_us": round(mean, 2),
                  "throughput_per_s": round(1e6/mean)}, indent=1))
PY'

echo
echo "==> fetching results"
gcloud compute scp "$TD:~/impl/results/tdx.json" "$ROOT/impl/results/tdx.json" \
  --zone="$ZONE" --project="$PROJECT" --quiet || true
rm -f "$TAR"
echo "==> done; results in impl/results/tdx.json"
