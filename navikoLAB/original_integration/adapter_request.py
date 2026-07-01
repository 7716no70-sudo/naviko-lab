from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class AdapterRequest:

    mission: str

    planner_result: Dict[str, Any] = field(default_factory=dict)

    capability_result: Dict[str, Any] = field(default_factory=dict)

    connector_result: Dict[str, Any] = field(default_factory=dict)

    metadata: Dict[str, Any] = field(default_factory=dict)