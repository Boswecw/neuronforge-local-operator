"""OperatorQueryNarrative.v1: human framing built only from the evidence object.

The narrative may not add source ids, remove contradictions, raise confidence,
claim authority, or change temporal order (plan 08). It is a pure function of
the evidence dict and never mutates it.
"""

from __future__ import annotations

import copy

_HEADER = (
    "Advisory context only (authoritative: false). "
    "This projection may explain and suggest; it may not approve, promote, "
    "or assert canonical truth."
)


def build_narrative(evidence: dict) -> str:
    evidence = copy.deepcopy(evidence)  # the narrative can never alter evidence
    lines = [_HEADER]
    facts = evidence.get("facts", {})
    query_type = evidence.get("query_type")

    if query_type == "current_baseline":
        if facts.get("baseline_run_id"):
            lines.append(
                f"Current baseline for {facts['task_contract']}: "
                f"{facts['baseline_run_id']} ({facts['model_id']} with "
                f"{facts['prompt_id']}), effective {facts['effective_at']}, "
                f"recorded by {facts['decision_id']}."
            )
        else:
            lines.append(
                f"No current baseline is projected for {facts.get('task_contract')}."
            )
    elif query_type == "baseline_history":
        entries = facts.get("entries", [])
        lines.append(
            f"{len(entries)} baseline decision(s) projected for "
            f"{facts.get('task_contract')}: "
            + "; ".join(
                f"{entry['run_id']} effective {entry['effective_at']} "
                f"({entry['decision_id']})"
                for entry in entries
            )
            if entries
            else f"No baseline history projected for {facts.get('task_contract')}."
        )
    elif query_type == "recurring_failures":
        recurring = facts.get("recurring_classes", [])
        if recurring:
            lines.append(
                "Recurring failure classes (count >= 2): " + ", ".join(recurring) + "."
            )
        else:
            lines.append("No failure class recurs across the projected runs.")
        for failure_class in sorted(facts.get("failure_classes", {})):
            bucket = facts["failure_classes"][failure_class]
            lines.append(
                f"{failure_class}: {bucket['count']} observation(s) "
                f"[{', '.join(bucket['failure_ids'])}] on runs "
                f"[{', '.join(bucket['run_ids'])}]."
            )
    elif query_type == "compare_runs":
        differing = facts.get("differing_fields", [])
        lines.append(
            "Differing fields: " + (", ".join(differing) if differing else "none") + "."
        )
        for key in ("run_a", "run_b"):
            run = facts[key]
            run_id = run["run_id"]
            lines.append(
                f"{run_id}: model {run['model_id']}, prompt {run['prompt_id']}, "
                f"status {run['status']}, evaluation outcomes "
                f"{facts['evaluation_outcomes'][run_id] or ['none']}, failure classes "
                f"{facts['failure_classes'][run_id] or ['none']}."
            )
    elif query_type == "explain_candidate":
        lines.append(
            f"{facts['run_id']} ({facts['model_id']} with {facts['prompt_id']}): "
            f"disposition {facts['disposition']}"
            + (f" per {facts['decision_id']}" if facts.get("decision_id") else "")
            + f"; evaluation outcomes {facts['evaluation_outcomes'] or ['none']}"
            + f"; failure classes {facts['failure_classes'] or ['none']}."
        )

    if evidence.get("contradicting_record_ids"):
        lines.append(
            "Contradicting records (review before acting): "
            + ", ".join(evidence["contradicting_record_ids"]) + "."
        )
    lines.append(
        "Promotion decisions remain manual operator review of canonical records."
    )
    return "\n".join(lines)
