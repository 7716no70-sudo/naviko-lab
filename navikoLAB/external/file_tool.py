class FileTool:

    def write(self, path: str, content: str):

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return {"status": "written", "path": path}

    def read(self, path: str):

        with open(path, "r", encoding="utf-8") as f:
            return f.read()