# prompt_assembly — Agent Working Rules

These rules apply to **any** agent (human or model) editing the
`prompt_assembly/` tree. They are stricter than the repo-wide CLAUDE.md
because Phase 0 here is a contract lock that other phases will depend on.

## Phase boundaries

- This directory is **Phase 0 only**. Do not introduce assembler logic,
  resolver behavior, policy engines, compaction logic, signing logic, or
  any model interaction here.
- If you find yourself wanting to write something that *runs* against an
  input, stop. That belongs to a later phase, not Phase 0.
- A "tiny honest stub" is allowed only when it has no behavior beyond
  raising a Phase 0 error or returning a frozen contract object. No silent
  fallbacks. No fake completeness.

## Contract editing rules

- **Never** add a lane id to `common_enums.schema.json` outside the locked
  set `LC-1, LC-2, LC-4`. Reserved lanes (LC-3, LC-5) belong in
  `unsupported_local_lanes`, not in the lane id enum.
- **Never** widen `trust_level`, `constraint_type`, `hash_algorithm`,
  `serialization_format`, `signature_algorithm`, or `error_code` enums
  inside Phase 0. New values mean a new contract version, not a Phase 0
  edit.
- **Always** edit the JSON schema and the matching Pydantic model in the
  same patch. The alignment tests will fail loudly if these drift.
- **Always** add or update at least one test when you change a contract.

## Error taxonomy rules

- Error code string values are the contract. **Renaming** a code is a
  breaking change even if the Python enum member name is unchanged.
- New error codes require:
  1. an entry in `runtime/errors.py`
  2. an entry in `common_enums.schema.json#/$defs/error_code`
  3. a test in `tests/test_errors.py`
- Never raise a bare `Exception` from this subsystem. Always go through
  `PromptAssemblyError` or one of its subclasses.

## Configuration rules

- `config/defaults.yaml` must declare a `tokenizer_id` and a
  `tokenizer_version` for every active profile. Inactive profiles may omit
  details, but `active: false` must be explicit.
- The `baselines` block in `defaults.yaml` is locked: BLAKE3 / canonical
  JSON / Ed25519 / `1.1.0-phase0`. Do not edit it in Phase 0.

## Test discipline

- Every contract has at least one valid-fixture test and one
  required-field-removal test.
- Every controlled enum has at least one rejection test for an unknown
  value.
- The schema/model alignment tests in `tests/test_alignment.py` are not
  optional. Do not skip them.
- Run `python3 -m pytest prompt_assembly/tests -q` before claiming any
  Phase 0 change is complete.

## Documentation discipline

- `README.md` describes only what is **actually shipped**. Do not document
  later-phase behavior as if it works.
- If you defer something on purpose, list it under "What Phase 0
  deliberately does not ship" in the README. Do not hide deferrals.

## What to do when in doubt

Fail closed, log everything, write to the contract surface, and ask before
inventing behavior. The Phase 0 contract is the load-bearing object — every
later phase depends on it being honest.
