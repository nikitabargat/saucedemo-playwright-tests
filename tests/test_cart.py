"""
Test Module: Shopping Cart

Covers cart item display, removal, persistence, and navigation.
"""

import allure
import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


@allure.feature("Cart")
@allure.story("Shopping Cart Operations")
class TestCart:
    """Shopping cart test suite."""

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Added items appear in cart with correct details")
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_added_items_appear_in_cart(
        self, logged_in_page, inventory_page: InventoryPage, cart_page: CartPage
    ):
        """Verify that items added from inventory appear in the cart."""
        inventory_page.add_to_cart_by_product_key("sauce-labs-backpack")
        inventory_page.add_to_cart_by_product_key("sauce-labs-bike-light")
        inventory_page.go_to_cart()

        items = cart_page.get_cart_item_names()
        assert len(items) == 2, f"Expected 2 items in cart, got {len(items)}"
        assert "Sauce Labs Backpack" in items
        assert "Sauce Labs Bike Light" in items

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Remove item from cart")
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_remove_item_from_cart(
        self, logged_in_page, inventory_page: InventoryPage, cart_page: CartPage
    ):
        """Verify that removing an item from the cart reduces the items count."""
        inventory_page.add_to_cart_by_product_key("sauce-labs-backpack")
        inventory_page.add_to_cart_by_product_key("sauce-labs-bike-light")
        inventory_page.go_to_cart()

        cart_page.remove_item("sauce-labs-backpack")

        items = cart_page.get_cart_item_names()
        assert len(items) == 1, f"Expected 1 item after removal, got {len(items)}"
        assert "Sauce Labs Bike Light" in items

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("'Continue Shopping' navigates back to inventory")
    @pytest.mark.cart
    @pytest.mark.regression
    def test_continue_shopping_navigation(
        self, logged_in_page, inventory_page: InventoryPage, cart_page: CartPage
    ):
        """Verify that 'Continue Shopping' returns to the inventory page."""
        inventory_page.go_to_cart()
        cart_page.continue_shopping()

        cart_page.expect_url_contains("/inventory.html")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Cart items persist after page navigation")
    @pytest.mark.cart
    @pytest.mark.regression
    def test_cart_persistence_after_navigation(
        self, logged_in_page, inventory_page: InventoryPage, cart_page: CartPage
    ):
        """Verify that cart items persist when navigating away and back."""
        inventory_page.add_to_cart_by_product_key("sauce-labs-backpack")
        inventory_page.go_to_cart()

        # Navigate away
        cart_page.continue_shopping()
        # Navigate back to cart
        inventory_page.go_to_cart()

        items = cart_page.get_cart_item_names()
        assert "Sauce Labs Backpack" in items, "Cart item should persist after navigation"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Cart badge reflects correct item count")
    @pytest.mark.cart
    @pytest.mark.regression
    def test_cart_badge_reflects_count(
        self, logged_in_page, inventory_page: InventoryPage, cart_page: CartPage
    ):
        """Verify the cart badge on the cart page shows the correct count."""
        inventory_page.add_to_cart_by_product_key("sauce-labs-backpack")
        inventory_page.add_to_cart_by_product_key("sauce-labs-bolt-t-shirt")
        inventory_page.go_to_cart()

        badge = cart_page.get_cart_badge_count()
        assert badge == 2, f"Expected badge count 2, got {badge}"
