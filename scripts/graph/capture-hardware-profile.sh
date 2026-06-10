#!/bin/bash
# Capture an NLOHardwareProfile.v1 record for the current host (G-04).
#
# Emits JSON on stdout (or to --output FILE). Metrics that cannot be captured
# on this host are listed in unsupported_metrics instead of being guessed.
#
# Usage:  bash scripts/graph/capture-hardware-profile.sh [--output FILE]
set -euo pipefail

OUTPUT=""
if [[ "${1:-}" == "--output" ]]; then
  OUTPUT="${2:?--output requires a file path}"
fi

NOW="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
HOST_SLUG="$(hostname 2>/dev/null | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9-' | cut -c1-40)"
[[ -n "$HOST_SLUG" ]] || HOST_SLUG="unknown-host"
PROFILE_ID="hw-${HOST_SLUG}-$(date -u +%Y%m%d%H%M%S)"

unsupported=()
fields=()

json_escape() {
  # bounded escape for strings we mostly control; strips control chars
  printf '%s' "$1" | tr -d '\000-\037' | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' | cut -c1-200
}

OS="$(uname -s 2>/dev/null | tr '[:upper:]' '[:lower:]' || true)"
if [[ -n "$OS" ]]; then
  fields+=("\"os\": \"$(json_escape "$OS")\"")
else
  unsupported+=("os")
fi

KERNEL="$(uname -r 2>/dev/null || true)"
if [[ -n "$KERNEL" ]]; then
  fields+=("\"kernel\": \"$(json_escape "$KERNEL")\"")
else
  unsupported+=("kernel")
fi

CPU_MODEL="$(awk -F': +' '/^model name/{print $2; exit}' /proc/cpuinfo 2>/dev/null || true)"
if [[ -n "$CPU_MODEL" ]]; then
  fields+=("\"cpu_model\": \"$(json_escape "$CPU_MODEL")\"")
else
  unsupported+=("cpu_model")
fi

CPU_CORES="$(nproc 2>/dev/null || true)"
if [[ "$CPU_CORES" =~ ^[0-9]+$ && "$CPU_CORES" -ge 1 ]]; then
  fields+=("\"cpu_cores\": $CPU_CORES")
else
  unsupported+=("cpu_cores")
fi

MEM_TOTAL_KB="$(awk '/^MemTotal:/{print $2}' /proc/meminfo 2>/dev/null || true)"
if [[ "$MEM_TOTAL_KB" =~ ^[0-9]+$ ]]; then
  fields+=("\"mem_total_gb\": $(awk -v kb="$MEM_TOTAL_KB" 'BEGIN{printf "%.1f", kb/1048576}')")
else
  unsupported+=("mem_total_gb")
fi

MEM_AVAIL_KB="$(awk '/^MemAvailable:/{print $2}' /proc/meminfo 2>/dev/null || true)"
if [[ "$MEM_AVAIL_KB" =~ ^[0-9]+$ ]]; then
  fields+=("\"mem_available_gb\": $(awk -v kb="$MEM_AVAIL_KB" 'BEGIN{printf "%.1f", kb/1048576}')")
else
  unsupported+=("mem_available_gb")
fi

if command -v nvidia-smi >/dev/null 2>&1; then
  GPU_NAME="$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -1 || true)"
  GPU_VRAM_MB="$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1 | tr -d ' ' || true)"
  if [[ -n "$GPU_NAME" && "$GPU_VRAM_MB" =~ ^[0-9]+$ ]]; then
    fields+=("\"gpu\": {\"name\": \"$(json_escape "$GPU_NAME")\", \"vram_gb\": $(awk -v mb="$GPU_VRAM_MB" 'BEGIN{printf "%.1f", mb/1024}')}")
  elif [[ -n "$GPU_NAME" ]]; then
    fields+=("\"gpu\": {\"name\": \"$(json_escape "$GPU_NAME")\"}")
  else
    unsupported+=("gpu")
  fi
else
  unsupported+=("gpu")
fi

UNSUPPORTED_JSON="[]"
if [[ ${#unsupported[@]} -gt 0 ]]; then
  sorted="$(printf '%s\n' "${unsupported[@]}" | sort | awk '{printf "%s\"%s\"", (NR>1?", ":""), $0}')"
  UNSUPPORTED_JSON="[${sorted}]"
fi

EXTRA=""
if [[ ${#fields[@]} -gt 0 ]]; then
  EXTRA="$(printf '%s,\n  ' "${fields[@]}")"
fi

JSON=$(cat <<JSONEOF
{
  "schema_version": "nlo-hardware-profile-v1",
  "hardware_profile_id": "${PROFILE_ID}",
  "captured_at": "${NOW}",
  "capture_tool": "scripts/graph/capture-hardware-profile.sh",
  ${EXTRA}"unsupported_metrics": ${UNSUPPORTED_JSON},
  "recorded_at": "${NOW}"
}
JSONEOF
)

if [[ -n "$OUTPUT" ]]; then
  printf '%s\n' "$JSON" > "$OUTPUT"
  echo "wrote $OUTPUT" >&2
else
  printf '%s\n' "$JSON"
fi
