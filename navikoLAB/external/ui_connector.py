class UIConnector:

    def render(self, state: dict):

        print("\n[UI STATE]")
        for k, v in state.items():
            print(f"{k}: {v}")

        return {"status": "rendered"}