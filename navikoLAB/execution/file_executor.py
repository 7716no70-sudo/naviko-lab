class FileExecutor:

    def write(self, path, content):

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return {"status": "written", "path": path}

    def read(self, path):

        with open(path, "r", encoding="utf-8") as f:
            return f.read()