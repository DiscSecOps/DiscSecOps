"""Registration feature tests using Page Object Model."""

import pytest
from playwright.sync_api import expect
from pytest_bdd import given, scenarios, then, when

from tests.e2e.conftest import replace_variables
from tests.e2e.pages.registration_page import RegistrationPage

# ==========================================
# SCENARIOS
# ==========================================
scenarios("registration.feature")


# ==========================================
# FIXTURES
# ==========================================
@pytest.fixture
def register_page(page):
    rp = RegistrationPage(page)
    rp.goto()
    return rp


# ==========================================
# GIVEN
# ==========================================


@given("I open the application and I am not logged in")
def open_app(page):
    base_url = replace_variables("<FRONTEND_URL>")
    page.goto(base_url)


@given("I am on the register page")
def on_register_page(register_page):
    register_page.expect_form_visible()


# ==========================================
# WHEN
# ==========================================
@when("I enter a username")
def enter_username(register_page):
    register_page.fill_username(replace_variables("<TEST_USERNAME>"))


@when("I enter an email")
def enter_email(register_page):
    register_page.fill_email(replace_variables("<TEST_EMAIL>"))


@when("I enter an invalid email")
def enter_invalid_email(register_page):
    register_page.fill_email("invalid-email")


@when("I enter a password")
def enter_password(register_page):
    register_page.fill_password(replace_variables("<TEST_PASSWORD>"))


@when("I enter a confirm password")
def enter_confirm_password(register_page):
    register_page.fill_confirm_password(replace_variables("<TEST_PASSWORD>"))


@when("I enter a different confirm password")
def enter_different_confirm(register_page):
    register_page.fill_confirm_password("DifferentPass123!")


@when('I click the "Create Account" button')
def click_register(register_page):
    register_page.click_register()


@when('I click the "Login here" link')
def click_login_link(register_page):
    register_page.click_login_link()


# ==========================================
# THEN
# ==========================================
@then('I should see the "Create Account" title')
def see_title(register_page):
    register_page.expect_title_visible()


@then("I should see the registration form")
def see_form(register_page):
    register_page.expect_form_visible()


@then('I should see a "Login here" link')
def see_login_link(register_page):
    expect(register_page.login_link).to_be_visible()


@then('the "Create Account" button should be disabled')
def button_disabled(register_page):
    register_page.expect_register_button_disabled()


@then('the "Create Account" button should be enabled')
def button_enabled(register_page):
    register_page.expect_register_button_enabled()


@then("I should be redirected to the login page")
def redirected_to_login(register_page):
    register_page.expect_redirect_to_login()


@then("I should see an email error message")
def email_error(register_page):
    register_page.expect_error_for_email()


@then("I should see a confirm password error message")
def confirm_password_error(register_page):
    register_page.expect_error_for_confirm_password()


@then("I should remain on the register page")
def remain_on_register(register_page):
    register_page.expect_on_register_page()
