from navikoLAB.cognition.cognition_core import CognitionCore


class CognitionBridge:

    def __init__(self, daemon):
        self.cognition = CognitionCore()
        self.daemon = daemon   # ★外から受け取る
        self.history = []

    def step(self):

        snapshot = self.daemon.loop.scanner.scan()
        result = self.cognition.run(snapshot, self.history)

        self.history.append(snapshot.get("decision", "UNKNOWN"))

        return result