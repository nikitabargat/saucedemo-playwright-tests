"""
Centralized configuration for the SauceDemo test framework.

Reads settings from environment variables (or .env file) with sensible defaults.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root if it exists
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)


class Settings:
    """Application-wide test settings."""

    # ── URLs ──────────────────────────────────────────────
    BASE_URL: str = os.getenv("BASE_URL", "https://www.saucedemo.com")

    # ── Browser ───────────────────────────────────────────
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"
    BROWSER: str = os.getenv("BROWSER", "chromium")
    SLOW_MO: int = int(os.getenv("SLOW_MO", "0"))

    # ── Timeouts (milliseconds) ───────────────────────────
    DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "30000"))

    # ── Paths ─────────────────────────────────────────────
    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
    ALLURE_RESULTS: Path = PROJECT_ROOT / "allure-results"
    SCREENSHOTS_DIR: Path = PROJECT_ROOT / "screenshots"


settings = Settings()
