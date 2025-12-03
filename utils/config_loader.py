#!/usr/bin/env python3

from __future__ import annotations

import json
import os
from typing import Any, Dict


class Config:

    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls) -> Config:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self) -> None:
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "config.json"
        )
        
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self._config = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}"
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")

    def get(self, *keys: str, default: Any = None) -> Any:
        value = self._config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return default
            else:
                return default
        return value

    def expand_path(self, *keys: str) -> str:
        path = self.get(*keys)
        if path and isinstance(path, str):
            return os.path.abspath(os.path.expanduser(path))
        return ""

    @property
    def all(self) -> Dict[str, Any]:
        return self._config


def get_config() -> Config:
    return Config()
