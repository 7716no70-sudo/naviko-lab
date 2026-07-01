from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC_DIR = ROOT / "navikoLAB" / "docs"
TEST_DIR = ROOT / "tests"


class DocumentationDiagnostics:
    def run(self) -> dict:
        markdown_files = list(DOC_DIR.glob("*.md")) if DOC_DIR.exists() else []
        json_files = list(DOC_DIR.glob("*.json")) if DOC_DIR.exists() else []
        test_files = list(TEST_DIR.glob("test_*.py")) if TEST_DIR.exists() else []

        missing = []

        if not markdown_files:
            missing.append("markdown_documentation")

        if not json_files:
            missing.append("json_summary")

        if not test_files:
            missing.append("generated_tests")

        status = "passed" if not missing else "warning"

        return {
            "status": status,
            "markdown_count": len(markdown_files),
            "json_count": len(json_files),
            "test_count": len(test_files),
            "missing": missing,
        }


def main() -> None:
    result = DocumentationDiagnostics().run()

    print("=== Documentation Diagnostics ===")
    print(f"状態: {result['status']}")
    print(f"Markdown数: {result['markdown_count']}")
    print(f"JSON数: {result['json_count']}")
    print(f"Test数: {result['test_count']}")
    print(f"不足候補: {len(result['missing'])}")

    for item in result["missing"]:
        print(f"- {item}")


if __name__ == "__main__":
    main()