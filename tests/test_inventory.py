"""
Test Module: Inventory / Products Page

Covers product listing, sorting, and add-to-cart functionality.
"""

import allure
import pytest

from pages.inventory_page import InventoryPage
from utils.helpers import get_product_data


@allure.feature("Inventory")
@allure.story("Product Listing & Sorting")
class TestInventory:
    """Inventory page test suite."""

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("All 6 products are displayed on the inventory page")
    @pytest.mark.smoke
    @pytest.mark.inventory
    def test_all_products_displayed(self, logged_in_page, inventory_page: InventoryPage):
        """Verify that all 6 products are visible on the inventory page."""
        products = get_product_data()
        count = inventory_page.get_product_count()

        assert count == products["total_count"], f"Expected {products['total_count']} products, got {count}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Products are sorted by Name (A→Z) by default")
    @pytest.mark.smoke
    @pytest.mark.inventory
    def test_sort_name_az_default(self, logged_in_page, inventory_page: InventoryPage):
        """Verify that products are sorted alphabetically A→Z by default."""
        names = inventory_page.get_product_names()
        assert names == sorted(names), f"Products are not sorted A→Z: {names}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Sort products by Name (Z→A)")
    @pytest.mark.inventory
    @pytest.mark.regression
    def test_sort_name_za(self, logged_in_page, inventory_page: InventoryPage):
        """Verify that sorting by Z→A reverses the product list."""
        inventory_page.sort_by("za")
        names = inventory_page.get_product_names()
        assert names == sorted(names, reverse=True), f"Products are not sorted Z→A: {names}"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Sort products by Price (Low→High)")
    @pytest.mark.inventory
    @pytest.mark.regression
    def test_sort_price_low_to_high(self, logged_in_page, inventory_page: InventoryPage):
        """Verify that sorting by price low→high orders products correctly."""
        inventory_page.sort_by("lohi")
        prices = inventory_page.get_product_prices()
        assert prices == sorted(prices), f"Prices are not sorted low→high: {prices}"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Sort products by Price (High→Low)")
    @pytest.mark.inventory
    @pytest.mark.regression
    def test_sort_price_high_to_low(self, logged_in_page, inventory_page: InventoryPage):
        """Verify that sorting by price high→low orders products correctly."""
        inventory_page.sort_by("hilo")
        prices = inventory_page.get_product_prices()
        assert prices == sorted(prices, reverse=True), f"Prices are not sorted high→low: {prices}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Add single item to cart — badge updates to 1")
    @pytest.mark.smoke
    @pytest.mark.inventory
    def test_add_single_item_badge_updates(self, logged_in_page, inventory_page: InventoryPage):
        """Verify that adding one item shows a cart badge with count 1."""
        inventory_page.add_to_cart_by_product_key("sauce-labs-backpack")
        count = inventory_page.get_cart_badge_count()

        assert count == 1, f"Expected cart badge count 1, got {count}"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Add multiple items to cart — badge shows correct count")
    @pytest.mark.inventory
    @pytest.mark.regression
    def test_add_multiple_items_badge_count(self, logged_in_page, inventory_page: InventoryPage):
        """Verify that adding 3 items shows a cart badge with count 3."""
        inventory_page.add_to_cart_by_product_key("sauce-labs-backpack")
        inventory_page.add_to_cart_by_product_key("sauce-labs-bike-light")
        inventory_page.add_to_cart_by_product_key("sauce-labs-bolt-t-shirt")

        count = inventory_page.get_cart_badge_count()
        assert count == 3, f"Expected cart badge count 3, got {count}"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Remove item from inventory page — badge decrements")
    @pytest.mark.inventory
    @pytest.mark.regression
    def test_remove_item_badge_decrements(self, logged_in_page, inventory_page: InventoryPage):
        """Verify that removing an item from inventory decrements the cart badge."""
        inventory_page.add_to_cart_by_product_key("sauce-labs-backpack")
        inventory_page.add_to_cart_by_product_key("sauce-labs-bike-light")
        assert inventory_page.get_cart_badge_count() == 2

        inventory_page.remove_by_product_key("sauce-labs-backpack")
        count = inventory_page.get_cart_badge_count()
        assert count == 1, f"Expected cart badge count 1 after removal, got {count}"
