import random


class EvolutionBalancer:

    def __init__(self):

        self.force_rate = 0.3   # 30%発火
        self.normal_rate = 0.7   # 70%安定

    def balance(self, action):

        # FORCE_EVOLUTIONが来ても確率で抑制
        if action == "FORCE_EVOLUTION":

            if random.random() < self.force_rate:
                return "FORCE_EVOLUTION"
            else:
                return "NORMAL"

        return action