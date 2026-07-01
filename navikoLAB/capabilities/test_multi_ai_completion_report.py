from pathlib import Path

from navikoLAB.capabilities.multi_ai_completion_report import MultiAICompletionReport


def main():
    root_dir = Path(__file__).resolve().parents[1]

    reporter = MultiAICompletionReport(
        root_dir
    )

    result = reporter.save_report()

    diagnosis = result.get("diagnosis", {})

    print("=== 第19工程 MultiAI統合 完成診断 ===")
    print("状態:", diagnosis.get("status"))
    print("完成率:", diagnosis.get("completion_rate"))
    print("保存先:", result.get("report_file"))
    print("")
    print(result.get("report_text"))


if __name__ == "__main__":
    main()