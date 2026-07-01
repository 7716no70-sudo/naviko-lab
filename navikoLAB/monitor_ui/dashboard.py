# dashboard.py

from navikoLAB.monitor_ui.metrics_engine import MetricsEngine
from navikoLAB.monitor_ui.log_stream import LogStream
from navikoLAB.monitor_ui.live_view import LiveView


class Dashboard:

    def __init__(self):

        self.metrics = MetricsEngine()
        self.logger = LogStream()
        self.view = LiveView()

    def update(self, state):

        m = self.metrics.build(state)

        self.logger.stream(m)
        self.view.render(m)

        return m