from pathlib import Path

try:
    # naviko.py から読み込む場合
    from navikoLAB.core.mission_manager import MissionManager
except ImportError:
    # core フォルダで単体テストする場合
    from mission_manager import MissionManager


class MissionBridge:
    """
    AutonomousCore と MissionManager の橋渡しクラス
    """

    def __init__(self, root_dir):

        self.root_dir = Path(root_dir)

        self.mission_manager = MissionManager(
            self.root_dir
        )

    def create_from_goal(
        self,
        goal,
        description=""
    ):

        mission = self.mission_manager.create_mission(
            goal,
            description
        )

        self.mission_manager.generate_tasks_by_goal(
            mission["id"]
        )

        self.mission_manager.update_status(
            mission["id"],
            "planning"
        )

        return mission

    def get_resume(self):

        return self.mission_manager.get_resume_mission()

    def start_build(self, mission_id):

        return self.mission_manager.update_status(
            mission_id,
            "building"
        )

    def start_reflection(self, mission_id):

        return self.mission_manager.update_status(
            mission_id,
            "reflection"
        )

    def start_improvement(self, mission_id):

        return self.mission_manager.update_status(
            mission_id,
            "improving"
        )

    def complete(self, mission_id):

        return self.mission_manager.complete_mission(
            mission_id
        )

    def diagnose(self):

        return self.mission_manager.diagnose()