"""
CheckoutStepTwoPage — Page Object for the Checkout: Overview / Review step.
"""

import allure

from pages.base_page import BasePage


class CheckoutStepTwoPage(BasePage):
    """Encapsulates locators and actions for Checkout Step Two (Overview)."""

    # ── Locators ──────────────────────────────────────────
    CART_ITEM = "[data-test='inventory-item']"
    CART_ITEM_NAME = "[data-test='inventory-item-name']"
    CART_ITEM_PRICE = "[data-test='inventory-item-price']"
    SUBTOTAL_LABEL = "[data-test='subtotal-label']"
    TAX_LABEL = "[data-test='tax-label']"
    TOTAL_LABEL = "[data-test='total-label']"
    FINISH_BUTTON = "[data-test='finish']"
    CANCEL_BUTTON = "[data-test='cancel']"

    # ── Queries ───────────────────────────────────────────

    def get_items_count(self) -> int:
        """Return the number of items in the order summary."""
        return self.get_count(self.CART_ITEM)

    def get_item_names(self) -> list[str]:
        """Return product names on the overview page."""
        return self.get_texts(self.CART_ITEM_NAME)

    def get_subtotal(self) -> str:
        """Return the subtotal text."""
        return self.get_text(self.SUBTOTAL_LABEL)

    def get_tax(self) -> str:
        """Return the tax text."""
        return self.get_text(self.TAX_LABEL)

    def get_total(self) -> str:
        """Return the total text."""
        return self.get_text(self.TOTAL_LABEL)

    # ── Actions ───────────────────────────────────────────

    @allure.step("Finish order")
    def click_finish(self) -> None:
        """Click the Finish button to complete the order."""
        self.click(self.FINISH_BUTTON)

    @allure.step("Cancel from overview")
    def click_cancel(self) -> None:
        """Cancel the order from the overview page."""
        self.click(self.CANCEL_BUTTON)
