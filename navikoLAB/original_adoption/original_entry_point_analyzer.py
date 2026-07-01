from pathlib import Path


class OriginalEntryPointAnalyzer:

    def __init__(self):

        self.original_file = (
            Path(__file__).resolve().parents[2]
            / "naviko.py"
        )

    def analyze(self):

        source = self.original_file.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        lines = source.splitlines()

        import_line = None
        main_line = None
        tk_line = None
        process_line = None
        custom_chat_line = None

        for i, line in enumerate(lines, start=1):

            stripped = line.strip()

            if import_line is None and (
                stripped.startswith("import ")
                or stripped.startswith("from ")
            ):
                import_line = i

            if process_line is None and "def process_user_request" in stripped:
                process_line = i

            if custom_chat_line is None and "def open_custom_chat_window" in stripped:
                custom_chat_line = i

            if tk_line is None and (
                ".mainloop(" in stripped
                or "mainloop()" in stripped
            ):
                tk_line = i

            if stripped == 'if __name__ == "__main__":':
                main_line = i

        if process_line:
            injection_target = "process_user_request"
            injection_line = process_line
        elif custom_chat_line:
            injection_target = "open_custom_chat_window"
            injection_line = custom_chat_line
        elif main_line:
            injection_target = "__main__"
            injection_line = main_line
        else:
            injection_target = "manual_review_required"
            injection_line = None

        return {

            "status": "completed",

            "original_found": self.original_file.exists(),

            "import_line": import_line,

            "main_line": main_line,

            "tk_mainloop_line": tk_line,

            "process_user_request_line": process_line,

            "custom_chat_window_line": custom_chat_line,

            "recommended_target": injection_target,

            "recommended_line": injection_line,

            "ready_for_locator": injection_line is not None,

            "dry_run": True,

            "external_operation": False,

            "real_gui_operation": False,

            "original_write": False

        }