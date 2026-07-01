class AgentRegistry:

    def __init__(self):

        self.agents = {
            "cognition": True,
            "evolution": True,
            "selfmodify": True
        }

    def is_active(self, name):
        return self.agents.get(name, False)