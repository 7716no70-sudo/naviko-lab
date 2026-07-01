from pathlib import Path

from navikoLAB.original_adoption.lab_feature_adoption_planner import LabFeatureAdoptionPlanner


def main():
    root_dir = Path(__file__).resolve().parents[1]

    planner = LabFeatureAdoptionPlanner(
        root_dir
    )

    plan = planner.create_plan()

    print(planner.format_plan(plan))


if __name__ == "__main__":
    main()