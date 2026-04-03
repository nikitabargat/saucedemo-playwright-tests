"""
ProductDetailPage — Page Object for the single product detail view.
"""

import allure

from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    """Encapsulates locators and actions for the Product Detail page."""

    # ── Locators ──────────────────────────────────────────
    PRODUCT_NAME = "[data-test='inventory-item-name']"
    PRODUCT_DESC = "[data-test='inventory-item-desc']"
    PRODUCT_PRICE = "[data-test='inventory-item-price']"
    PRODUCT_IMAGE = "img.inventory_details_img"
    ADD_TO_CART_BUTTON = "[data-test='add-to-cart']"
    REMOVE_BUTTON = "[data-test='remove']"
    BACK_BUTTON = "[data-test='back-to-products']"

    # ── Queries ───────────────────────────────────────────

    def get_product_name(self) -> str:
        """Return the product name."""
        return self.get_text(self.PRODUCT_NAME)

    def get_product_description(self) -> str:
        """Return the product description."""
        return self.get_text(self.PRODUCT_DESC)

    def get_product_price(self) -> str:
        """Return the product price text (e.g. '$29.99')."""
        return self.get_text(self.PRODUCT_PRICE)

    def is_product_image_visible(self) -> bool:
        """Return True if the product image is visible."""
        return self.is_visible(self.PRODUCT_IMAGE)

    # ── Actions ───────────────────────────────────────────

    @allure.step("Add to cart from product detail")
    def add_to_cart(self) -> None:
        """Click the Add to Cart button on the detail page."""
        self.click(self.ADD_TO_CART_BUTTON)

    @allure.step("Remove from cart on product detail")
    def remove_from_cart(self) -> None:
        """Click the Remove button on the detail page."""
        self.click(self.REMOVE_BUTTON)

    @allure.step("Navigate back to products")
    def go_back_to_products(self) -> None:
        """Click the 'Back to products' button."""
        self.click(self.BACK_BUTTON)

    def is_remove_button_visible(self) -> bool:
        """Check if Remove button is displayed (item is in cart)."""
        return self.is_visible(self.REMOVE_BUTTON)
