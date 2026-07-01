from navikoLAB.ai_network.agents.planner_agent import PlannerAgent
from navikoLAB.ai_network.agents.research_agent import ResearchAgent
from navikoLAB.ai_network.agents.execution_agent import ExecutionAgent
from navikoLAB.ai_network.agents.reflection_agent import ReflectionAgent
from navikoLAB.ai_network.message_bus import MessageBus


class NetworkOrchestrator:

    def __init__(self):

        self.bus = MessageBus()

        self.planner = PlannerAgent()
        self.research = ResearchAgent()
        self.execution = ExecutionAgent()
        self.reflection = ReflectionAgent()

    def step(self, state):

        plan = self.planner.run(state)
        insights = self.research.run(state)
        execution = self.execution.run(plan)
        reflection = self.reflection.run(state)

        self.bus.send("planner", "execution", plan)
        self.bus.send("research", "planner", insights)
        self.bus.send("reflection", "planner", reflection)

        return {
            "plan": plan,
            "insights": insights,
            "execution": execution,
            "reflection": reflection
        }