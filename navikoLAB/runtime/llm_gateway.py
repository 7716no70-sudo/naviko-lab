# navikoLAB/runtime/llm_gateway.py

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import time
import uuid


PHASE = "Phase106-6 LLM Gateway (Safe Adapter Layer)"

ROOT = Path(__file__).resolve().parents[2]

LLM_DIR = ROOT / "runtime" / "llm_gateway"
LLM_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LLM_DIR / "llm_gateway_log.json"


# -----------------------------
# SAFE LLM ADAPTER (MOCK)
# -----------------------------

class MockLLM:

    def generate(self, prompt: str) -> str:

        # simulate latency
        time.sleep(0.1)

        return f"[MOCK-LLM] response to: {prompt}"


# -----------------------------
# REQUEST MODEL
# -----------------------------

@dataclass
class LLMRequest:
    request_id: str
    prompt: str


@dataclass
class LLMResponse:
    request_id: str
    output: str


# -----------------------------
# LLM GATEWAY (SAFE LAYER)
# -----------------------------

class LLMGateway:

    def __init__(self):

        self.llm = MockLLM()

        self.requests: list[LLMRequest] = []
        self.responses: list[LLMResponse] = []

    # -----------------------------
    # SAFE CALL
    # -----------------------------

    def call(self, prompt: str) -> LLMResponse:

        request = LLMRequest(
            request_id=str(uuid.uuid4()),
            prompt=prompt,
        )

        self.requests.append(request)

        # ALL GO THROUGH MOCK / SAFE ADAPTER
        output = self.llm.generate(prompt)

        response = LLMResponse(
            request.request_id,
            output,
        )

        self.responses.append(response)

        return response

    # -----------------------------
    # SIMULATED INTENT WRAPPER
    # -----------------------------

    def chat(self, user_text: str) -> str:

        prompt = f"""
You are Naviko AI OS.
Respond simply and safely.

User: {user_text}
"""

        res = self.call(prompt)

        return res.output

    # -----------------------------
    # SAVE LOG
    # -----------------------------

    def save(self):

        data = {
            "phase": PHASE,
            "requests": [r.__dict__ for r in self.requests],
            "responses": [r.__dict__ for r in self.responses],
        }

        LOG_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# -----------------------------
# ENTRY POINT
# -----------------------------

def main():

    gateway = LLMGateway()

    print("=== Naviko LLM Gateway ===")
    print("phase:", PHASE)
    print("mode: dry_run")

    print(gateway.chat("ナビ子こんにちは"))
    print(gateway.chat("今日のタスクは？"))

    gateway.save()

    print("saved:", LOG_FILE)


if __name__ == "__main__":
    main()