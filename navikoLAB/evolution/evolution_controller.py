# evolution_controller.py


class EvolutionController:

    def decide(self, is_repetition):

        if is_repetition:
            return "FORCE_EVOLUTION"

        return "NORMAL"