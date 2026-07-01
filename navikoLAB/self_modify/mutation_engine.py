# mutation_engine.py


class MutationEngine:

    def mutate(self, behavior):

        mutated = behavior.copy()

        # 軽微進化
        mutated["mutation_level"] = mutated.get("mutation_level", 0) + 1

        return mutated