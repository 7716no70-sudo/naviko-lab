# -*- coding: utf-8 -*-
"""
Naviko Tool System - ツールメタデータ定義

このモジュールは、ツールの型定義とメタデータクラスを提供します。

Author: Naviko Development Team
Date: 2026-07-08
Version: 1.0.0
"""

from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


class ToolCategory(Enum):
    """ツールカテゴリ"""
    DATA_PROCESSING = "data_processing"
    AI_ML = "ai_ml"
    EXTERNAL_API = "external_api"
    FILE_OPERATION = "file_operation"
    VOICE_PROCESSING = "voice_processing"
    IMAGE_PROCESSING = "image_processing"
    WEB = "web"
    SYSTEM = "system"
    OTHER = "other"


class ToolComplexity(Enum):
    """ツールの複雑度"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"


@dataclass
class ToolMetadata:
    """ツールメタデータ"""
    name: str
    version: str
    category: ToolCategory
    description: str
    complexity: ToolComplexity = ToolComplexity.MODERATE
    required_params: List[str] = field(default_factory=list)
    optional_params: List[str] = field(default_factory=list)
    return_type: str = "Any"
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    author: str = "Naviko Team"
    priority: int = 50
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "category": self.category.value,
            "description": self.description,
            "complexity": self.complexity.value,
            "required_params": self.required_params,
            "optional_params": self.optional_params,
            "return_type": self.return_type,
            "tags": self.tags,
            "dependencies": self.dependencies,
            "author": self.author,
            "priority": self.priority
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ToolMetadata":
        return cls(
            name=data["name"],
            version=data["version"],
            category=ToolCategory(data["category"]),
            description=data["description"],
            complexity=ToolComplexity(data.get("complexity", "moderate")),
            required_params=data.get("required_params", []),
            optional_params=data.get("optional_params", []),
            return_type=data.get("return_type", "Any"),
            tags=data.get("tags", []),
            dependencies=data.get("dependencies", []),
            author=data.get("author", "Naviko Team"),
            priority=data.get("priority", 50)
        )
    
    def validate_params(self, params: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        for required_param in self.required_params:
            if required_param not in params:
                return False, f"必須パラメータが不足: {required_param}"
        return True, None


__version__ = "1.0.0"
__author__ = "Naviko Development Team"
__all__ = ["ToolCategory", "ToolComplexity", "ToolMetadata"]
