#!/usr/bin/env bash
set -euo pipefail

# render-continuity-candidate.sh
#
# Bloom-facing Markdown renderer for a continuity candidate artifact envelope.
#
# Renders the envelope as a reviewer-readable Markdown document.
# No canonicality language. No promotion UI. Candidate framing throughout.
#
# Usage:
#   scripts/render-continuity-candidate.sh <envelope_file>
#   scripts/render-continuity-candidate.sh <envelope_file> <output_file>

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <envelope_file> [output_file]"
  exit 1
fi

ENVELOPE_FILE="$1"
OUTPUT_FILE="${2:-}"

if [ ! -f "$ENVELOPE_FILE" ]; then
  echo "Error: envelope file not found: $ENVELOPE_FILE" >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "Error: jq is required" >&2
  exit 1
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

render() {
  local STATUS TASK_ID RUN_ID MODEL TIMESTAMP SCOPE FINDINGS_COUNT

  STATUS="$(jq -r '.envelope_status' "$ENVELOPE_FILE")"
  TASK_ID="$(jq -r '.task_id' "$ENVELOPE_FILE")"
  RUN_ID="$(jq -r '.run_id' "$ENVELOPE_FILE")"
  MODEL="$(jq -r '.model_id' "$ENVELOPE_FILE")"
  TIMESTAMP="$(jq -r '.timestamp' "$ENVELOPE_FILE")"
  SCOPE="$(jq -r '.scope_label' "$ENVELOPE_FILE")"
  FINDINGS_COUNT="$(jq '.candidate_findings | length' "$ENVELOPE_FILE")"
  PACKET_ID="$(jq -r '.scene_packet_id // "—"' "$ENVELOPE_FILE")"

  echo "# Continuity Candidate Review"
  echo
  echo "| Field | Value |"
  echo "|-------|-------|"
  echo "| Task | \`$TASK_ID\` |"
  echo "| Run | \`$RUN_ID\` |"
  echo "| Model | \`$MODEL\` |"
  echo "| Scope | $SCOPE |"
  echo "| Packet | $PACKET_ID |"
  echo "| Timestamp | $TIMESTAMP |"
  echo "| Status | **$STATUS** |"
  echo

  # --- Fail-closed path ---

  if [ "$STATUS" = "fail_closed" ]; then
    local FAILURE_REASON
    FAILURE_REASON="$(jq -r '.failure_reason // "unknown"' "$ENVELOPE_FILE")"

    echo "## Result: Fail Closed"
    echo
    echo "> **This run failed validation. No candidate findings are available.**"
    echo
    echo "**Failure reason:** $FAILURE_REASON"
    echo
    echo "_Investigate the failure reason and re-run before proceeding._"
    echo
    echo "---"
    echo
    echo "> No findings are promoted or available for review from this run."
    return
  fi

  # --- Valid candidate path ---

  local OVERALL_NOTE
  OVERALL_NOTE="$(jq -r '.overall_run_note // ""' "$ENVELOPE_FILE")"

  echo "## Summary"
  echo
  echo "$OVERALL_NOTE"
  echo
  echo "**Candidate findings:** $FINDINGS_COUNT"
  echo

  echo "---"
  echo

  if [ "$FINDINGS_COUNT" -eq 0 ]; then
    echo "_No candidate findings were identified in this bounded two-scene window._"
    echo
    echo "> This is a valid result. A zero-finding run means no strong review issue was detected"
    echo "> within scope. It does not mean the scenes are error-free beyond this window."
    echo
    echo "---"
    echo
    echo "> **Posture reminder:** These are candidate findings for reviewer consideration only."
    echo "> No finding represents canonical story truth."
    return
  fi

  # --- Render each finding ---

  for i in $(seq 0 $((FINDINGS_COUNT - 1))); do
    local FID LABEL FTYPE CLAIM SCOPE_TYPE CONFIDENCE UNCERTAINTY REVIEW_NOTE STATE SEVERITY
    FID="$(jq -r ".candidate_findings[$i].finding_id" "$ENVELOPE_FILE")"
    LABEL="$(jq -r ".candidate_findings[$i].finding_label" "$ENVELOPE_FILE")"
    FTYPE="$(jq -r ".candidate_findings[$i].finding_type" "$ENVELOPE_FILE")"
    CLAIM="$(jq -r ".candidate_findings[$i].claim" "$ENVELOPE_FILE")"
    SCOPE_TYPE="$(jq -r ".candidate_findings[$i].scope_type" "$ENVELOPE_FILE")"
    CONFIDENCE="$(jq -r ".candidate_findings[$i].confidence" "$ENVELOPE_FILE")"
    UNCERTAINTY="$(jq -r ".candidate_findings[$i].uncertainty_note" "$ENVELOPE_FILE")"
    REVIEW_NOTE="$(jq -r ".candidate_findings[$i].review_note" "$ENVELOPE_FILE")"
    STATE="$(jq -r ".candidate_findings[$i].candidate_state" "$ENVELOPE_FILE")"
    SEVERITY="$(jq -r ".candidate_findings[$i].severity_hint // \"—\"" "$ENVELOPE_FILE")"

    echo "## $FID — $LABEL"
    echo
    echo "| Field | Value |"
    echo "|-------|-------|"
    echo "| Type | \`$FTYPE\` |"
    echo "| Scope | $SCOPE_TYPE |"
    echo "| Confidence | $CONFIDENCE |"
    echo "| Severity hint | $SEVERITY |"
    echo "| State | \`$STATE\` |"
    echo
    echo "**Candidate claim:**"
    echo
    echo "> $CLAIM"
    echo
    echo "**Evidence:**"
    echo

    local NUM_SPANS
    NUM_SPANS="$(jq ".candidate_findings[$i].evidence_spans | length" "$ENVELOPE_FILE")"

    for j in $(seq 0 $((NUM_SPANS - 1))); do
      local SCENE_ID SPAN_TEXT SPAN_ROLE POS_HINT
      SCENE_ID="$(jq -r ".candidate_findings[$i].evidence_spans[$j].scene_id" "$ENVELOPE_FILE")"
      SPAN_TEXT="$(jq -r ".candidate_findings[$i].evidence_spans[$j].span_text" "$ENVELOPE_FILE")"
      SPAN_ROLE="$(jq -r ".candidate_findings[$i].evidence_spans[$j].span_role" "$ENVELOPE_FILE")"
      POS_HINT="$(jq -r ".candidate_findings[$i].evidence_spans[$j].position_hint // \"\"" "$ENVELOPE_FILE")"

      if [ -n "$POS_HINT" ]; then
        echo "- **[$SCENE_ID]** (\`$SPAN_ROLE\`, $POS_HINT): \"$SPAN_TEXT\""
      else
        echo "- **[$SCENE_ID]** (\`$SPAN_ROLE\`): \"$SPAN_TEXT\""
      fi
    done

    echo
    echo "**Uncertainty:** $UNCERTAINTY"
    echo
    echo "**Review note:** $REVIEW_NOTE"
    echo

    # Optional: taxonomy tags
    local TAG_COUNT
    TAG_COUNT="$(jq ".candidate_findings[$i].taxonomy_tags | length // 0" "$ENVELOPE_FILE" 2>/dev/null || echo 0)"
    if [ "$TAG_COUNT" -gt 0 ]; then
      local TAGS
      TAGS="$(jq -r ".candidate_findings[$i].taxonomy_tags | join(\", \")" "$ENVELOPE_FILE")"
      echo "**Tags:** $TAGS"
      echo
    fi

    echo "---"
    echo
  done

  echo "> **Posture reminder:** These are candidate findings for reviewer consideration only."
  echo "> No finding represents canonical story truth."
  echo "> Each finding requires human review before any action is taken."
}

if [ -n "$OUTPUT_FILE" ]; then
  render > "$OUTPUT_FILE"
  echo "Rendered to: $OUTPUT_FILE"
else
  render
fi
