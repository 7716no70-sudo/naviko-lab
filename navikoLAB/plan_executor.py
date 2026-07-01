import json
from pathlib import Path
from datetime import datetime


class PlanExecutor:
    def __init__(self, root_dir, agent_registry=None):
        self.root = Path(root_dir)
        self.agent_registry = agent_registry

        self.executor_dir = self.root / "executions"
        self.executor_dir.mkdir(parents=True, exist_ok=True)

        self.execution_log_file = self.executor_dir / "execution_log.json"

        if not self.execution_log_file.exists():
            self.execution_log_file.write_text("[]", encoding="utf-8")

    def _load_log(self):
        try:
            return json.loads(self.execution_log_file.read_text(encoding="utf-8"))
        except Exception:
            return []

    def _save_log(self, data):
        self.execution_log_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def create_execution(self, plan):
        steps = []

        for i, step in enumerate(plan.get("steps", []), start=1):
            steps.append({
                "step_number": i,
                "text": step,
                "status": "pending",
                "started_at": None,
                "completed_at": None,
                "result": ""
            })

        execution = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "purpose": plan.get("purpose", ""),
            "selected_agents": plan.get("selected_agents", []),
            "required_capabilities": plan.get("required_capabilities", []),
            "steps": steps,
            "status": "created"
        }

        log = self._load_log()
        log.append(execution)
        self._save_log(log)

        return execution

    def mark_step_running(self, execution, step_number):
        for step in execution.get("steps", []):
            if step.get("step_number") == step_number:
                step["status"] = "running"
                step["started_at"] = datetime.now().isoformat(timespec="seconds")
                execution["status"] = "running"
                return True

        return False

    def mark_step_done(self, execution, step_number, result=""):
        for step in execution.get("steps", []):
            if step.get("step_number") == step_number:
                step["status"] = "done"
                step["completed_at"] = datetime.now().isoformat(timespec="seconds")
                step["result"] = result
                return True

        return False

    def mark_step_failed(self, execution, step_number, result=""):
        for step in execution.get("steps", []):
            if step.get("step_number") == step_number:
                step["status"] = "failed"
                step["completed_at"] = datetime.now().isoformat(timespec="seconds")
                step["result"] = result
                execution["status"] = "failed"
                return True

        return False

    def run_simulation(self, plan):
        execution = self.create_execution(plan)

        for step in execution.get("steps", []):
            number = step.get("step_number")
            self.mark_step_running(execution, number)
            self.mark_step_done(
                execution,
                number,
                result="仮実行成功"
            )

        execution["status"] = "completed"

        if self.agent_registry:
            for agent_id in execution.get("selected_agents", []):
                self.agent_registry.record_result(agent_id, success=True)

        log = self._load_log()
        log.append(execution)
        self._save_log(log)

        return execution

    def diagnose_executor(self):
        log = self._load_log()

        completed = 0
        failed = 0
        running = 0

        for item in log:
            status = item.get("status")

            if status == "completed":
                completed += 1
            elif status == "failed":
                failed += 1
            elif status == "running":
                running += 1

        return {
            "execution_count": len(log),
            "completed_count": completed,
            "failed_count": failed,
            "running_count": running,
            "execution_log_file": str(self.execution_log_file),
            "agent_registry_connected": self.agent_registry is not None
        }

    def format_execution(self, execution):
        lines = []
        lines.append("=== ナビ子 v1.2 PlanExecutor 実行ログ ===")
        lines.append(f"目的: {execution.get('purpose')}")
        lines.append(f"状態: {execution.get('status')}")
        lines.append("")

        lines.append("使用エージェント:")
        for agent in execution.get("selected_agents", []):
            lines.append(f"- {agent}")

        lines.append("")
        lines.append("ステップ:")
        for step in execution.get("steps", []):
            lines.append(
                f"{step.get('step_number')}. "
                f"[{step.get('status')}] "
                f"{step.get('text')} / "
                f"{step.get('result')}"
            )

        return "\n".join(lines)