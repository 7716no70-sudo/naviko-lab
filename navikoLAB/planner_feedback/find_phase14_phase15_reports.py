from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "navikoLAB"

KEYWORDS = [
    "phase14",
    "feedback_loop",
    "phase15",
    "planner_self",
    "planner_improvement",
    "completion",
]

def main():
    print("=== Phase14 / Phase15 Report Finder ===")

    matches = []
    for path in BASE.rglob("*.json"):
        name = path.name.lower()
        text_path = str(path).lower()

        if any(k in name or k in text_path for k in KEYWORDS):
            matches.append(path)

    for path in matches:
        print(path)

    print(f"候補数: {len(matches)}")

if __name__ == "__main__":
    main()