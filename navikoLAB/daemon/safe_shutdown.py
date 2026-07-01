# safe_shutdown.py

import os
import json

SHUTDOWN_FLAG = "daemon_shutdown.json"


def request_shutdown():
    with open(SHUTDOWN_FLAG, "w") as f:
        json.dump({"shutdown": True}, f)


def check_shutdown():
    if not os.path.exists(SHUTDOWN_FLAG):
        return False

    with open(SHUTDOWN_FLAG, "r") as f:
        data = json.load(f)

    return data.get("shutdown", False)