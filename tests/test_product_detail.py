"""
Test Module: Product Detail Page

Covers navigation to product detail, content verification, and cart actions.
"""

import allure
import pytest

from pages.inventory_page import InventoryPage
from pages.product_detail_page import ProductDetailPage


@allure.feature("Product Detail")
@allure.story("Product Detail View")
class TestProductDetail:
    """Product detail page test suite."""

    PRODUCT_NAME = "Sauce Labs Backpack"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Navigate to product detail via product name")
    @pytest.mark.smoke
    @pytest.mark.product_detail
    def test_navigate_to_product_detail(
        self, logged_in_page, inventory_page: InventoryPage, product_detail_page: ProductDetailPage
    ):
        """Verify clicking a product name navigates to the detail page."""
        inventory_page.click_product_by_name(self.PRODUCT_NAME)

        name = product_detail_page.get_product_name()
        assert name == self.PRODUCT_NAME, f"Expected '{self.PRODUCT_NAME}', got '{name}'"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Product detail shows correct name, description, price, and image")
    @pytest.mark.product_detail
    @pytest.mark.regression
    def test_product_detail_content(
        self, logged_in_page, inventory_page: InventoryPage, product_detail_page: ProductDetailPage
    ):
        """Verify all product details are displayed correctly."""
        inventory_page.click_product_by_name(self.PRODUCT_NAME)

        assert product_detail_page.get_product_name() == self.PRODUCT_NAME
        assert len(product_detail_page.get_product_description()) > 0, "Description should not be empty"
        assert "$" in product_detail_page.get_product_price(), "Price should contain '$'"
        assert product_detail_page.is_product_image_visible(), "Product image should be visible"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Add to cart from product detail page")
    @pytest.mark.product_detail
    @pytest.mark.regression
    def test_add_to_cart_from_detail(
        self, logged_in_page, inventory_page: InventoryPage, product_detail_page: ProductDetailPage
    ):
        """Verify adding a product to the cart from the detail page shows the Remove button."""
        inventory_page.click_product_by_name(self.PRODUCT_NAME)
        product_detail_page.add_to_cart()

        assert product_detail_page.is_remove_button_visible(), "Remove button should appear after adding to cart"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Navigate back to products from detail page")
    @pytest.mark.product_detail
    @pytest.mark.regression
    def test_back_to_products(
        self, logged_in_page, inventory_page: InventoryPage, product_detail_page: ProductDetailPage
    ):
        """Verify the 'Back to products' button returns to the inventory page."""
        inventory_page.click_product_by_name(self.PRODUCT_NAME)
        product_detail_page.go_back_to_products()

        product_detail_page.expect_url_contains("/inventory.html")
