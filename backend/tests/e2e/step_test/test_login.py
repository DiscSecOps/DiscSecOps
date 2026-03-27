# backend/tests/e2e/step_test/test_login.py
"""Login feature tests using Page Object Model."""

import pytest
from tests.e2e.pages.login_page import LoginPage
from pytest_bdd import scenarios, given,then, when
from tests.e2e.conftest import replace_variables

scenarios("login.feature")

# ==========================================
# GIVEN STEPS
# ==========================================
@given("I open the application")
def open_app(page):
    page.goto("/")


# ==========================================
# FIXTURES
# ==========================================
@pytest.fixture
def login_page(page):
    """Provide a LoginPage instance and navigate to login page."""
    lp = LoginPage(page)
    lp.goto()
    return lp


# ==========================================
# LOGIN STEPS
# ==========================================
@when('I login with username "<TEST_USERNAME>" and password "<TEST_PASSWORD>"')
def when_login_valid(login_page):
    login_page.login_as(
        username=replace_variables("<TEST_USERNAME>"),
        password=replace_variables("<TEST_PASSWORD>"),
    )


@when('I login with username "<TEST_USERNAME>" and password "testuserpass123!"')
def when_login_invalid_password(login_page):
    login_page.login_as(username=replace_variables("<TEST_USERNAME>"), password="testuserpass123!")


@when('I enter a blank username and password "<TEST_PASSWORD>"')
def when_enter_blank_username(login_page):
    login_page.password_input.fill(replace_variables("<TEST_PASSWORD>"))
    # leave username blank


@when('I enter username "<TEST_USERNAME>" and a blank password')
def when_enter_blank_password(login_page):
    login_page.username_input.fill(replace_variables("<TEST_USERNAME>"))
    # leave password blank


@then(
    'I should see "Password must be at least 8 characters and include uppercase, lowercase, number, and special character" error'
)
def then_see_password_error(login_page):
    login_page.expect_error_message(
        "Password must be at least 8 characters and include uppercase, lowercase, number, and special character"
    )