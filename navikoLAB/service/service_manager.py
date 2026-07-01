# service_manager.py

import os


class ServiceManager:

    FLAG_FILE = "naviko_service.flag"

    def enable(self):
        with open(self.FLAG_FILE, "w") as f:
            f.write("enabled")

    def disable(self):
        if os.path.exists(self.FLAG_FILE):
            os.remove(self.FLAG_FILE)

    def is_enabled(self):
        return os.path.exists(self.FLAG_FILE)