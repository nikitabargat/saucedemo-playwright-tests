"""
Utility helpers for the SauceDemo test framework.
"""

import json
from pathlib import Path


_DATA_DIR = Path(__file__).resolve().parent.parent / "test_data"


def load_test_data(filename: str = "users.json") -> dict:
    """Load and return parsed JSON test data."""
    filepath = _DATA_DIR / filename
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def get_valid_user(key: str = "standard_user") -> dict:
    """Return credentials dict for a valid user."""
    data = load_test_data()
    return data["valid_users"][key]


def get_invalid_user(key: str) -> dict:
    """Return credentials + expected error for an invalid user scenario."""
    data = load_test_data()
    return data["invalid_users"][key]


def get_checkout_info(key: str = "valid") -> dict:
    """Return checkout form data."""
    data = load_test_data()
    return data["checkout_info"][key]


def get_product_data() -> dict:
    """Return product catalog metadata."""
    data = load_test_data()
    return data["products"]
