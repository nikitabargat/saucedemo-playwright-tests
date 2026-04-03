"""
LoginPage — Page Object for the SauceDemo login screen.
"""

import allure

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Encapsulates locators and actions for the Login page."""

    # ── Locators ──────────────────────────────────────────
    USERNAME_INPUT = "[data-test='username']"
    PASSWORD_INPUT = "[data-test='password']"
    LOGIN_BUTTON = "[data-test='login-button']"
    ERROR_MESSAGE = "[data-test='error']"
    ERROR_CLOSE_BUTTON = ".error-button"

    # ── Actions ───────────────────────────────────────────

    def open(self) -> "LoginPage":
        """Navigate to the login page."""
        self.navigate("/")
        return self

    @allure.step("Login with username='{username}'")
    def login(self, username: str, password: str) -> None:
        """Fill credentials and submit the login form."""
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        """Return the error message text displayed on login failure."""
        self.wait_for(self.ERROR_MESSAGE)
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        """Check if the error container is visible."""
        return self.is_visible(self.ERROR_MESSAGE)

    @allure.step("Close the error message")
    def close_error(self) -> None:
        """Dismiss the error message by clicking the X button."""
        self.click(self.ERROR_CLOSE_BUTTON)

    def is_on_login_page(self) -> bool:
        """Return True if the login button is visible (indicating we're on the login page)."""
        return self.is_visible(self.LOGIN_BUTTON)
