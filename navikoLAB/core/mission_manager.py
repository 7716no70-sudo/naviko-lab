import json
from pathlib import Path
from datetime import datetime
from uuid import uuid4
from navikoLAB.core.mission_capability_bridge import MissionCapabilityBridge


class MissionManager:
    """
    長期ミッション管理クラス

    ・ミッション作成
    ・目的別タスク分解
    ・タスク追加
    ・タスク完了
    ・進捗率自動計算
    ・途中保存
    ・途中再開
    ・履歴保存
    """

    def __init__(self, root_dir):

        self.root_dir = Path(root_dir)

        self.mission_dir = self.root_dir / "missions"
        self.mission_dir.mkdir(exist_ok=True)

        self.mission_file = self.mission_dir / "missions.json"
        self.history_file = self.mission_dir / "mission_history.json"

        self.missions = self.load()
        self.repair_old_missions()
        self.capability_bridge = MissionCapabilityBridge()
        

    def load(self):

        if self.mission_file.exists():
            try:
                return json.loads(
                    self.mission_file.read_text(
                        encoding="utf-8"
                    )
                )
            except Exception:
                pass

        return []

    def repair_old_missions(self):

        changed = False

        for mission in self.missions:

            if "goal_type" not in mission:
                mission["goal_type"] = self.detect_goal_type(
                    mission.get("title", "") + " " + mission.get("description", "")
                )
                changed = True

            if "updated_at" not in mission:
                mission["updated_at"] = mission.get(
                    "created_at",
                    datetime.now().isoformat()
                )
                changed = True

            if "tasks" not in mission:
                mission["tasks"] = []
                changed = True

        if changed:
            self.save()

            self.save_history(
                "repair_old_missions",
                None,
                {
                    "message": "old mission data repaired"
                }
            )


    def save(self):

        self.mission_file.write_text(
            json.dumps(
                self.missions,
                ensure_ascii=False,
                indent=4
            ),
            encoding="utf-8"
        )

    def save_history(self, action, mission_id=None, detail=None):

        history = []

        if self.history_file.exists():
            try:
                history = json.loads(
                    self.history_file.read_text(
                        encoding="utf-8"
                    )
                )
            except Exception:
                history = []

        record = {
            "time": datetime.now().isoformat(),
            "action": action,
            "mission_id": mission_id,
            "detail": detail or {}
        }

        history.append(record)

        self.history_file.write_text(
            json.dumps(
                history,
                ensure_ascii=False,
                indent=4
            ),
            encoding="utf-8"
        )

    def detect_goal_type(self, text):

        text = text.lower()

        if "ゲーム" in text or "game" in text:
            return "game"

        if "動画" in text or "youtube" in text or "video" in text:
            return "video"

        if "画像" in text or "イラスト" in text or "image" in text:
            return "image"

        if "ai" in text or "人工知能" in text or "エージェント" in text:
            return "ai_tool"

        if "アプリ" in text or "app" in text or "ツール" in text:
            return "app"

        return "general"

    def get_lifecycle_states(self):

        return [
            "planning",
            "waiting_agent",
            "building",
            "reflection",
            "improving",
            "active",
            "paused",
            "completed",
            "failed"
        ]


    def create_mission(self, title, description=""):

        goal_type = self.detect_goal_type(
            title + " " + description
        )

        mission = {

            "id": str(uuid4()),

            "title": title,

            "description": description,

            "goal_type": goal_type,

            "created_at": datetime.now().isoformat(),

            "updated_at": datetime.now().isoformat(),

            "status": "active",

            "progress": 0,

            "tasks": []

        }

        mission = self.capability_bridge.attach_capability_result(mission)

        self.missions.append(mission)

        self.save()

        self.save_history(
            "create_mission",
            mission["id"],
            {
                "title": title,
                "description": description,
                "goal_type": goal_type,
                "required_capabilities": mission.get("required_capabilities", []),
                "missing_capabilities": mission.get("missing_capabilities", []),
                "recommended_agents": mission.get("recommended_agents", [])
            }
        )

        return mission

    def list_missions(self):

        return self.missions

    def get_mission(self, mission_id):

        for mission in self.missions:

            if mission["id"] == mission_id:
                return mission

        return None

    def add_task(self, mission_id, title, description=""):

        mission = self.get_mission(mission_id)

        if mission is None:
            return None

        task = {
            "id": str(uuid4()),
            "title": title,
            "description": description,
            "status": "todo",
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }

        mission["tasks"].append(task)

        mission["updated_at"] = datetime.now().isoformat()

        self.recalculate_progress(mission)

        self.save()

        self.save_history(
            "add_task",
            mission_id,
            {
                "task_id": task["id"],
                "title": title
            }
        )

        return task

    def generate_tasks_by_goal(self, mission_id):

        mission = self.get_mission(mission_id)

        if mission is None:
            return []

        goal_type = mission.get("goal_type", "general")

        task_map = {

            "app": [
                "アプリの目的を整理する",
                "必要な画面と機能を洗い出す",
                "データ保存方式を決める",
                "最小構成のアプリを作成する",
                "操作テストを行う",
                "不足機能を追加する",
                "READMEと使い方を整える",
                "完成診断を行う"
            ],

            "game": [
                "ゲームのジャンルを決める",
                "プレイヤー操作を設計する",
                "ルールと勝敗条件を決める",
                "画面構成を作る",
                "最小プレイ可能版を作成する",
                "難易度と演出を調整する",
                "テストプレイを行う",
                "完成版として整理する"
            ],

            "video": [
                "動画の目的を整理する",
                "視聴者と用途を決める",
                "構成案を作る",
                "台本を作成する",
                "素材リストを作る",
                "編集手順を分解する",
                "完成動画を評価する",
                "改善点を反映する"
            ],

            "image": [
                "画像の用途を整理する",
                "雰囲気とスタイルを決める",
                "必要な構図を考える",
                "生成プロンプトを作成する",
                "候補画像を評価する",
                "修正指示を作る",
                "完成画像を選定する"
            ],

            "ai_tool": [
                "AIツールの目的を整理する",
                "必要なAI能力を洗い出す",
                "入力と出力を定義する",
                "利用するエージェントを決める",
                "最小機能を実装する",
                "動作ログを確認する",
                "Reflectionで評価する",
                "改善要求を生成する"
            ],

            "general": [
                "目的を整理する",
                "必要な作業を洗い出す",
                "作業工程を分解する",
                "最初の成果物を作成する",
                "成果物を自己評価する",
                "改善点を反映する",
                "完成状態を確認する"
            ]
        }

        created_tasks = []

        for task_title in task_map.get(goal_type, task_map["general"]):

            created_task = self.add_task(
                mission_id,
                task_title
            )

            if created_task:
                created_tasks.append(created_task)

        self.save_history(
            "generate_tasks_by_goal",
            mission_id,
            {
                "goal_type": goal_type,
                "task_count": len(created_tasks)
            }
        )

        return created_tasks

    def generate_basic_tasks(self, mission_id):

        return self.generate_tasks_by_goal(mission_id)

    def complete_task(self, mission_id, task_id):

        mission = self.get_mission(mission_id)

        if mission is None:
            return False

        for task in mission["tasks"]:

            if task["id"] == task_id:

                task["status"] = "done"
                task["completed_at"] = datetime.now().isoformat()

                mission["updated_at"] = datetime.now().isoformat()

                self.recalculate_progress(mission)

                self.save()

                self.save_history(
                    "complete_task",
                    mission_id,
                    {
                        "task_id": task_id
                    }
                )

                return True

        return False

    def recalculate_progress(self, mission):

        tasks = mission.get("tasks", [])

        if not tasks:
            mission["progress"] = 0
            mission["status"] = "active"
            return 0

        done_count = 0

        for task in tasks:
            if task.get("status") == "done":
                done_count += 1

        progress = int(
            done_count / len(tasks) * 100
        )

        mission["progress"] = progress

        if progress >= 100:
            mission["status"] = "completed"
        elif mission.get("status") not in ["paused", "failed"]:
            mission["status"] = "active"

        return progress

    def update_status(self, mission_id, status):

        if status not in self.get_lifecycle_states():
            return False

        mission = self.get_mission(mission_id)

        if mission is None:
            return False

        mission["status"] = status
        mission["updated_at"] = datetime.now().isoformat()

        self.save()

        self.save_history(
            "update_status",
            mission_id,
            {
                "status": status
            }
        )

        return True

    def pause_mission(self, mission_id):

        return self.update_status(
            mission_id,
            "paused"
        )

    def fail_mission(self, mission_id):

        return self.update_status(
            mission_id,
            "failed"
        )

    def complete_mission(self, mission_id):

        mission = self.get_mission(mission_id)

        if mission is None:
            return False

        mission["progress"] = 100

        return self.update_status(
            mission_id,
            "completed"
        )


    def update_progress(self, mission_id, progress):

        mission = self.get_mission(mission_id)

        if mission is None:
            return False

        mission["progress"] = max(
            0,
            min(100, progress)
        )

        mission["updated_at"] = datetime.now().isoformat()

        if mission["progress"] >= 100:
            mission["status"] = "completed"
        else:
            mission["status"] = "active"

        self.save()

        self.save_history(
            "update_progress",
            mission_id,
            {
                "progress": mission["progress"]
            }
        )

        return True

    def get_resume_mission(self):

        resumable_statuses = [
            "planning",
            "waiting_agent",
            "building",
            "reflection",
            "improving",
            "active",
            "paused"
        ]

        resume_missions = []

        for mission in self.missions:

            if mission.get("status") in resumable_statuses:
                resume_missions.append(mission)

        if not resume_missions:
            return None

        resume_missions.sort(
            key=lambda mission: mission.get("updated_at", ""),
            reverse=True
        )

        return resume_missions[0]

    def diagnose(self):

        active_count = 0
        completed_count = 0
        task_count = 0
        done_task_count = 0

        goal_type_count = {}
        status_count = {}

        for mission in self.missions:

            if mission.get("status") == "completed":
                completed_count += 1
            else:
                active_count += 1

            status = mission.get("status", "unknown")

            status_count[status] = status_count.get(
                status,
                0
            ) + 1



            goal_type = mission.get("goal_type", "unknown")

            goal_type_count[goal_type] = goal_type_count.get(
                goal_type,
                0
            ) + 1

            for task in mission.get("tasks", []):
                task_count += 1

                if task.get("status") == "done":
                    done_task_count += 1

        return {
            "mission_count": len(self.missions),
            "active_count": active_count,
            "completed_count": completed_count,
            "task_count": task_count,
            "done_task_count": done_task_count,
            "goal_type_count": goal_type_count,
            "status_count": status_count,
            "mission_file": str(self.mission_file),
            "history_file": str(self.history_file)
        }