import json
from pathlib import Path
from datetime import datetime
from navikoLAB.core.autonomous_capability_flow import AutonomousCapabilityFlow

class AutonomousCore:
    def __init__(
        self,
        root_dir,
        memory_manager=None,
        goal_manager=None,
        agent_registry=None,
        task_planner=None,
        plan_executor=None,
        autonomy_controller=None,
        mission_bridge=None
    ):
        self.root = Path(root_dir)

        self.memory_manager = memory_manager
        self.goal_manager = goal_manager
        self.agent_registry = agent_registry
        self.task_planner = task_planner
        self.plan_executor = plan_executor
        self.autonomy_controller = autonomy_controller
        self.mission_bridge = mission_bridge

        self.autonomous_capability_flow = AutonomousCapabilityFlow(
            self.root.parent
        )

        self.core_dir = self.root / "autonomous_core"
        self.core_dir.mkdir(parents=True, exist_ok=True)

        self.core_log_file = self.core_dir / "autonomous_core_log.json"

        if not self.core_log_file.exists():
            self.core_log_file.write_text("[]", encoding="utf-8")

    def _load_log(self):
        try:
            return json.loads(self.core_log_file.read_text(encoding="utf-8"))
        except Exception:
            return []

    def _save_log(self, data):
        self.core_log_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def process_purpose(self, purpose):
        result = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "purpose": purpose,
            "memory_saved": False,
            "goal_summary": None,
            "mission": None,
            "capability_flow": None,
            "plan": None,
            "autonomy": None,
            "execution": None,
            "status": "started",
            "messages": []
        }

        if self.memory_manager:
            self.memory_manager.add_memory(
                f"目的を受信: {purpose}",
                importance=5,
                memory_type="short"
            )
            result["memory_saved"] = True
            result["messages"].append("目的を短期記憶に保存しました。")

        if self.mission_bridge:
            mission = self.mission_bridge.create_from_goal(
                purpose,
                "AutonomousCoreから作成されたMission"
            )

            result["mission"] = mission

            result["messages"].append(
                "MissionManagerに長期ミッションを作成しました。"
            )

            capability_flow_result = self.autonomous_capability_flow.run(
                mission
            )

            result["capability_flow"] = capability_flow_result

            result["messages"].append(
                "CapabilityRouterとAgentExecutorを実行しました。"
            )


        if self.goal_manager:
            result["goal_summary"] = self.goal_manager.diagnose_goals()
            result["messages"].append("目標状態を確認しました。")

        if not self.task_planner:
            result["status"] = "failed"
            result["messages"].append("TaskPlanner が接続されていません。")
            self._append_log(result)
            return result

        plan = self.task_planner.create_plan(purpose)
        result["plan"] = plan
        result["messages"].append("実行計画を作成しました。")

        if self.mission_bridge and result.get("mission"):
            self.mission_bridge.mission_manager.update_status(
                result["mission"]["id"],
                "waiting_agent"
            )

            result["messages"].append(
                "Mission状態をwaiting_agentへ更新しました。"
            )


        if self.autonomy_controller:
            autonomy = self.autonomy_controller.diagnose_autonomy()
            result["autonomy"] = autonomy
            result["messages"].append("自律実行許可を確認しました。")

            can_execute = self.autonomy_controller.can_execute_plan()
        else:
            can_execute = False
            result["messages"].append("AutonomyController 未接続のため仮実行のみ許可。")

        if not self.plan_executor:
            result["status"] = "planned_only"
            result["messages"].append("PlanExecutor 未接続のため計画のみ作成しました。")
            self._append_log(result)
            return result

        if self.mission_bridge and result.get("mission"):
            self.mission_bridge.start_build(
                result["mission"]["id"]
            )

            result["messages"].append(
                "Mission状態をbuildingへ更新しました。"
            )


        if can_execute:
            execution = self.plan_executor.run_simulation(plan)
            result["execution"] = execution
            result["status"] = "executed_simulation"
            result["messages"].append("現在は安全上、実行処理は仮実行として処理しました。")
        else:
            execution = self.plan_executor.run_simulation(plan)
            result["execution"] = execution
            result["status"] = "safe_simulation_completed"
            result["messages"].append("安全モードのため仮実行を完了しました。")

        if self.mission_bridge and result.get("mission"):
            self.mission_bridge.start_reflection(
                result["mission"]["id"]
            )

            self.mission_bridge.start_improvement(
                result["mission"]["id"]
            )

            self.mission_bridge.complete(
                result["mission"]["id"]
            )

            result["messages"].append(
                "Mission状態をreflection→improving→completedへ更新しました。"
            )


        self._append_log(result)
        return result

    def _append_log(self, result):
        log = self._load_log()
        log.append(result)
        self._save_log(log)

    def diagnose_core(self):
        log = self._load_log()

        return {
            "core_log_count": len(log),
            "core_log_file": str(self.core_log_file),
            "memory_connected": self.memory_manager is not None,
            "goal_connected": self.goal_manager is not None,
            "agent_registry_connected": self.agent_registry is not None,
            "task_planner_connected": self.task_planner is not None,
            "plan_executor_connected": self.plan_executor is not None,
            "autonomy_controller_connected": self.autonomy_controller is not None,
            "mission_bridge_connected": self.mission_bridge is not None
        }

    def format_result(self, result):
        lines = []
        lines.append("=== ナビ子 v1.2 AutonomousCore 統合処理結果 ===")
        lines.append(f"目的: {result.get('purpose')}")
        lines.append(f"状態: {result.get('status')}")
        lines.append("")

        lines.append("メッセージ:")
        for msg in result.get("messages", []):
            lines.append(f"- {msg}")

        plan = result.get("plan")
        if plan:
            lines.append("")
            lines.append("必要能力:")
            for cap in plan.get("required_capabilities", []):
                lines.append(f"- {cap}")

            lines.append("")
            lines.append("選択エージェント:")
            for agent in plan.get("selected_agents", []):
                lines.append(f"- {agent}")

        autonomy = result.get("autonomy")
        if autonomy:
            lines.append("")
            lines.append("自律許可:")
            lines.append(f"- モード: {autonomy.get('mode')}")
            lines.append(f"- 許可レベル: {autonomy.get('permission_level')}")
            lines.append(f"- 実行許可: {autonomy.get('allow_real_execution')}")

        execution = result.get("execution")
        if execution:
            lines.append("")
            lines.append("実行状態:")
            lines.append(f"- {execution.get('status')}")
            lines.append(f"- ステップ数: {len(execution.get('steps', []))}")

        return "\n".join(lines)