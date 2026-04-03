"""
CheckoutCompletePage — Page Object for the order confirmation screen.
"""

from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    """Encapsulates locators and actions for the Checkout Complete page."""

    # ── Locators ──────────────────────────────────────────
    COMPLETE_HEADER = "[data-test='complete-header']"
    COMPLETE_TEXT = "[data-test='complete-text']"
    PONY_EXPRESS_IMAGE = "[data-test='pony-express']"
    BACK_HOME_BUTTON = "[data-test='back-to-products']"

    # ── Queries ───────────────────────────────────────────

    def get_complete_header(self) -> str:
        """Return the confirmation heading text (e.g. 'Thank you for your order!')."""
        return self.get_text(self.COMPLETE_HEADER)

    def get_complete_text(self) -> str:
        """Return the confirmation body text."""
        return self.get_text(self.COMPLETE_TEXT)

    def is_pony_express_image_visible(self) -> bool:
        """Return True if the confirmation image is visible."""
        return self.is_visible(self.PONY_EXPRESS_IMAGE)

    # ── Actions ───────────────────────────────────────────

    def go_back_home(self) -> None:
        """Click 'Back Home' to return to the inventory page."""
        self.click(self.BACK_HOME_BUTTON)
