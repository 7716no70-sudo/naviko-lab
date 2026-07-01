import os
import subprocess


class SystemExecutor:

    def run_command(self, command):

        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        return {
            "stdout": result.stdout,
            "stderr": result.stderr
        }