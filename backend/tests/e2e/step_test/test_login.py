# backend/tests/e2e/step_test/test_login.py
"""Login feature tests using Page Object Model."""

import re

import pytest
from playwright.sync_api import expect
from pytest_bdd import given, scenarios, then, when

from tests.e2e.conftest import replace_variables
from tests.e2e.pages.login_page import LoginPage

# ==========================================
# SCENARIOS
# ==========================================
scenarios("login.feature")


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
# GIVEN STEPS
# ==========================================
@given("I open the application and I am not logged in")
def open_app(page):
    base_url = replace_variables("<FRONTEND_URL>")
    page.goto(base_url)


@given("I am on the login page")
def given_on_login_page(login_page):
    login_page.expect_form_visible()


# ==========================================
# WHEN STEPS
# ==========================================
@when("I go to the login page")
def go_to_login_page(login_page):
    login_page.goto()


@when("I enter a username")
def enter_username(login_page):
    username = replace_variables("<TEST_USERNAME>")
    login_page.fill_username(username)


@when("I enter a password")
def enter_password(login_page):
    password = replace_variables("<TEST_PASSWORD>")
    login_page.fill_password(password)


@when('I enter a blank username and password "<TEST_PASSWORD>"')
def blank_username(login_page):
    login_page.password_input.fill(replace_variables("<TEST_PASSWORD>"))
    login_page.username_input.fill("")


@when('I enter username "<TEST_USERNAME>" and a blank password')
def blank_password(login_page):
    login_page.username_input.fill(replace_variables("<TEST_USERNAME>"))
    login_page.password_input.fill("")


@when('I login with username "<TEST_USERNAME>" and password "<TEST_PASSWORD>"')
def when_login_valid(login_page):
    login_page.login_as(
        username=replace_variables("<TEST_USERNAME>"), password=replace_variables("<TEST_PASSWORD>")
    )


@when('I login with username "<TEST_USERNAME>" and password "testuserpass123!"')
def when_login_invalid_password(login_page):
    login_page.login_as(username=replace_variables("<TEST_USERNAME>"), password="testuserpass123!")


@when('I click the "Register here" link')
def click_register_link(login_page):
    login_page.click_register_link()


# ==========================================
# THEN STEPS
# ==========================================
@then("I should see the login form")
def then_see_login_form(login_page):
    login_page.expect_form_visible()


@then("I should see a link to register")
def then_see_register_link(login_page):
    expect(login_page.register_link).to_be_visible()


@then("the login button should be disabled")
def login_button_disabled(login_page):
    login_page.expect_login_button_disabled()


@then("the login button should be enabled")
def login_button_enabled(login_page):
    login_page.expect_login_button_enabled()


@then(
    'I should see "Password must be at least 8 characters and include uppercase, lowercase, number, and special character" error'
)
def then_see_password_error(login_page):
    login_page.expect_error_message(
        "Password must be at least 8 characters and include uppercase, lowercase, number, and special character"
    )


@then("I should be redirected to the register page")
def check_register_page(login_page):
    login_page.page.wait_for_load_state("networkidle")
    assert re.search(r"/register$", login_page.page.url), (
        f"Expected /register, got {login_page.page.url}"
    )


@then("I should remain on the login page")
def remain_on_login_page(login_page):
    login_page.page.wait_for_load_state("networkidle")
    assert re.search(r"/login$", login_page.page.url), f"Expected /login, got {login_page.page.url}"
    login_page.expect_form_visible()
