# backend/tests/e2e/step_test/test_registration.py
"""Registration feature tests using Page Object Model."""

import pytest
from tests.e2e.pages.registration_page import RegistrationPage
from pytest_bdd import scenarios, given,then, when
from tests.e2e.conftest import replace_variables

scenarios("registration.feature")

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
    """Provide a LoginPage instance and navigate to Registration page."""
    lp = RegistrationPage(page)
    lp.goto()
    return lp


# ==========================================
# REGISTRATION STEPS
# ==========================================


@when("I fill in the registration form with:")
def when_fill_registration_form(datatable, given_on_registration_page):
    """Fill the registration form with data from the feature file."""
    reg_page: RegistrationPage = given_on_registration_page
    data = dict(datatable)

    reg_page.register_as(
        username=replace_variables(data.get("username", "")),
        fullname=data.get("full_name", ""),  # Aici rămâne nemodificat
        email=replace_variables(data.get("email", "")),
        password=replace_variables(data.get("password", "")),
        confirm=replace_variables(data.get("confirm", "")),
    )


@then('I should see "Account created for <TEST_USERNAME>! You can now login." message')
def then_see_success_message(given_on_registration_page):
    reg_page: RegistrationPage = given_on_registration_page
    reg_page.expect_success_message(replace_variables("<TEST_USERNAME>"))


@when("I submit the form with invalid email")
def when_invalid_email(given_on_registration_page):
    reg_page: RegistrationPage = given_on_registration_page
    reg_page.register_as(
        username="testuser2",
        fullname="",
        email="invalid-email",
        password="Password123!",
        confirm="Password123!",
    )


@then('I should see "Please enter a valid email address" error')
def then_see_email_error(given_on_registration_page):
    reg_page: RegistrationPage = given_on_registration_page
    reg_page.expect_error_message("Please enter a valid email address")


@then('I should see "Password must be at least 8 characters" error')
def then_see_password_error(given_on_registration_page):
    reg_page: RegistrationPage = given_on_registration_page
    reg_page.expect_error_message("Password must be at least 8 characters")


@then(
    'I should see "Password must be at least 8 characters and include uppercase, lowercase, number, and special character" error'
)
def then_see_password_complexity_error(given_on_registration_page):
    reg_page: RegistrationPage = given_on_registration_page
    reg_page.expect_error_message(
        "Password must be at least 8 characters and include uppercase, lowercase, number, and special character"
    )


@then('I should see "Passwords do not match" error')
def then_see_password_mismatch_error(given_on_registration_page):
    reg_page: RegistrationPage = given_on_registration_page
    reg_page.expect_error_message("Passwords do not match")
