# navikoLAB/runtime/tool_gateway.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json
import uuid


PHASE = "Phase106-2 Naviko Tool Gateway Layer"

ROOT = Path(__file__).resolve().parents[2]

TOOL_DIR = ROOT / "runtime" / "tool_gateway"
TOOL_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = TOOL_DIR / "tool_gateway_log.json"


# -----------------------------
# TOOL REGISTRY (SAFE ONLY)
# -----------------------------

ALLOWED_TOOLS = {
    "log_note": "Write safe log entry",
    "generate_text": "Simulated text generation",
    "analyze_data": "Simulated analysis",
}


# -----------------------------
# TOOL REQUEST MODEL
# -----------------------------

@dataclass
class ToolRequest:
    request_id: str
    tool_name: str
    payload: str
    timestamp: str


@dataclass
class ToolResult:
    request_id: str
    tool_name: str
    status: str
    output: str


# -----------------------------
# TOOL GATEWAY CORE
# -----------------------------

class ToolGateway:

    def __init__(self):

        self.requests: list[ToolRequest] = []
        self.results: list[ToolResult] = []

    # -----------------------------
    # TOOL EXECUTION (DRY RUN ONLY)
    # -----------------------------

    def execute_tool(self, tool_name: str, payload: str):

        request = ToolRequest(
            request_id=str(uuid.uuid4()),
            tool_name=tool_name,
            payload=payload,
            timestamp=datetime.now().isoformat(timespec="seconds"),
        )

        self.requests.append(request)

        if tool_name not in ALLOWED_TOOLS:

            result = ToolResult(
                request.request_id,
                tool_name,
                status="denied",
                output="[DRY RUN] tool not allowed",
            )

        else:

            result = ToolResult(
                request.request_id,
                tool_name,
                status="approved_dry_run",
                output=f"[DRY RUN] executed tool: {tool_name} with {payload}",
            )

        self.results.append(result)

        return result

    # -----------------------------
    # SIMULATED HIGH LEVEL ACTIONS
    # -----------------------------

    def log_note(self, text: str):

        return self.execute_tool("log_note", text)

    def generate_text(self, prompt: str):

        return self.execute_tool("generate_text", prompt)

    def analyze_data(self, data: str):

        return self.execute_tool("analyze_data", data)

    def unsafe_tool(self, name: str, payload: str):

        # everything else blocked
        return self.execute_tool(name, payload)

    # -----------------------------
    # SAVE LOG
    # -----------------------------

    def save(self):

        data = {
            "phase": PHASE,
            "requests": [r.__dict__ for r in self.requests],
            "results": [r.__dict__ for r in self.results],
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }

        LOG_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# -----------------------------
# ENTRY POINT
# -----------------------------

def main():

    gateway = ToolGateway()

    # safe simulated calls
    gateway.log_note("Naviko started tool gateway")
    gateway.generate_text("Explain AI OS in simple terms")
    gateway.analyze_data("sample dataset")

    # blocked call simulation
    gateway.unsafe_tool("delete_system_files", "test")

    gateway.save()

    print("=== Naviko Tool Gateway ===")
    print("phase:", PHASE)
    print("mode: dry_run")
    print("allowed_tools:", len(ALLOWED_TOOLS))
    print("requests:", len(gateway.requests))
    print("results:", len(gateway.results))
    print("saved:", LOG_FILE)


if __name__ == "__main__":
    main()