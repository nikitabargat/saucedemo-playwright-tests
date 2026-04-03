"""
CheckoutStepOnePage — Page Object for the Checkout: Your Information step.
"""

import allure

from pages.base_page import BasePage


class CheckoutStepOnePage(BasePage):
    """Encapsulates locators and actions for Checkout Step One (Information)."""

    # ── Locators ──────────────────────────────────────────
    FIRST_NAME_INPUT = "[data-test='firstName']"
    LAST_NAME_INPUT = "[data-test='lastName']"
    POSTAL_CODE_INPUT = "[data-test='postalCode']"
    CONTINUE_BUTTON = "[data-test='continue']"
    CANCEL_BUTTON = "[data-test='cancel']"
    ERROR_MESSAGE = "[data-test='error']"

    # ── Actions ───────────────────────────────────────────

    @allure.step("Fill checkout info: {first_name} {last_name}, {postal_code}")
    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Fill in the checkout information form."""
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.POSTAL_CODE_INPUT, postal_code)

    @allure.step("Click Continue")
    def click_continue(self) -> None:
        """Submit the checkout information form."""
        self.click(self.CONTINUE_BUTTON)

    @allure.step("Cancel checkout")
    def click_cancel(self) -> None:
        """Cancel the checkout and return to the cart."""
        self.click(self.CANCEL_BUTTON)

    def get_error_message(self) -> str:
        """Return the validation error message text."""
        self.wait_for(self.ERROR_MESSAGE)
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        """Check if an error message is visible."""
        return self.is_visible(self.ERROR_MESSAGE)
