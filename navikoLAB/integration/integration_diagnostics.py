from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

INTEGRATION_DIR = ROOT / "navikoLAB" / "integration"
REPORT_DIR = INTEGRATION_DIR / "reports"
PIPELINE_DIR = INTEGRATION_DIR / "pipelines"


class IntegrationDiagnostics:
    def run(self) -> dict:
        integration_maps = list(REPORT_DIR.glob("original_integration_map_*.json")) if REPORT_DIR.exists() else []
        pipelines = list(PIPELINE_DIR.glob("mission_pipeline_*.json")) if PIPELINE_DIR.exists() else []

        missing = []

        if not integration_maps:
            missing.append("original_integration_map")

        if not pipelines:
            missing.append("mission_pipeline")

        return {
            "status": "passed" if not missing else "warning",
            "integration_map_count": len(integration_maps),
            "pipeline_count": len(pipelines),
            "missing": missing,
        }


def main() -> None:
    result = IntegrationDiagnostics().run()

    print("=== Integration Diagnostics ===")
    print(f"状態: {result['status']}")
    print(f"IntegrationMap数: {result['integration_map_count']}")
    print(f"Pipeline数: {result['pipeline_count']}")
    print(f"不足候補: {len(result['missing'])}")

    for item in result["missing"]:
        print(f"- {item}")


if __name__ == "__main__":
    main()