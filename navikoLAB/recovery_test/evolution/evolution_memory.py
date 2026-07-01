# evolution_memory.py


class EvolutionMemory:

    def __init__(self):
        self.history = []

    def record(self, state):
        self.history.append(state)

    def get(self):
        return self.history