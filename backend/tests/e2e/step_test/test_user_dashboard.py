# backend/tests/e2e/step_test/test_user_dashboard.py

import re

import pytest
from pytest_bdd import given, scenarios, then

from tests.e2e.conftest import replace_variables
from tests.e2e.pages.dashboard_page import DashboardPage
from tests.e2e.pages.login_page import LoginPage

# ==========================================
# SCENARIOS
# ==========================================
scenarios("user-dashboard.feature")


# ==========================================
# FIXTURES
# ==========================================
@pytest.fixture
def dashboard_page(page):
    dp = DashboardPage(page)
    print("Simulating login...")
    return dp


# ==========================================
# GIVEN
# ==========================================
@given('I am logged in as "<TEST_USERNAME>" with password "<TEST_PASSWORD>"')
def given_logged_in_user(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login_as(
        username=replace_variables("<TEST_USERNAME>"), password=replace_variables("<TEST_PASSWORD>")
    )
    # Wait for navigation to dashboard after login
    page.wait_for_url(re.compile(r".*/user-dashboard$"), timeout=10000)


@given("I am on the dashboard page")
def on_dashboard_page(dashboard_page):
    dashboard_page.goto()  # navigatează la dashboard
    dashboard_page.expect_on_dashboard_page()  # verify elements specific to dashboard are visible


# ==========================================
# THEN
# ==========================================


@then('I should see a welcome message with "<TEST_USERNAME>!"')
def then_see_welcome_message(dashboard_page):
    username = replace_variables("<TEST_USERNAME>")
    dashboard_page.expect_welcome_section_visible(username)


@then("I should see the statistics section with circles and posts count")
def then_see_statistics(dashboard_page):
    dashboard_page.expect_stat_cards_visible()


@then('I should see a "Create New Circle" button')
def then_see_create_circle_button(dashboard_page):
    dashboard_page.expect_create_circle_btn_visible()


@then('I should see a "Create New Post" button')
def then_see_create_post_button(dashboard_page):
    dashboard_page.expect_create_post_btn_visible()


@then('I should see "You haven\'t joined any circles yet."')
def then_see_empty_circles(dashboard_page):
    dashboard_page.expect_empty_circles_state()


@then('I should see a "Create Your First Circle" button')
def then_see_first_circle_button(dashboard_page):
    dashboard_page.expect_empty_circles_state()


@then('I should see "No recent posts in your circles."')
def then_see_empty_posts(dashboard_page):
    dashboard_page.expect_empty_activity_message()
