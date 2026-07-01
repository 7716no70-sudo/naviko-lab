class ExternalRouter:

    def route(self, task_type):

        if task_type == "browser":
            return "browser_controller"

        if task_type == "gui":
            return "gui_controller"

        if task_type == "app":
            return "app_controller"

        if task_type == "web":
            return "web_scraper"

        return "noop"