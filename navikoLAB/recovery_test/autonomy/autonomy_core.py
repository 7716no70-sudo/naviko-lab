from navikoLAB.autonomy.autonomous_goal_engine import AutonomousGoalEngine
from navikoLAB.cognition.cognition_bridge import CognitionBridge
from navikoLAB.evolution.evolution_bridge import EvolutionBridge
from navikoLAB.self_modify.self_modify_bridge import SelfModifyBridge
from navikoLAB.planning.planning_core import PlanningCore
from navikoLAB.multi_agent.orchestrator import Orchestrator
from navikoLAB.external.external_core import ExternalCore
from navikoLAB.monitor_ui.ui_launcher import UILauncher
from navikoLAB.ai_network.network_orchestrator import NetworkOrchestrator
from navikoLAB.execution.execution_engine import ExecutionEngine
from navikoLAB.external.external_core import ExternalCore
from navikoLAB.evaluation.evaluation_engine import EvaluationEngine
from navikoLAB.evolution.self_evolution_engine import SelfEvolutionEngine
from navikoLAB.memory.memory_core import MemoryCore
from navikoLAB.goal.goal_stabilizer import GoalStabilizer
from navikoLAB.identity.identity_core import IdentityCore
from navikoLAB.decision.decision_stabilizer import DecisionStabilizer
from navikoLAB.conflict.conflict_resolver import ConflictResolver
from navikoLAB.self_repair.self_repair_engine import SelfRepairEngine
from navikoLAB.monitoring.health_monitor import HealthMonitor
from navikoLAB.stability.stability_kernel import StabilityKernel
from navikoLAB.backup.backup_manager import BackupManager
from navikoLAB.recovery.recovery_manager import RecoveryManager

class AutonomyCore:

    def __init__(self, daemon):

        self.goal_engine = AutonomousGoalEngine()
        self.cognition = CognitionBridge(daemon)
        self.evolution = EvolutionBridge()
        self.self_modify = SelfModifyBridge()

        self.evaluator = EvaluationEngine()
        self.self_evolution = SelfEvolutionEngine()

        self.network = NetworkOrchestrator()

        self.ui = UILauncher()

        self.multi_agent = Orchestrator()

        self.external = ExternalCore()

        self.execution = ExecutionEngine(self.external)

        # ★ Phase51追加
        self.planner = PlanningCore()
        
        self.external = ExternalCore()

        self.memory = MemoryCore()

        self.goal_stabilizer = GoalStabilizer()

        self.identity = IdentityCore() 

        self.decision = DecisionStabilizer(self.identity)

        self.stability = StabilityKernel()

        self.conflict = ConflictResolver()

        self.self_repair = SelfRepairEngine()

        self.health_monitor = HealthMonitor()

        # Phase67 BackupManager
        self.backup_manager = BackupManager()

        # Phase69 RecoveryManager
        self.recovery_manager = RecoveryManager()

        self.history = []


    def step(self, daemon):

        # ■ ① 観測
        snapshot = daemon.loop.scanner.scan()

        # ■ ② 分析系
        network_result = self.network.step(snapshot)
        planning_result = self.planner.run(snapshot)
        goals = self.goal_engine.generate(snapshot)
        cognition_result = self.cognition.step()

        # ■ ③ 外部（軽い処理）
        external_result = self.external.execute(
            "ui",
            {"goals": goals}
        )

        # ■ ④ 進化
        evolution_result = self.evolution.step(
            cognition_result,
            self.history
        )

        # ■ ⑤ 評価
        eval_result = self.evaluator.evaluate(
            self.history,
            goals
        )

        decision_result = self.decision.decide(
            goals,
            evolution_result,
            self.memory
        )

        if evolution_result.get("action") == "FORCE_EVOLUTION":
            decision_result["action_mode"] = "EXPAND"

        print("[DECISION]", decision_result)

        # ■ ⑥ 自己進化
        evo_state = self.self_evolution.evolve(
            eval_result.get("semantic"),
            eval_result.get("trigger"),
            eval_result.get("repetition")
        )

        # ■ ⑦ 実行（Phase62修正版）
        if (
            decision_result.get("action_mode") in ["EXPAND", "NORMAL"]
            and evolution_result.get("action") in ["FORCE_EVOLUTION", "EVOLUTION"]
        ):
            execution_result = self.execution.execute({
                "type": "file",
                "path": "naviko_output.txt",
                "content": str(goals)
            })
        else:
            execution_result = {"status": "skipped"}    

        # ■ ⑧ Identity（Phase61）
        identity_state = self.identity.evolve_identity(
            self.memory,
            evolution_result
        )

        stability_result = self.stability.run(
            decision_result,
            self.memory,
            identity_state,
            evolution_result
        )

        decision_result = stability_result["decision"]

        health_result = self.health_monitor.evaluate(
            stability_result,
            self.memory,
            identity_state,
            decision_result,
            evolution_result,
            execution_result
        )

        # Phase67-2 Backup trigger
        backup_result = {"status": "skipped"}

        if (
            health_result.get("system_health") == "stable"
            and evolution_result.get("action") == "FORCE_EVOLUTION"
        ):
            backup_result = self.backup_manager.create_snapshot(
                label="stable_force_evolution"
            )
        # Phase69-3 Recovery trigger
        recovery_result = self.recovery_manager.run(
            health_result,
            stability_result
        )


        conflict_result = self.conflict.resolve(
            goals,
            identity_state,
            evolution_result,
            decision_result,
            self.memory
        )

        # ■ ⑨ Memory保存
        self.memory.save_goal(goals)
        self.memory.save_execution(execution_result)
        self.memory.save_evolution(evolution_result)

        # Phase66-3 Health履歴保存
        if hasattr(self.memory, "save_health"):
            self.memory.save_health(health_result)

        # ■ ⑩ History
        self.history.append({
            "goals": goals,
            "eval": eval_result,
            "evo": evo_state,
            "identity": identity_state,
            "decision": decision_result,
            "health": health_result,
            "backup": backup_result,
            "recovery": recovery_result
        })

        # ■ Phase64 Self Repair
        repair_result = self.self_repair.repair(
            snapshot,
            self.memory,
            identity_state,
            conflict_result,
            execution_result
        )

        # ■ ⑪ UI（最後）
        self.ui.run({
            "goals": goals,
            "network": network_result,
            "planning": planning_result,
            "evolution": evolution_result,

            "memory": self.memory.latest(),
            "identity": identity_state,

            "history_size": len(self.history),
            "memory_size": len(self.memory.goal_memory),

            "decision": decision_result,

            "conflict": conflict_result,

            "self_repair": repair_result,
            "backup": backup_result,
            "recovery": recovery_result,

            "system_health": health_result["system_health"],
            "health_score": health_result["health_score"],
            "stability_score": health_result["stability_score"],
            "warnings": health_result["warnings"]
        })


        # ■ ⑫ debug
        if execution_result:
            print("[EXECUTION]", execution_result)

        if backup_result:
            print("[BACKUP]", backup_result)

        if recovery_result:
            print("[RECOVERY]", recovery_result)

        

        # ■ Multi-Agent（1回だけ）
        multi_result = self.multi_agent.run(snapshot)

        # ■ ⑬ return
        return {
            "goals": goals,
            "network": network_result,
            "multi_agent": multi_result,   # ★修正
            "external": external_result,
            "decision": decision_result,
            "planning": planning_result,
            "cognition": cognition_result,
            "evolution": evolution_result,
            "conflict": conflict_result,
            "self_repair": repair_result,
            "behavior": self.self_modify.step(
                cognition_result,
                evolution_result.get("action", "NORMAL")
            ),
            "execution": execution_result,
            "health": health_result,
            "backup": backup_result,
            "recovery": recovery_result
        }