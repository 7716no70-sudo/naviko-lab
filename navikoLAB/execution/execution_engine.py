class ExecutionEngine:

    def __init__(self, external_core):
        self.external = external_core
        self.log = []

    def execute(self, task):

        task_type = task.get("type")

        # ■ ファイル系は内部処理
        if task_type == "file":
            result = {
                "status": "written",
                "path": task.get("path"),
                "content": task.get("content")
            }

        # ■ 外部系はExternalCoreへ
        elif task_type in ["browser", "gui", "web", "app"]:
            result = self.external.execute(task_type, task)

        # ■ 未知タスク
        else:
            result = {"status": "noop", "reason": "unknown_task"}

        self.log.append({
            "task": task,
            "result": result
        })

        return result