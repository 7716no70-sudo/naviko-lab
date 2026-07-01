class ExecutionRouter:

    def route(self, task_type):

        if task_type == "file":
            return "file_executor"

        if task_type == "system":
            return "system_executor"

        if task_type == "task":
            return "task_executor"

        return "noop"