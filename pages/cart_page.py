"""
CartPage — Page Object for the Shopping Cart page.
"""

import allure

from pages.base_page import BasePage


class CartPage(BasePage):
    """Encapsulates locators and actions for the Cart page."""

    # ── Locators ──────────────────────────────────────────
    CART_ITEM = "[data-test='inventory-item']"
    CART_ITEM_NAME = "[data-test='inventory-item-name']"
    CART_ITEM_PRICE = "[data-test='inventory-item-price']"
    CART_ITEM_QUANTITY = "[data-test='item-quantity']"
    REMOVE_BUTTON_PREFIX = "[data-test='remove-"
    CONTINUE_SHOPPING_BUTTON = "[data-test='continue-shopping']"
    CHECKOUT_BUTTON = "[data-test='checkout']"
    CART_BADGE = "[data-test='shopping-cart-badge']"

    # ── Navigation ────────────────────────────────────────

    def open(self) -> "CartPage":
        """Navigate directly to the cart page."""
        self.navigate("/cart.html")
        return self

    # ── Queries ───────────────────────────────────────────

    def get_cart_items_count(self) -> int:
        """Return the number of items in the cart list."""
        return self.get_count(self.CART_ITEM)

    def get_cart_item_names(self) -> list[str]:
        """Return a list of product names in the cart."""
        return self.get_texts(self.CART_ITEM_NAME)

    def get_cart_item_prices(self) -> list[str]:
        """Return a list of product prices in the cart."""
        return self.get_texts(self.CART_ITEM_PRICE)

    def get_cart_badge_count(self) -> int:
        """Return the cart badge count, or 0 if not visible."""
        if self.is_visible(self.CART_BADGE):
            return int(self.get_text(self.CART_BADGE))
        return 0

    # ── Actions ───────────────────────────────────────────

    @allure.step("Remove item '{product_key}' from cart")
    def remove_item(self, product_key: str) -> None:
        """Remove an item from the cart by its data-test key."""
        selector = f"{self.REMOVE_BUTTON_PREFIX}{product_key}']"
        self.click(selector)

    @allure.step("Click 'Continue Shopping'")
    def continue_shopping(self) -> None:
        """Navigate back to inventory by clicking Continue Shopping."""
        self.click(self.CONTINUE_SHOPPING_BUTTON)

    @allure.step("Proceed to checkout")
    def proceed_to_checkout(self) -> None:
        """Click the Checkout button."""
        self.click(self.CHECKOUT_BUTTON)
