"""
Shared test fixtures for the SauceDemo test suite.

Provides pre-configured page objects and an authenticated session fixture.
"""

import pytest
from playwright.sync_api import Page

from config.settings import settings
from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout_step_two_page import CheckoutStepTwoPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.product_detail_page import ProductDetailPage
from utils.helpers import get_valid_user


# ── Base URL fixture (required by pytest-playwright) ──────

@pytest.fixture(scope="session")
def base_url():
    """Provide the base URL for pytest-playwright."""
    return settings.BASE_URL


# ── Page Object fixtures ─────────────────────────────────

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Return a LoginPage instance bound to the current Playwright page."""
    return LoginPage(page)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    """Return an InventoryPage instance."""
    return InventoryPage(page)


@pytest.fixture
def product_detail_page(page: Page) -> ProductDetailPage:
    """Return a ProductDetailPage instance."""
    return ProductDetailPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    """Return a CartPage instance."""
    return CartPage(page)


@pytest.fixture
def checkout_step_one(page: Page) -> CheckoutStepOnePage:
    """Return a CheckoutStepOnePage instance."""
    return CheckoutStepOnePage(page)


@pytest.fixture
def checkout_step_two(page: Page) -> CheckoutStepTwoPage:
    """Return a CheckoutStepTwoPage instance."""
    return CheckoutStepTwoPage(page)


@pytest.fixture
def checkout_complete(page: Page) -> CheckoutCompletePage:
    """Return a CheckoutCompletePage instance."""
    return CheckoutCompletePage(page)


# ── Pre-authenticated session ─────────────────────────────

@pytest.fixture
def logged_in_page(page: Page, login_page: LoginPage, inventory_page: InventoryPage) -> Page:
    """
    Return a Playwright Page that is already logged in as standard_user.

    Use this fixture for any test that doesn't focus on login itself
    to avoid repeating the login flow.
    """
    user = get_valid_user("standard_user")
    login_page.open()
    login_page.login(user["username"], user["password"])
    inventory_page.wait_for(inventory_page.INVENTORY_LIST)
    return page
