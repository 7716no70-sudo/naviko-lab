class ToolRouter:

    def route(self, command: str):

        command = command.lower()

        if "file" in command:
            return "file_tool"

        if "ui" in command:
            return "ui_tool"

        if "api" in command:
            return "api_tool"

        return "noop"