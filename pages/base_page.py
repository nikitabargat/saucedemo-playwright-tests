"""
BasePage — shared helpers inherited by every page object.
"""

import re

import allure
from playwright.sync_api import Page, expect

from config.settings import settings


class BasePage:
    """Base class providing common Playwright interactions for all page objects."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.page.set_default_timeout(settings.DEFAULT_TIMEOUT)

    # ── Navigation ────────────────────────────────────────

    def navigate(self, path: str = "/") -> None:
        """Navigate to a path relative to BASE_URL."""
        url = f"{settings.BASE_URL}{path}"
        with allure.step(f"Navigate to {url}"):
            self.page.goto(url, wait_until="domcontentloaded")

    def get_current_url(self) -> str:
        """Return the current page URL."""
        return self.page.url

    # ── Element Interactions ──────────────────────────────

    def click(self, locator: str) -> None:
        """Click an element identified by the given selector."""
        with allure.step(f"Click on '{locator}'"):
            self.page.locator(locator).click()

    def fill(self, locator: str, value: str) -> None:
        """Fill a text input."""
        with allure.step(f"Fill '{locator}' with '{value}'"):
            self.page.locator(locator).fill(value)

    def get_text(self, locator: str) -> str:
        """Return the inner text of an element."""
        return self.page.locator(locator).inner_text()

    def get_texts(self, locator: str) -> list[str]:
        """Return inner texts of all matching elements."""
        return self.page.locator(locator).all_inner_texts()

    def is_visible(self, locator: str) -> bool:
        """Check if an element is visible."""
        return self.page.locator(locator).is_visible()

    def wait_for(self, locator: str, state: str = "visible") -> None:
        """Wait for an element to reach the specified state."""
        self.page.locator(locator).wait_for(state=state)

    def get_count(self, locator: str) -> int:
        """Return the number of elements matching the locator."""
        return self.page.locator(locator).count()

    def get_attribute(self, locator: str, attribute: str) -> str | None:
        """Return the value of an attribute on the first matching element."""
        return self.page.locator(locator).get_attribute(attribute)

    # ── Assertions (Playwright expect) ────────────────────

    def expect_visible(self, locator: str) -> None:
        """Assert that an element is visible."""
        expect(self.page.locator(locator)).to_be_visible()

    def expect_text(self, locator: str, text: str) -> None:
        """Assert that an element contains the expected text."""
        expect(self.page.locator(locator)).to_have_text(text)

    def expect_url_contains(self, fragment: str) -> None:
        """Assert the current URL contains a fragment."""
        # Use regex for flexible substring matching in URLs
        pattern = re.compile(f".*{re.escape(fragment)}.*")
        expect(self.page).to_have_url(pattern)

    # ── Screenshots ───────────────────────────────────────

    def take_screenshot(self, name: str = "screenshot") -> bytes:
        """Capture a full-page screenshot and attach it to the Allure report."""
        screenshot = self.page.screenshot(full_page=True)
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
        return screenshot

    # ── Dropdown ──────────────────────────────────────────

    def select_option(self, locator: str, value: str) -> None:
        """Select an option by its value attribute."""
        with allure.step(f"Select '{value}' from '{locator}'"):
            self.page.locator(locator).select_option(value)
