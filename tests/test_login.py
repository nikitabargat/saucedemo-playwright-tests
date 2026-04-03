"""
Test Module: Authentication (Login Page)

Covers positive and negative login scenarios for the SauceDemo application.
"""

import allure
import pytest

from pages.login_page import LoginPage
from utils.helpers import get_invalid_user, get_valid_user


@allure.feature("Authentication")
@allure.story("Login")
class TestLogin:
    """Login page test suite."""

    # ── Positive Tests ────────────────────────────────────

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Login with valid standard_user credentials")
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_valid_standard_user(self, login_page: LoginPage):
        """Verify that standard_user can log in and reaches the inventory page."""
        user = get_valid_user("standard_user")
        login_page.open()
        login_page.login(user["username"], user["password"])

        login_page.expect_url_contains("/inventory.html")

    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Login with performance_glitch_user (slow but successful)")
    @pytest.mark.login
    @pytest.mark.regression
    def test_login_performance_glitch_user(self, login_page: LoginPage):
        """Verify that performance_glitch_user can log in despite the delay."""
        user = get_valid_user("performance_glitch_user")
        login_page.open()
        login_page.login(user["username"], user["password"])

        login_page.expect_url_contains("/inventory.html")

    # ── Negative Tests ────────────────────────────────────

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Login with locked_out_user shows error")
    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.negative
    def test_login_locked_out_user(self, login_page: LoginPage):
        """Verify that locked_out_user sees the correct error message."""
        user = get_invalid_user("locked_out_user")
        login_page.open()
        login_page.login(user["username"], user["password"])

        error = login_page.get_error_message()
        assert error == user["expected_error"], f"Expected '{user['expected_error']}', got '{error}'"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Login with invalid password shows error")
    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.negative
    def test_login_invalid_password(self, login_page: LoginPage):
        """Verify that an incorrect password triggers the correct error."""
        user = get_invalid_user("invalid_password")
        login_page.open()
        login_page.login(user["username"], user["password"])

        error = login_page.get_error_message()
        assert error == user["expected_error"]

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Login with empty username shows error")
    @pytest.mark.login
    @pytest.mark.negative
    def test_login_empty_username(self, login_page: LoginPage):
        """Verify that submitting with an empty username shows 'Username is required'."""
        user = get_invalid_user("empty_username")
        login_page.open()
        login_page.login(user["username"], user["password"])

        error = login_page.get_error_message()
        assert error == user["expected_error"]

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Login with empty password shows error")
    @pytest.mark.login
    @pytest.mark.negative
    def test_login_empty_password(self, login_page: LoginPage):
        """Verify that submitting with an empty password shows 'Password is required'."""
        user = get_invalid_user("empty_password")
        login_page.open()
        login_page.login(user["username"], user["password"])

        error = login_page.get_error_message()
        assert error == user["expected_error"]

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Login with both fields empty shows error")
    @pytest.mark.login
    @pytest.mark.negative
    def test_login_both_fields_empty(self, login_page: LoginPage):
        """Verify that submitting with both fields empty shows 'Username is required'."""
        user = get_invalid_user("empty_both")
        login_page.open()
        login_page.login(user["username"], user["password"])

        error = login_page.get_error_message()
        assert error == user["expected_error"]

    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Error message can be dismissed via X button")
    @pytest.mark.login
    @pytest.mark.regression
    def test_error_message_dismissible(self, login_page: LoginPage):
        """Verify that the error message disappears after clicking the close button."""
        user = get_invalid_user("invalid_password")
        login_page.open()
        login_page.login(user["username"], user["password"])

        assert login_page.is_error_displayed(), "Error should be visible"
        login_page.close_error()
        assert not login_page.is_error_displayed(), "Error should be dismissed"
