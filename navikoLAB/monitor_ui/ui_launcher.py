from navikoLAB.monitor_ui.dashboard import Dashboard


class UILauncher:

    def __init__(self):

        self.dashboard = Dashboard()

    def run(self, state):

        self.dashboard.update(state)