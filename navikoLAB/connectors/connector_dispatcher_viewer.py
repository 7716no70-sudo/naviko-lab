from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TARGET_FILE = ROOT / "navikoLAB" / "connectors" / "connector_dispatcher.py"


KEYWORDS = [
    "from ",
    "import ",
    "class ConnectorDispatcher",
    "def __init__",
    "def dispatch",
    "def execute",
    "chatgpt",
    "app_operator",
]


def print_file_header(lines, max_lines=20):
    print("=== connector_dispatcher.py 先頭部分 ===")

    for i, line in enumerate(lines[:max_lines], start=1):
        print(f"{i}: {line}")


def print_keyword_context(lines, keyword, before=8, after=12):
    found = False

    for index, line in enumerate(lines, start=1):
        if keyword in line:
            found = True
            start = max(1, index - before)
            end = min(len(lines), index + after)

            print("")
            print(f"=== keyword: {keyword} / line {index} ===")

            for i in range(start, end + 1):
                prefix = ">>" if i == index else "  "
                print(f"{prefix} {i}: {lines[i - 1]}")

    if not found:
        print("")
        print(f"=== keyword: {keyword} ===")
        print("見つかりませんでした。")


def main():
    print("=== ConnectorDispatcher Viewer ===")
    print(f"対象: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print("対象ファイルが見つかりません。")
        return

    lines = TARGET_FILE.read_text(
        encoding="utf-8",
        errors="ignore"
    ).splitlines()

    print(f"総行数: {len(lines)}")
    print("")

    print_file_header(lines)

    for keyword in KEYWORDS:
        print_keyword_context(lines, keyword)


if __name__ == "__main__":
    main()