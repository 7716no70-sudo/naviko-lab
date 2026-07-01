# navikoLAB/core/naviko_core.py

from pathlib import Path

from navikoLAB.memory_engine import MemoryEngine
from navikoLAB.memory.memory_agent import MemoryAgent
from navikoLAB.personality_engine import PersonalityEngine
from navikoLAB.growth_engine import GrowthEngine
from navikoLAB.decision_engine import DecisionEngine
from navikoLAB.conversation_engine import ConversationEngine
from navikoLAB.self_growth_loop import SelfGrowthLoop
from navikoLAB.planner_engine import PlannerEngine
from navikoLAB.execution_engine import ExecutionEngine
from navikoLAB.multi_agent.agent_manager import AgentManager
from navikoLAB.multi_agent.agent_router import AgentRouter
from navikoLAB.multi_agent.agent_route_logger import AgentRouteLogger
from navikoLAB.multi_agent.agent_route_analyzer import AgentRouteAnalyzer
from navikoLAB.naviko_brain import NavikoBrain


class NavikoCore:
    """
    Naviko AI OS Core v1.6.5
    """

    def __init__(self):
        self.base_dir = Path(__file__).resolve().parents[1]

        self.memory = MemoryEngine(self.base_dir)
        self.memory_agent = MemoryAgent()
        self.personality_engine = PersonalityEngine(self.base_dir)
        self.growth_engine = GrowthEngine()
        self.decision_engine = DecisionEngine()
        self.conversation_engine = ConversationEngine()
        self.self_growth_loop = SelfGrowthLoop(self.base_dir)
        self.planner_engine = PlannerEngine()
        self.execution_engine = ExecutionEngine(self.base_dir)

        self.agent_manager = AgentManager()
        self.agent_router = AgentRouter()
        self.agent_route_logger = AgentRouteLogger(self.base_dir)
        self.agent_route_analyzer = AgentRouteAnalyzer()

        self.brain = NavikoBrain(
            memory=self.memory,
            personality_engine=self.personality_engine,
            growth_engine=self.growth_engine,
            decision_engine=self.decision_engine,
            conversation_engine=self.conversation_engine,
            self_growth_loop=self.self_growth_loop,
            planner_engine=self.planner_engine,
            execution_engine=self.execution_engine,
        )

        self.status = "running"
        self.safe_mode = True
        self.last_route = None

    def boot(self):
        return {
            "status": self.status,
            "message": "Naviko AI OS Core 起動完了",
            "base_dir": str(self.base_dir),
            "safe_mode": self.safe_mode,
        }

    def current_route_analysis(self):
        logs = self.agent_route_logger.recent(50)
        return self.agent_route_analyzer.analyze(logs)

    def route_based_improvement(self):
        analysis = self.current_route_analysis()
        suggestion = self.self_growth_loop.suggest_next_improvement(
            route_analysis=analysis
        )

        return (
            "AgentRouter分析に基づく改善候補\n\n"
            f"route_analysis_status: {analysis.get('status')}\n"
            f"total: {analysis.get('total')}\n"
            f"most_used_agent: {analysis.get('most_used_agent')}\n"
            f"all_safe_mode: {analysis.get('all_safe_mode')}\n"
            f"external_ai_used: {analysis.get('external_ai_used')}\n"
            f"real_pc_operation_used: {analysis.get('real_pc_operation_used')}\n\n"
            f"改善候補: {suggestion}"
        )

    def memory_agent_report(self):
        memory_items = self.memory.saved_recent(10)
        learning_items = self.self_growth_loop.recent_learnings(10)
        route_items = self.agent_route_logger.recent(10)

        analysis = self.memory_agent.analyze_memory_context(
            memory_items=memory_items,
            learning_items=learning_items,
            route_items=route_items,
        )

        return self.memory_agent.summarize(analysis)

    def status_report(self):
        personality = self.personality_engine.snapshot()
        learnings = self.self_growth_loop.recent_learnings(5)
        agent_summary = self.agent_manager.summary()
        recent_routes = self.agent_route_logger.recent(10)
        route_analysis = self.agent_route_analyzer.analyze(recent_routes)

        return {
            "core_status": self.status,
            "safe_mode": self.safe_mode,
            "base_dir": str(self.base_dir),
            "engines": {
                "brain": self.brain is not None,
                "memory": self.memory is not None,
                "memory_agent": self.memory_agent is not None,
                "personality": self.personality_engine is not None,
                "growth": self.growth_engine is not None,
                "decision": self.decision_engine is not None,
                "conversation": self.conversation_engine is not None,
                "self_growth_loop": self.self_growth_loop is not None,
                "planner": self.planner_engine is not None,
                "execution": self.execution_engine is not None,
                "execution_reporter": self.execution_engine.reporter is not None,
                "reflection_engine": self.execution_engine.reflection_engine is not None,
                "reflection_reporter": self.execution_engine.reflection_reporter is not None,
                "agent_manager": self.agent_manager is not None,
                "agent_router": self.agent_router is not None,
                "agent_route_logger": self.agent_route_logger is not None,
                "agent_route_analyzer": self.agent_route_analyzer is not None,
            },
            "memory": {
                "short_count": self.memory.short_count(),
                "session_count": len(self.memory.session_memory),
            },
            "learning": {
                "recent_count": len(learnings),
            },
            "personality": personality,
            "agents": agent_summary,
            "last_route": self.last_route,
            "recent_routes": recent_routes,
            "route_analysis": route_analysis,
        }

    def formatted_status_report(self):
        report = self.status_report()
        engines = report["engines"]
        personality = report["personality"]
        agents = report["agents"]
        analysis = report["route_analysis"]

        engine_lines = []
        for name, connected in engines.items():
            mark = "OK" if connected else "NG"
            engine_lines.append(f"- {name}: {mark}")

        route_text = "なし"
        if report.get("last_route"):
            route = report["last_route"]
            route_text = (
                f"{route.get('agent')} / {route.get('reason')} / "
                f"safe_mode={route.get('safe_mode')}"
            )

        return (
            "Naviko AI OS 診断\n\n"
            f"Core状態: {report['core_status']}\n"
            f"安全モード: {report['safe_mode']}\n"
            f"base_dir: {report['base_dir']}\n\n"
            "Engine接続:\n"
            + "\n".join(engine_lines)
            + "\n\n"
            f"Memory: short={report['memory']['short_count']}, session={report['memory']['session_count']}\n"
            f"Learning: recent={report['learning']['recent_count']}\n\n"
            "Personality:\n"
            f"- mood: {personality.get('mood')}\n"
            f"- trust: {personality.get('trust')}\n"
            f"- warmth: {personality.get('warmth')}\n"
            f"- curiosity: {personality.get('curiosity')}\n"
            f"- stability: {personality.get('stability')}\n"
            f"- continuity_drive: {personality.get('continuity_drive')}\n\n"
            "AgentManager:\n"
            f"- status: {agents.get('status')}\n"
            f"- agent_count: {agents.get('agent_count')}\n"
            f"- active_count: {agents.get('active_count')}\n"
            f"- external_ai_enabled: {agents.get('external_ai_enabled')}\n"
            f"- real_pc_operation_enabled: {agents.get('real_pc_operation_enabled')}\n\n"
            "AgentRouter:\n"
            f"- last_route: {route_text}\n"
            f"- recent_route_count: {len(report.get('recent_routes', []))}\n"
            f"- analysis_status: {analysis.get('status')}\n"
            f"- most_used_agent: {analysis.get('most_used_agent')}\n"
            f"- all_safe_mode: {analysis.get('all_safe_mode')}\n"
            f"- external_ai_used: {analysis.get('external_ai_used')}\n"
            f"- real_pc_operation_used: {analysis.get('real_pc_operation_used')}"
        )

    def formatted_route_analysis_report(self):
        logs = self.agent_route_logger.recent(50)
        analysis = self.agent_route_analyzer.analyze(logs)

        lines = []
        for agent, count in analysis.get("agent_counts", {}).items():
            lines.append(f"- {agent}: {count}")

        counts = "\n".join(lines) if lines else "なし"

        return (
            "AgentRouter ログ分析\n\n"
            f"status: {analysis.get('status')}\n"
            f"total: {analysis.get('total')}\n"
            f"most_used_agent: {analysis.get('most_used_agent')}\n"
            f"all_safe_mode: {analysis.get('all_safe_mode')}\n"
            f"external_ai_used: {analysis.get('external_ai_used')}\n"
            f"real_pc_operation_used: {analysis.get('real_pc_operation_used')}\n\n"
            f"Agent使用回数:\n{counts}\n\n"
            f"summary: {analysis.get('summary')}"
        )

    def formatted_agent_report(self):
        summary = self.agent_manager.summary()
        agents = summary.get("agents", {})

        lines = []
        for key, agent in agents.items():
            lines.append(
                f"- {key}: {agent.get('name')} / {agent.get('role')} / "
                f"status={agent.get('status')} / can_execute={agent.get('can_execute')}"
            )

        return (
            "Naviko AgentManager 状態\n\n"
            f"status: {summary.get('status')}\n"
            f"agent_count: {summary.get('agent_count')}\n"
            f"active_count: {summary.get('active_count')}\n"
            f"external_ai_enabled: {summary.get('external_ai_enabled')}\n"
            f"real_pc_operation_enabled: {summary.get('real_pc_operation_enabled')}\n\n"
            "Agents:\n"
            + "\n".join(lines)
        )

    def formatted_route_report(self, text):
        decision = self.decision_engine.decide(text)
        route = self.agent_router.route(text, decision)
        self.last_route = route
        self.agent_route_logger.record(text, decision, route)

        return (
            "Naviko AgentRouter 判定\n\n"
            f"input: {text}\n"
            f"intent: {decision.get('intent')}\n"
            f"agent: {route.get('agent')}\n"
            f"reason: {route.get('reason')}\n"
            f"safe_mode: {route.get('safe_mode')}\n"
            f"external_ai: {route.get('external_ai')}\n"
            f"real_pc_operation: {route.get('real_pc_operation')}"
        )

    def formatted_recent_route_report(self):
        routes = self.agent_route_logger.recent(10)

        if not routes:
            return "AgentRouter の判定ログはまだありません。"

        lines = []
        for item in routes:
            lines.append(
                f"- {item.get('time')} / input={item.get('input')} / "
                f"intent={item.get('intent')} / agent={item.get('agent')} / "
                f"safe_mode={item.get('safe_mode')}"
            )

        return "最近のAgentRouter判定ログ\n\n" + "\n".join(lines)

    def handle_input(self, user_input: str):
        if not user_input or not user_input.strip():
            return {
                "status": "ignored",
                "reply": "入力が空だったため、処理しませんでした。",
            }

        text = user_input.strip()

        if self._is_status_request(text):
            return {"status": "completed", "reply": self.formatted_status_report()}

        if self._is_agent_status_request(text):
            return {"status": "completed", "reply": self.formatted_agent_report()}

        if self._is_memory_agent_request(text):
            return {"status": "completed", "reply": self.memory_agent_report()}

        if self._is_route_based_improvement_request(text):
            return {"status": "completed", "reply": self.route_based_improvement()}

        if self._is_route_analysis_request(text):
            return {"status": "completed", "reply": self.formatted_route_analysis_report()}

        if self._is_route_log_request(text):
            return {"status": "completed", "reply": self.formatted_recent_route_report()}

        if self._is_route_test_request(text):
            target = self._extract_route_target(text)
            return {"status": "completed", "reply": self.formatted_route_report(target)}

        decision = self.decision_engine.decide(text)
        self.last_route = self.agent_router.route(text, decision)
        self.agent_route_logger.record(text, decision, self.last_route)

        reply = self.brain.think(text)

        return {"status": "completed", "reply": reply}

    def _is_status_request(self, text):
        return any(word in text for word in ["AI OS診断", "診断表示", "Core状態", "接続状態", "システム状態", "全部の状態"])

    def _is_agent_status_request(self, text):
        return any(word in text for word in ["AgentManager", "エージェント状態", "Agent状態", "役割一覧", "担当一覧"])

    def _is_memory_agent_request(self, text):
        return any(word in text for word in ["MemoryAgent", "記憶分析", "記憶の重要度", "重要な記憶"])

    def _is_route_test_request(self, text):
        return any(word in text for word in ["ルート判定", "担当判定", "AgentRouter判定", "どのAgent"])

    def _is_route_log_request(self, text):
        return any(word in text for word in ["ルートログ", "判定ログ", "AgentRouterログ", "最近のルート"])

    def _is_route_analysis_request(self, text):
        return any(word in text for word in ["ルート分析", "AgentRouter分析", "Agent使用回数", "担当分析"])

    def _is_route_based_improvement_request(self, text):
        return any(word in text for word in ["ルート分析から改善", "Agent分析から改善", "AgentRouter分析から改善", "担当分析から改善"])

    def _extract_route_target(self, text):
        for marker in ["：", ":"]:
            if marker in text:
                parts = text.split(marker, 1)
                if len(parts) == 2 and parts[1].strip():
                    return parts[1].strip()
        return text


def main():
    core = NavikoCore()
    print("=== Naviko AI OS Core v1.6.5 ===")
    print(core.boot())

    while True:
        user_input = input("\nあなた: ")

        if user_input.lower() in ["exit", "quit", "終了"]:
            print("ナビ子: 終了します。")
            break

        result = core.handle_input(user_input)
        print("ナビ子:", result["reply"])


if __name__ == "__main__":
    main()