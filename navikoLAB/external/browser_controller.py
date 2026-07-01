from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BrowserController:

    def __init__(self):

        self.driver = None
        self.current_url = None

    def _ensure_driver(self):

        if self.driver is None:
            options = Options()

            # ★重要：勝手に閉じるの防止
            options.add_experimental_option("detach", True)

            self.driver = webdriver.Chrome(options=options)

    def open(self, url):

        self._ensure_driver()

        if not url:
            return {"status": "error", "reason": "no url"}

        # ★同じURLなら再読み込みしない
        if self.current_url == url:
            return {"status": "skipped", "reason": "same url"}

        self.current_url = url

        try:
            self.driver.get(url)

        except Exception as e:
            # ★死んでたら復旧
            self.driver = None
            self._ensure_driver()
            self.driver.get(url)

        return {
            "status": "opened",
            "url": url
        }

    def close(self):

        if self.driver:
            self.driver.quit()
            self.driver = None
            self.current_url = None