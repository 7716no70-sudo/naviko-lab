class NextPhaseGenerator:

    def generate(self, scored):

        safe_phases = []

        for item, risk in scored:

            if risk <= 2:
                safe_phases.append(item)

        return safe_phases