"""NeuronForge Local prompt-assembly runtime layer (Phase 0).

Phase 0 only ships:

* Pydantic v2 models that mirror the JSON contracts under
  ``prompt_assembly/contracts/``.
* The stable error taxonomy.

No assembler logic lives here yet. Importing this package must remain free
of side effects.
"""

from prompt_assembly.runtime import errors, models  # noqa: F401

__all__ = ["errors", "models"]
