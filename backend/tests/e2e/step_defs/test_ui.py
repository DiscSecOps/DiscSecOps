"""Authentication UI feature tests."""

from playwright.sync_api import Page, expect
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)


@scenario('ui.feature', 'Login button is disabled when form is empty')
def test_login_button_is_disabled_when_form_is_empty() -> None:
    """Login button is disabled when form is empty."""


@scenario('ui.feature', 'Login page is accessible')
def test_login_page_is_accessible() -> None:
    """Login page is accessible."""


@scenario('ui.feature', 'Register page is accessible')
def test_register_page_is_accessible() -> None:
    """Register page is accessible."""


@given('I am on the login page')
def verify_login_page(page: Page) -> None:
    go_to_login_directly(page)


@given('I open the application')
def open_app(page: Page) -> None:
    page.goto("/")


@when('I enter a password')
def enter_password(page: Page) -> None:
    page.locator('#password').fill("password123")


@when('I enter a username')
def enter_username(page: Page) -> None:
    page.locator('#username').fill("testuser")


@when('I go to the login page')
def go_to_login_directly(page: Page) -> None:
    page.goto("/login")


@when('I go to the register page')
def go_to_register_page(page: Page) -> None:
    page.goto("/register")


@then('I should see the login form')
def verify_login_form(page: Page) -> None:
    # We check for the heading and the presence of the submit button
    expect(page.get_by_role("heading", name="Login to Social Circles")).to_be_visible()
    expect(page.get_by_role("button", name="Login")).to_be_visible()


@then('I should see the registration form')
def verify_register_form(page: Page) -> None:
    expect(page.get_by_role("heading", name="Create Account")).to_be_visible()
    expect(page.get_by_role("button", name="Create Account")).to_be_visible()



@then('the login button should be disabled')
def check_login_button_disabled(page: Page) -> None:
    button = page.get_by_role("button", name="Login")
    expect(button).to_be_disabled()


@then('the login button should be enabled')
def check_login_button_enabled(page: Page) -> None:
    button = page.get_by_role("button", name="Login")
    expect(button).to_be_enabled()

