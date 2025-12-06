"""Configuration management for EasyQA Framework."""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class Config:
    """Configuration manager for test framework."""

    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        """Singleton pattern for config."""
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Load configuration from YAML file."""
        config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"

        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                self._config = yaml.safe_load(f)
        else:
            logger.warning(f"Config file not found at {config_path}, using defaults")
            self._config = self._get_default_config()

        # Override with environment variables
        self._load_env_overrides()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "browser": {
                "default": "chrome",
                "headless": False,
                "window_size": "1920,1080",
                "timeout": 30,
            },
            "ai": {
                "visual_testing": {
                    "enabled": True,
                    "threshold": 0.95,
                    "model_path": "models/visual_model.h5",
                },
                "self_healing": {
                    "enabled": True,
                    "confidence_threshold": 0.8,
                    "max_attempts": 3,
                },
                "test_generation": {"enabled": True, "min_confidence": 0.7},
            },
            "reporting": {
                "screenshots_on_failure": True,
                "video_recording": False,
                "ai_insights": True,
            },
            "performance": {"lighthouse_enabled": True, "load_time_threshold": 3.0},
            "database": {"type": "sqlite", "path": "data/test_results.db"},
        }

    def _load_env_overrides(self):
        """Load configuration overrides from environment variables."""
        env_mappings = {
            "EASYQA_BROWSER": ("browser", "default"),
            "EASYQA_HEADLESS": ("browser", "headless"),
            "EASYQA_AI_VISUAL": ("ai", "visual_testing", "enabled"),
            "EASYQA_AI_HEALING": ("ai", "self_healing", "enabled"),
        }

        for env_var, config_path in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                self._set_nested_value(config_path, value)

    def _set_nested_value(self, keys: tuple, value: Any):
        """Set value in nested dictionary."""
        d = self._config
        for key in keys[:-1]:
            d = d.setdefault(key, {})
        d[keys[-1]] = value

    def get(self, *keys: str, default: Any = None) -> Any:
        """Get configuration value by nested keys."""
        value = self._config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return default
            else:
                return default
        return value

    def set(self, *keys: str, value: Any):
        """Set configuration value by nested keys."""
        self._set_nested_value(keys, value)

    @property
    def config(self) -> Dict[str, Any]:
        """Get full configuration dictionary."""
        return self._config


# Global config instance
config = Config()
