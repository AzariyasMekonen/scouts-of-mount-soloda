#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

TEST_FLAG="AdwaCTF{DYNAMIC_SCOUT_TEST_$(date +%s)}"
OUT_DIR="$(pwd)/test_output"

echo "============================================================"
echo " [1/3] Direct Python Dynamic File Generation Test"
echo "============================================================"
rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

FLAG="$TEST_FLAG" USER_ID="team_lion_42" OUTPUT_DIR="$OUT_DIR" OUTPUT_FILENAME="recon_dispatch.txt" python3 src/generate.py

echo "[+] Verifying generated file..."
if [ -f "solve/solve.py" ]; then
    RECOVERED=$(python3 solve/solve.py "$OUT_DIR/recon_dispatch.txt" | tail -n 1)
    if [[ "$RECOVERED" =~ "$TEST_FLAG" ]]; then
        echo "SUCCESS: Python dynamic generator verified: $TEST_FLAG"
    else
        echo "FAIL: Expected $TEST_FLAG but got $RECOVERED" >&2
        exit 1
    fi
else
    if [ -s "$OUT_DIR/recon_dispatch.txt" ]; then
        echo "SUCCESS: Python dynamic generator created non-empty recon_dispatch.txt"
    else
        echo "FAIL: $OUT_DIR/recon_dispatch.txt is missing or empty" >&2
        exit 1
    fi
fi

echo
echo "============================================================"
echo " [2/3] Container Engine Verification (Podman / Docker)"
echo "============================================================"
if command -v podman >/dev/null 2>&1; then
    CONTAINER_CLI="podman"
elif command -v docker >/dev/null 2>&1; then
    CONTAINER_CLI="docker"
else
    echo "Notice: Neither podman nor docker found, skipping container test."
    rm -rf "$OUT_DIR"
    exit 0
fi

IMAGE_NAME="adwactf/scouts-of-mount-soloda-generator:latest"
CONTAINER_TEST_FLAG="AdwaCTF{CONTAINER_DYNAMIC_FLAG_PASSED_1896}"

echo "[+] Building container with $CONTAINER_CLI..."
$CONTAINER_CLI build -t "$IMAGE_NAME" .

echo "[+] Running container with dynamic FLAG=$CONTAINER_TEST_FLAG..."
rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"
chmod 777 "$OUT_DIR"

$CONTAINER_CLI run --rm \
  -e FLAG="$CONTAINER_TEST_FLAG" \
  -e USER_ID="participant_test_soloda" \
  -v "$OUT_DIR:/output:Z" \
  "$IMAGE_NAME"

echo
echo "============================================================"
echo " [3/3] Verifying Container Output File"
echo "============================================================"
if [ ! -f "$OUT_DIR/recon_dispatch.txt" ]; then
    echo "Error: /output/recon_dispatch.txt was not generated!" >&2
    exit 1
fi

if [ -f "solve/solve.py" ]; then
    RECOVERED_CONTAINER=$(python3 solve/solve.py "$OUT_DIR/recon_dispatch.txt" | tail -n 1)
    if [[ "$RECOVERED_CONTAINER" =~ "$CONTAINER_TEST_FLAG" ]]; then
        echo "SUCCESS: Container generated file verified! Flag: $CONTAINER_TEST_FLAG"
        rm -rf "$OUT_DIR"
        exit 0
    else
        echo "FAIL: Expected $CONTAINER_TEST_FLAG but got $RECOVERED_CONTAINER" >&2
        exit 1
    fi
else
    if [ -s "$OUT_DIR/recon_dispatch.txt" ]; then
        echo "SUCCESS: Container generated non-empty recon_dispatch.txt"
        rm -rf "$OUT_DIR"
        exit 0
    else
        echo "FAIL: Container output file is empty" >&2
        exit 1
    fi
fi
