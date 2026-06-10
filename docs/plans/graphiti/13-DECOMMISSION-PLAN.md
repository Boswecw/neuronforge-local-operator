# Decommission Plan

## Principle

The pilot must remain removable in one bounded change set.

## Removal Scope

Remove:

- Graphiti dependency;
- graph backend compose files;
- graph runtime package;
- graph CLI commands;
- environment variables;
- Docker volumes;
- projection reports;
- Graphiti-specific tests;
- Graphiti-specific documentation.

Retain:

- normalized experiment schemas;
- failure taxonomy;
- hardware provenance;
- canonical run/evaluation/decision records;
- source-of-truth matrix;
- independently useful operator evidence contracts;
- comparison findings.

## Secure Deletion

Run:

1. stop containers;
2. remove containers;
3. remove named volumes;
4. delete local exports;
5. delete caches;
6. verify no graph ports remain open;
7. verify no credentials remain;
8. remove ignored runtime directories.

## Decommission Verification

- NLO tests pass without Graphiti installed;
- no import references remain;
- no environment variables remain required;
- no canonical schema requires Graphiti fields;
- canonical experiment records remain valid;
- public NeuronForge is unaffected.
