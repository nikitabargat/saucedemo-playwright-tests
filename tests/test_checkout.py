"""
Test Module: Checkout Flow

Covers the complete checkout process, form validation, and cancellation.
"""

import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout_step_two_page import CheckoutStepTwoPage
from pages.inventory_page import InventoryPage
from utils.helpers import get_checkout_info


@allure.feature("Checkout")
@allure.story("Purchase Flow")
class TestCheckout:
    """Checkout flow test suite."""

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Complete end-to-end purchase (happy path)")
    @pytest.mark.smoke
    @pytest.mark.checkout
    @pytest.mark.e2e
    def test_complete_purchase_e2e(
        self,
        logged_in_page,
        inventory_page: InventoryPage,
        cart_page: CartPage,
        checkout_step_one: CheckoutStepOnePage,
        checkout_step_two: CheckoutStepTwoPage,
        checkout_complete: CheckoutCompletePage,
    ):
        """Verify the full purchase flow from add-to-cart to order confirmation."""
        info = get_checkout_info()

        # Add item and go to cart
        inventory_page.add_to_cart_by_product_key("sauce-labs-backpack")
        inventory_page.go_to_cart()

        # Proceed to checkout
        cart_page.proceed_to_checkout()

        # Fill checkout information
        checkout_step_one.fill_checkout_info(info["first_name"], info["last_name"], info["postal_code"])
        checkout_step_one.click_continue()

        # Verify overview and finish
        assert checkout_step_two.get_items_count() == 1
        checkout_step_two.click_finish()

        # Verify completion
        header = checkout_complete.get_complete_header()
        assert header == "Thank you for your order!", f"Expected confirmation message, got '{header}'"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Checkout with empty first name shows error")
    @pytest.mark.smoke
    @pytest.mark.checkout
    @pytest.mark.negative
    def test_checkout_empty_first_name(
        self,
        logged_in_page,
        inventory_page: InventoryPage,
        cart_page: CartPage,
        checkout_step_one: CheckoutStepOnePage,
    ):
        """Verify that leaving first name empty shows 'First Name is required'."""
        inventory_page.add_to_cart_by_product_key("sauce-labs-backpack")
        inventory_page.go_to_cart()
        cart_page.proceed_to_checkout()

        checkout_step_one.fill_checkout_info("", "Doe", "10001")
        checkout_step_one.click_continue()

        error = checkout_step_one.get_error_message()
        assert "First Name is required" in error, f"Expected first name error, got '{error}'"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Checkout with empty last name shows error")
    @pytest.mark.checkout
    @pytest.mark.negative
    def test_checkout_empty_last_name(
        self,
        logged_in_page,
        inventory_page: InventoryPage,
        cart_page: CartPage,
        checkout_step_one: CheckoutStepOnePage,
    ):
        """Verify that leaving last name empty shows 'Last Name is required'."""
        inventory_page.add_to_cart_by_product_key("sauce-labs-backpack")
        inventory_page.go_to_cart()
        cart_page.proceed_to_checkout()

        checkout_step_one.fill_checkout_info("John", "", "10001")
        checkout_step_one.click_continue()

        error = checkout_step_one.get_error_message()
        assert "Last Name is required" in error, f"Expected last name error, got '{error}'"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Checkout with empty zip code shows error")
    @pytest.mark.checkout
    @pytest.mark.negative
    def test_checkout_empty_postal_code(
        self,
        logged_in_page,
        inventory_page: InventoryPage,
        cart_page: CartPage,
        checkout_step_one: CheckoutStepOnePage,
    ):
        """Verify that leaving postal code empty shows 'Postal Code is required'."""
        inventory_page.add_to_cart_by_product_key("sauce-labs-backpack")
        inventory_page.go_to_cart()
        cart_page.proceed_to_checkout()

        checkout_step_one.fill_checkout_info("John", "Doe", "")
        checkout_step_one.click_continue()

        error = checkout_step_one.get_error_message()
        assert "Postal Code is required" in error, f"Expected postal code error, got '{error}'"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Order summary shows correct items and total")
    @pytest.mark.checkout
    @pytest.mark.regression
    def test_order_summary_correct(
        self,
        logged_in_page,
        inventory_page: InventoryPage,
        cart_page: CartPage,
        checkout_step_one: CheckoutStepOnePage,
        checkout_step_two: CheckoutStepTwoPage,
    ):
        """Verify the checkout overview displays correct items and price totals."""
        info = get_checkout_info()

        inventory_page.add_to_cart_by_product_key("sauce-labs-backpack")
        inventory_page.add_to_cart_by_product_key("sauce-labs-bike-light")
        inventory_page.go_to_cart()
        cart_page.proceed_to_checkout()

        checkout_step_one.fill_checkout_info(info["first_name"], info["last_name"], info["postal_code"])
        checkout_step_one.click_continue()

        item_names = checkout_step_two.get_item_names()
        assert len(item_names) == 2, f"Expected 2 items in summary, got {len(item_names)}"
        assert "Sauce Labs Backpack" in item_names
        assert "Sauce Labs Bike Light" in item_names

        total_text = checkout_step_two.get_total()
        assert "$" in total_text, f"Total should contain '$', got '{total_text}'"

    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Cancel from checkout step one returns to cart")
    @pytest.mark.checkout
    @pytest.mark.regression
    def test_cancel_checkout_step_one(
        self,
        logged_in_page,
        inventory_page: InventoryPage,
        cart_page: CartPage,
        checkout_step_one: CheckoutStepOnePage,
    ):
        """Verify cancelling from step one returns to the cart page."""
        inventory_page.add_to_cart_by_product_key("sauce-labs-backpack")
        inventory_page.go_to_cart()
        cart_page.proceed_to_checkout()

        checkout_step_one.click_cancel()

        checkout_step_one.expect_url_contains("/cart.html")

    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Cancel from checkout step two returns to inventory")
    @pytest.mark.checkout
    @pytest.mark.regression
    def test_cancel_checkout_step_two(
        self,
        logged_in_page,
        inventory_page: InventoryPage,
        cart_page: CartPage,
        checkout_step_one: CheckoutStepOnePage,
        checkout_step_two: CheckoutStepTwoPage,
    ):
        """Verify cancelling from step two returns to the inventory page."""
        info = get_checkout_info()

        inventory_page.add_to_cart_by_product_key("sauce-labs-backpack")
        inventory_page.go_to_cart()
        cart_page.proceed_to_checkout()

        checkout_step_one.fill_checkout_info(info["first_name"], info["last_name"], info["postal_code"])
        checkout_step_one.click_continue()

        checkout_step_two.click_cancel()

        checkout_step_two.expect_url_contains("/inventory.html")
