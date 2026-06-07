from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


class SourceArtifact(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_ref: str = Field(..., min_length=1, max_length=200)
    artifact_class: Literal["retrieval_package"] = "retrieval_package"
    artifact_hash: str = Field(..., min_length=16, max_length=128)
    source_gnat_run_id: str = Field(..., min_length=1, max_length=200)
    source_plan_hash: str = Field(..., min_length=1, max_length=200)
    source_state: Literal["ready", "partial_success"]
    completeness_status: Literal["complete", "incomplete"]
    retrieval_profile_id: str = Field(..., min_length=1, max_length=120)

    @model_validator(mode="after")
    def state_matches_completeness(self) -> "SourceArtifact":
        if self.source_state == "ready" and self.completeness_status != "complete":
            raise ValueError("ready source artifacts must be complete")
        if self.source_state == "partial_success" and self.completeness_status != "incomplete":
            raise ValueError("partial_success source artifacts must be incomplete")
        return self


class ExplicitRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_scope: Literal["app_request", "user_request"]
    requested_by: str = Field(..., min_length=1, max_length=200)
    operator_visible_summary: str = Field(..., min_length=1, max_length=300)


class ModelResourceDisclosure(BaseModel):
    model_config = ConfigDict(extra="forbid", protected_namespaces=())

    route_class: Literal["DETERMINISTIC", "FAST_LOCAL", "WORKHORSE_LOCAL", "HIGH_QUALITY_LOCAL"]
    model_id: str = Field(..., min_length=1, max_length=200)
    resource_budget_class: Literal[
        "deterministic",
        "fast_local",
        "workhorse_local",
        "high_quality_local",
    ]
    execution_mode: Literal["deterministic_adapter", "local_model"]


class CandidateGeneration(BaseModel):
    model_config = ConfigDict(extra="forbid", protected_namespaces=())

    candidate_contract_family: str = Field(..., min_length=1, max_length=200)
    semantic_result_posture: Literal["non_canonical_candidate"] = "non_canonical_candidate"
    allowed_candidate_classes: list[
        Literal[
            "structure_summary_candidate",
            "continuity_candidate",
            "code_relationship_candidate",
            "suggestion_candidate",
        ]
    ] = Field(..., min_length=1)
    model_resource_disclosure: ModelResourceDisclosure


class TransferGuardrails(BaseModel):
    model_config = ConfigDict(extra="forbid")

    cor_receipts_immutable: Literal[True] = True
    receipt_mutation_allowed: Literal[False] = False
    semantic_output_canonical: Literal[False] = False
    raw_content_included: Literal[False] = False
    details_redacted: Literal[True] = True


class CorGnatSemanticHandoffRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_version: Literal["GnatSemanticHandoff.v1"] = "GnatSemanticHandoff.v1"
    handoff_id: str = Field(..., min_length=1, max_length=200)
    request_id: str = Field(..., min_length=1, max_length=200)
    source_service_id: Literal["cortex"] = "cortex"
    destination_service_id: Literal["neuronforge-local"] = "neuronforge-local"
    source_artifact: SourceArtifact
    explicit_request: ExplicitRequest
    candidate_generation: CandidateGeneration
    transfer_guardrails: TransferGuardrails
    operator_visible_message: str = Field(..., min_length=1, max_length=500)
    created_at: str = Field(..., min_length=1)


class NeuronForgeGnatSemanticHandoffReceipt(BaseModel):
    model_config = ConfigDict(extra="forbid", protected_namespaces=())

    receipt_version: Literal["NeuronForgeGnatSemanticHandoffReceipt.v1"] = (
        "NeuronForgeGnatSemanticHandoffReceipt.v1"
    )
    receipt_id: str = Field(..., min_length=1, max_length=220)
    source_handoff_id: str = Field(..., min_length=1, max_length=200)
    request_id: str = Field(..., min_length=1, max_length=200)
    source_service_id: Literal["cortex"] = "cortex"
    destination_service_id: Literal["neuronforge-local"] = "neuronforge-local"
    candidate_contract_family: str = Field(..., min_length=1, max_length=200)
    candidate_generation_state: Literal["accepted_for_candidate_generation"]
    semantic_result_posture: Literal["non_canonical_candidate"] = "non_canonical_candidate"
    provenance_class: Literal["inferred_candidate"] = "inferred_candidate"
    cor_receipts_mutation_allowed: Literal[False] = False
    model_resource_disclosure: ModelResourceDisclosure
    details_redacted: Literal[True] = True
    operator_visible_summary: str = Field(..., min_length=1, max_length=500)
    accepted_at: str = Field(default_factory=_utc_now)


def accept_cor_gnat_semantic_handoff(
    request: CorGnatSemanticHandoffRequest,
) -> NeuronForgeGnatSemanticHandoffReceipt:
    return NeuronForgeGnatSemanticHandoffReceipt(
        receipt_id=f"nf-gnat-semantic-{request.handoff_id}",
        source_handoff_id=request.handoff_id,
        request_id=request.request_id,
        candidate_contract_family=request.candidate_generation.candidate_contract_family,
        candidate_generation_state="accepted_for_candidate_generation",
        model_resource_disclosure=request.candidate_generation.model_resource_disclosure,
        operator_visible_summary=(
            "Accepted referenced COR GNAT syntax artifact for non-canonical candidate generation; "
            "NeuronForge will not mutate COR receipts or claim canonical semantic truth."
        ),
    )
