"""
Ollama adapter for analyze.style.scene.v1.

Calls the local Ollama instance following the same pattern as the existing
run-continuity-adjacent-scene.sh executor: stream the system prompt
followed by the scene text, collect output, return raw text.

The adapter uses the Ollama HTTP API (localhost:11434) rather than the
CLI to avoid requiring subprocess shell escaping.  If Ollama is
unavailable, a RuntimeError is raised and the caller emits a failed
response.
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from pathlib import Path

OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5:14b"
PROMPT_FILE = Path(__file__).resolve().parent.parent.parent / "prompts" / "style-analysis-scene-v1.md"


def _load_system_prompt() -> str:
    """Read the frozen v1 system prompt from disk."""
    try:
        return PROMPT_FILE.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"Could not read prompt file {PROMPT_FILE}: {exc}") from exc


def call_ollama(
    scene_text: str,
    model: str = DEFAULT_MODEL,
    timeout_seconds: int = 120,
) -> str:
    """
    Send the scene text to the local Ollama model and return raw output.

    Uses the Ollama /api/generate endpoint with the system prompt in the
    dedicated `system` field so instruction-level constraints (dimension
    definitions, hard rules) are treated as authoritative by the model.

    Raises:
        RuntimeError: if the Ollama server is unreachable or returns an
                      error response.
    """
    system_prompt = _load_system_prompt()

    payload = json.dumps(
        {
            "model": model,
            "system": system_prompt,
            "prompt": scene_text,
            "stream": False,
        }
    ).encode("utf-8")

    url = f"{OLLAMA_BASE_URL}/api/generate"
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout_seconds) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Ollama server unreachable at {OLLAMA_BASE_URL}: {exc}"
        ) from exc

    try:
        body = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Unexpected response from Ollama (not JSON): {exc}") from exc

    if body.get("error"):
        raise RuntimeError(f"Ollama returned error: {body['error']}")

    response_text: str = body.get("response", "")
    if not response_text:
        raise RuntimeError("Ollama returned empty response")

    return response_text
