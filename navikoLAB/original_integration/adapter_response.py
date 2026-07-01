from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class AdapterResponse:

    status: str

    routed: bool

    dry_run: bool

    app_operator_called: bool

    payload: Dict[str, Any] = field(default_factory=dict)