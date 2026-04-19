# neuronforge wave-1 promotion seam — operator examples

- mirror: `registry/pact_wave1_envelope_mirror.json`
- manifest hash: `sha256:26b75ef5232a149e523d1bf2db1302cf5a9ba4025d66cdaecbd227e0dadedcf8`
- strict success hash: `sha256:e11c303a2d61950cef8502d41e6337cf53c2dae94456bdff79d12cde8304568c`
- admission stage: `wave1_internal`

## case_1_strict_admitted — PASS
- admission: `strict_admitted`
- reason codes: none

## case_2_non_strict_admitted — PASS
- admission: `non_strict_admitted`
- reason codes: none

## case_3_missing_manifest — PASS
- admission: `not_admitted`
- reason codes: `manifest_hash_missing`

## case_4_unsupported_profile — PASS
- admission: `not_admitted`
- reason codes: `used_profile_unsupported`

## case_5_digest_mismatch — PASS
- admission: `not_admitted`
- reason codes: `non_strict_canonical_digest_mismatch`

## case_6_lineage_loss_attempt — PASS
- admission: `strict_admitted`
- reason codes: none

## case_7_replay_stable — PASS
- admission: `strict_admitted`
- reason codes: none
