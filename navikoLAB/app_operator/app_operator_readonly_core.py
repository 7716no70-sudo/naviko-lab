from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class ReadOnlyOperationResult:
    operation: str
    status: str
    allowed: bool
    target_exists: bool
    target_type: str
    message: str
    real_gui_operation: bool = False
    external_operation: bool = False
    original_write: bool = False


class AppOperatorReadOnlyCore:
    def inspect_path(self, target_path: str) -> ReadOnlyOperationResult:
        path = Path(target_path)
        exists = path.exists()

        if not exists:
            target_type = "missing"
        elif path.is_dir():
            target_type = "directory"
        elif path.is_file():
            target_type = "file"
        else:
            target_type = "other"

        return ReadOnlyOperationResult(
            operation="inspect_path",
            status="completed",
            allowed=True,
            target_exists=exists,
            target_type=target_type,
            message="read_only_inspection_completed",
        )


def inspect_path_readonly(target_path: str) -> dict:
    core = AppOperatorReadOnlyCore()
    return asdict(core.inspect_path(target_path))