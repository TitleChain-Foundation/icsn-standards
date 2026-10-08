#!/usr/bin/env bash
# Run the WHOLE benchmark suite inside a real Intel TDX trust domain, and again
# on an identical non-confidential instance, so every headline number in the
# paper has a hardware measurement behind it rather than a laptop one.
#
# This is the companion to run_on_gcp.sh, which measures attestation: the quote,
# the key binding, and the trust-domain overhead on one pipeline step. That
# script answers "what does the hardware cost". This one answers "what do the
# numbers we publish become when the hardware is really there".
#
#   ./impl/tdx/run_suite_on_gcp.sh [PROJECT] [ZONE]
#
# Requires gcloud, authenticated, with billing enabled. Creates two VMs and
# DELETES THEM at the end, including on failure. Cost is a few tens of cents.
#
# Why a control, and why it is not optional. The published numbers were measured
# on an Apple M2 Max. Running them on a c3-standard-4 changes the machine AND
# adds a trust domain, and a single number cannot separate those. The control is
# the same instance shape with TDX off, so each benchmark yields a pair and the
# trust-domain cost is isolated from the platform change.
#
# Results land in impl/results/suite/{td,control}/ and are not merged into
# impl/results/, because those are the laptop numbers the paper currently cites
# and overwriting them would silently restate published figures.

set -euo pipefail
PROJECT="${1:-$(gcloud config get-value project 2>/dev/null)}"
ZONE="${2:-us-central1-a}"
TD=poc-suite-tdx-$$
CTL=poc-suite-control-$$
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="$ROOT/impl/results/suite"

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
# Everything the suite actually imports, not just what the pipeline needs.
# bench_pq needs dilithium-py; bench_ops reaches schema/cbor_profile.py, which
# needs cbor2 and pulls in validate.py, which needs jsonschema. Miss any of
# them and a benchmark either dies or -- worse, as cbor2 did -- silently
# produces None where a byte count should be.
~/venv/bin/pip install -q cryptography dilithium-py cbor2 jsonschema >/dev/null 2>&1'

for host in "$TD" "$CTL"; do
  echo "==> provisioning $host"
  for i in 1 2 3 4 5; do
    if gcloud compute scp "$TAR" "$host:~/poc-impl.tgz" --zone="$ZONE" \
         --project="$PROJECT" --quiet >/dev/null 2>&1; then break; fi
    sleep 15
  done
  gcloud compute ssh "$host" --zone="$ZONE" --project="$PROJECT" --quiet \
    --command="$SETUP"
done

# The five benchmarks behind the paper's tables. bench_tdx.py is deliberately
# absent: it is run_on_gcp.sh's job and it cannot run on the control at all.
#
# ORDER IS LOAD-BEARING. bench_ops.py reads results/bench_pq.json, and that file
# ships inside the tarball carrying the laptop's numbers. Run bench_ops first and
# it silently folds an Apple M2 Max measurement into a table labelled as this
# machine's -- a mixed-provenance result that looks entirely normal. bench_pq
# runs first so bench_ops reads numbers from the host it is running on.
#
# The stale copy is deleted before the run for the same reason: if bench_pq
# fails, bench_ops must fail too rather than quietly falling back to the
# shipped file.
SUITE='set -e
cd ~/impl
# Every shipped result is a laptop measurement. Delete them all before running,
# so a file that exists afterwards was necessarily produced on this host. The
# first attempt at this script fetched ops.json for both instances after
# bench_ops had failed on both -- byte-identical to the shipped file, and it
# would have been read as a hardware measurement.
rm -f results/bench.json results/ops.json results/frontier.json \
      results/merkle.json results/bench_pq.json
for b in bench_pq bench bench_ops bench_frontier bench_merkle; do
  echo "--- $b"
  ~/venv/bin/python3 "bench/$b.py" >/dev/null 2>/tmp/$b.err \
    || { echo "    FAILED: $b"; tail -3 /tmp/$b.err | sed "s/^/      /"; }
done
~/venv/bin/python3 - <<PY
import json, platform, subprocess
def cpu():
    try:
        for line in open("/proc/cpuinfo"):
            if line.startswith("model name"):
                return line.split(":",1)[1].strip()
    except Exception:
        pass
    return "unknown"
def tdx():
    try:
        d = subprocess.run(["sudo","dmesg"], capture_output=True, text=True).stdout
        return "tdx: Guest detected" in d
    except Exception:
        return False
print(json.dumps({"cpu": cpu(), "kernel": platform.release(),
                  "python": platform.python_version(),
                  "tdx_guest_detected": tdx()}, indent=1))
PY'

for host in "$TD" "$CTL"; do
  echo
  echo "==> running the suite on $host"
  gcloud compute ssh "$host" --zone="$ZONE" --project="$PROJECT" --quiet \
    --command="sudo mount -t configfs none /sys/kernel/config 2>/dev/null || true; $SUITE"
done

echo
echo "==> fetching results"
mkdir -p "$OUT/td" "$OUT/control"
for pair in "$TD:td" "$CTL:control"; do
  host="${pair%%:*}"; dir="${pair##*:}"
  for f in bench ops frontier merkle bench_pq; do
    gcloud compute scp "$host:~/impl/results/$f.json" "$OUT/$dir/$f.json" \
      --zone="$ZONE" --project="$PROJECT" --quiet 2>/dev/null || true
  done
done
rm -f "$TAR"
echo "==> done; results in impl/results/suite/"
