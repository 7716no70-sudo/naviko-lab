# forced_evolution_gate.py


class ForcedEvolutionGate:

    def open(self, should_evolve):

        if should_evolve:
            return "FORCE_EVOLUTION"

        return "NORMAL"