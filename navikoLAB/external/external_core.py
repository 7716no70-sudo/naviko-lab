from navikoLAB.external.external_router import ExternalRouter
from navikoLAB.external.browser_controller import BrowserController
from navikoLAB.external.gui_controller import GUIController
from navikoLAB.external.app_controller import AppController
from navikoLAB.external.web_scraper import WebScraper


class ExternalCore:

    def __init__(self):

        self.router = ExternalRouter()

        self.browser = BrowserController()

        self.gui = GUIController()
        self.app = AppController()
        self.web = WebScraper()

        self.last_browser_url = None

    def execute(self, task_type, payload):

        if task_type == "browser":

            url = payload.get("url")

            if not url:
                return {"status": "error", "reason": "no url"}

            # 同じURLはスキップ
            if self.last_browser_url == url:
                return {"status": "skipped", "reason": "same url"}

            self.last_browser_url = url

            return self.browser.open(url)


        if task_type == "gui":
            return self.gui.click(
                payload.get("x"),
                payload.get("y")
            )


        if task_type == "app":
            return self.app.run(payload.get("name"))


        if task_type == "web":
            return self.web.search(payload.get("query"))


        return {"status": "noop"}