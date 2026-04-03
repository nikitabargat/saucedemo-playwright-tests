"""
InventoryPage — Page Object for the Products / Inventory listing.
"""

import allure

from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Encapsulates locators and actions for the Inventory (Products) page."""

    # ── Locators ──────────────────────────────────────────
    INVENTORY_LIST = "[data-test='inventory-list']"
    INVENTORY_ITEM = "[data-test='inventory-item']"
    INVENTORY_ITEM_NAME = "[data-test='inventory-item-name']"
    INVENTORY_ITEM_PRICE = "[data-test='inventory-item-price']"
    INVENTORY_ITEM_DESC = "[data-test='inventory-item-desc']"
    SORT_DROPDOWN = "[data-test='product-sort-container']"
    CART_BADGE = "[data-test='shopping-cart-badge']"
    CART_LINK = "[data-test='shopping-cart-link']"
    ADD_TO_CART_PREFIX = "[data-test='add-to-cart-"
    REMOVE_PREFIX = "[data-test='remove-"

    # Hamburger menu
    BURGER_MENU_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "[data-test='logout-sidebar-link']"
    ABOUT_LINK = "[data-test='about-sidebar-link']"
    RESET_LINK = "[data-test='reset-sidebar-link']"
    CLOSE_MENU_BUTTON = "#react-burger-cross-btn"

    # Header / Footer
    HEADER_TITLE = "[data-test='title']"
    FOOTER = "[data-test='footer']"

    # ── Navigation ────────────────────────────────────────

    def open(self) -> "InventoryPage":
        """Navigate directly to the inventory page."""
        self.navigate("/inventory.html")
        return self

    # ── Product Queries ───────────────────────────────────

    def get_product_count(self) -> int:
        """Return the number of products displayed."""
        return self.get_count(self.INVENTORY_ITEM)

    def get_product_names(self) -> list[str]:
        """Return a list of all visible product names."""
        return self.get_texts(self.INVENTORY_ITEM_NAME)

    def get_product_prices(self) -> list[float]:
        """Return a list of all visible product prices as floats."""
        raw = self.get_texts(self.INVENTORY_ITEM_PRICE)
        return [float(p.replace("$", "")) for p in raw]

    def click_product_by_name(self, name: str) -> None:
        """Click a product's name link to open its detail page."""
        with allure.step(f"Click product: {name}"):
            self.page.locator(self.INVENTORY_ITEM_NAME, has_text=name).click()

    # ── Sorting ───────────────────────────────────────────

    @allure.step("Sort products by '{value}'")
    def sort_by(self, value: str) -> None:
        """Sort products using the dropdown. Values: az, za, lohi, hilo."""
        self.select_option(self.SORT_DROPDOWN, value)

    def get_selected_sort(self) -> str:
        """Return the currently selected sort option value."""
        return self.page.locator(self.SORT_DROPDOWN).input_value()

    # ── Cart Interactions ─────────────────────────────────

    def add_to_cart_by_product_key(self, product_key: str) -> None:
        """
        Add a product to the cart using its data-test key.
        Example key: 'sauce-labs-backpack'
        """
        selector = f"{self.ADD_TO_CART_PREFIX}{product_key}']"
        with allure.step(f"Add to cart: {product_key}"):
            self.click(selector)

    def remove_by_product_key(self, product_key: str) -> None:
        """Remove a product from the cart using its data-test key."""
        selector = f"{self.REMOVE_PREFIX}{product_key}']"
        with allure.step(f"Remove from cart: {product_key}"):
            self.click(selector)

    def get_cart_badge_count(self) -> int:
        """Return the number shown on the cart badge, or 0 if hidden."""
        if self.is_visible(self.CART_BADGE):
            text = self.get_text(self.CART_BADGE)
            return int(text)
        return 0

    def go_to_cart(self) -> None:
        """Click the cart icon to navigate to the cart page."""
        with allure.step("Navigate to cart"):
            self.click(self.CART_LINK)

    # ── Hamburger Menu ────────────────────────────────────

    @allure.step("Open hamburger menu")
    def open_menu(self) -> None:
        """Open the side navigation menu."""
        self.click(self.BURGER_MENU_BUTTON)
        self.wait_for(self.CLOSE_MENU_BUTTON)

    @allure.step("Logout via menu")
    def logout(self) -> None:
        """Open menu and click logout."""
        self.open_menu()
        self.click(self.LOGOUT_LINK)

    @allure.step("Click 'About' in menu")
    def click_about(self) -> None:
        """Open menu and click the About link."""
        self.open_menu()
        self.click(self.ABOUT_LINK)

    @allure.step("Reset app state via menu")
    def reset_app_state(self) -> None:
        """Open menu and click 'Reset App State'."""
        self.open_menu()
        self.click(self.RESET_LINK)

    @allure.step("Close hamburger menu")
    def close_menu(self) -> None:
        """Close the side navigation menu."""
        self.click(self.CLOSE_MENU_BUTTON)

    # ── Page Assertions ───────────────────────────────────

    def get_page_title(self) -> str:
        """Return the page header title text."""
        return self.get_text(self.HEADER_TITLE)

    def is_footer_visible(self) -> bool:
        """Return True if the footer is visible."""
        return self.is_visible(self.FOOTER)
