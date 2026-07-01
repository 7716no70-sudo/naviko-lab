from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LAB_ROOT = ROOT / "navikoLAB"


SEARCH_KEYWORDS = [
    "class ConnectorDispatcher",
    "def dispatch",
    "def execute",
    "chatgpt",
    "app_operator",
    "ConnectorDispatcher",
]


def iter_python_files():
    for path in LAB_ROOT.rglob("*.py"):
        if "__pycache__" in str(path):
            continue
        yield path


def find_keyword_locations():
    results = []

    for path in iter_python_files():
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception:
            continue

        for index, line in enumerate(lines, start=1):
            for keyword in SEARCH_KEYWORDS:
                if keyword in line:
                    results.append({
                        "file": path,
                        "line": index,
                        "keyword": keyword,
                        "text": line.strip(),
                    })

    return results


def print_context(path, line_no, before=5, after=8):
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()

    start = max(1, line_no - before)
    end = min(len(lines), line_no + after)

    print("")
    print(f"--- {path} : L{line_no} ---")

    for i in range(start, end + 1):
        prefix = ">>" if i == line_no else "  "
        print(f"{prefix} {i}: {lines[i - 1]}")


def main():
    print("=== ConnectorDispatcher Locator ===")

    results = find_keyword_locations()

    if not results:
        print("ConnectorDispatcher 関連コードが見つかりませんでした。")
        return

    for item in results:
        print(
            f"{item['file']}:{item['line']} "
            f"[{item['keyword']}] {item['text']}"
        )

    print("")
    print("=== 主要候補の前後コード ===")

    shown = 0

    for item in results:
        if item["keyword"] in [
            "class ConnectorDispatcher",
            "def dispatch",
            "def execute",
            "chatgpt",
            "app_operator",
        ]:
            print_context(item["file"], item["line"])
            shown += 1

        if shown >= 8:
            break


if __name__ == "__main__":
    main()