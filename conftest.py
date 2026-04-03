"""
Root conftest — Allure hooks for screenshot capture on failure.
"""

import allure
import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to the Allure report when a test fails."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page") or item.funcargs.get("logged_in_page")
        if page is not None:
            try:
                screenshot = page.screenshot(full_page=True)
                allure.attach(
                    screenshot,
                    name=f"failure-{item.name}",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass  # Page may already be closed
