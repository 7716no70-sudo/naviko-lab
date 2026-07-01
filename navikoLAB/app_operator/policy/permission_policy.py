class PermissionPolicy:
    LEVELS = {
        1: "auto",
        2: "simple_approval",
        3: "normal_approval",
        4: "strict_approval",
    }

    LEVEL1_ACTIONS = {
        "knowledge整理",
        "log整理",
        "report_generate",
        "window_inspect",
    }

    LEVEL2_ACTIONS = {
        "browser_search",
        "open_application",
        "explorer_open",
    }

    LEVEL3_ACTIONS = {
        "mouse_click",
        "keyboard_input",
        "ocr_read",
    }

    LEVEL4_ACTIONS = {
        "delete_file",
        "change_settings",
        "system_operation",
        "shutdown",
        "restart",
        "install_software",
        "payment",
        "purchase",
        "send_email",
    }

    def classify(self, action):
        if action in self.LEVEL1_ACTIONS:
            level = 1
        elif action in self.LEVEL2_ACTIONS:
            level = 2
        elif action in self.LEVEL3_ACTIONS:
            level = 3
        elif action in self.LEVEL4_ACTIONS:
            level = 4
        else:
            level = 3

        return {
            "action": action,
            "permission_level": level,
            "permission_type": self.LEVELS[level],
            "requires_approval": level >= 2,
            "requires_strict_approval": level >= 4,
            "dry_run": True,
            "external_operation": False,
        }