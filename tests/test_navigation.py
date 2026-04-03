"""
Test Module: Navigation & UI Elements

Covers header, footer, hamburger menu, logout, and app state reset.
"""

import allure
import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@allure.feature("Navigation")
@allure.story("Navigation & Layout")
class TestNavigation:
    """Navigation and UI elements test suite."""

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Header and footer are visible on inventory page")
    @pytest.mark.navigation
    @pytest.mark.regression
    def test_header_and_footer_visible(self, logged_in_page, inventory_page: InventoryPage):
        """Verify that the page header title and footer are displayed."""
        title = inventory_page.get_page_title()
        assert title == "Products", f"Expected header 'Products', got '{title}'"
        assert inventory_page.is_footer_visible(), "Footer should be visible"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Hamburger menu opens and shows correct links")
    @pytest.mark.navigation
    @pytest.mark.regression
    def test_hamburger_menu_links(self, logged_in_page, inventory_page: InventoryPage):
        """Verify that the hamburger menu opens and displays all expected links."""
        inventory_page.open_menu()

        assert inventory_page.is_visible(inventory_page.LOGOUT_LINK), "Logout link should be visible"
        assert inventory_page.is_visible(inventory_page.ABOUT_LINK), "About link should be visible"
        assert inventory_page.is_visible(inventory_page.RESET_LINK), "Reset App State link should be visible"

        inventory_page.close_menu()

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Logout via hamburger menu")
    @pytest.mark.smoke
    @pytest.mark.navigation
    def test_logout(self, logged_in_page, inventory_page: InventoryPage, login_page: LoginPage):
        """Verify that clicking Logout returns to the login page."""
        inventory_page.logout()

        assert login_page.is_on_login_page(), "Should be back on the login page after logout"

    @allure.severity(allure.severity_level.MINOR)
    @allure.title("'About' link navigates to saucelabs.com")
    @pytest.mark.navigation
    @pytest.mark.regression
    def test_about_link(self, logged_in_page, inventory_page: InventoryPage):
        """Verify the About link navigates to the Sauce Labs website."""
        inventory_page.click_about()

        inventory_page.expect_url_contains("saucelabs.com")

    @allure.severity(allure.severity_level.MINOR)
    @allure.title("'Reset App State' clears the cart")
    @pytest.mark.navigation
    @pytest.mark.regression
    def test_reset_app_state(self, logged_in_page, inventory_page: InventoryPage):
        """Verify that resetting app state clears the shopping cart badge."""
        # Add items to cart first
        inventory_page.add_to_cart_by_product_key("sauce-labs-backpack")
        inventory_page.add_to_cart_by_product_key("sauce-labs-bike-light")
        assert inventory_page.get_cart_badge_count() == 2

        # Reset
        inventory_page.reset_app_state()
        inventory_page.close_menu()

        badge = inventory_page.get_cart_badge_count()
        assert badge == 0, f"Cart badge should be 0 after reset, got {badge}"
