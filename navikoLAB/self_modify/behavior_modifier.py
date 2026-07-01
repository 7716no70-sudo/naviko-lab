# behavior_modifier.py


class BehaviorModifier:

    def modify(self, rules):

        behavior = {
            "loop_speed": 1,
            "risk_threshold": 2
        }

        if "increase_autonomy" in rules:
            behavior["loop_speed"] = 0.5

        if "strengthen_stability" in rules:
            behavior["risk_threshold"] = 1

        if "enhance_observation" in rules:
            behavior["logging"] = "verbose"

        return behavior