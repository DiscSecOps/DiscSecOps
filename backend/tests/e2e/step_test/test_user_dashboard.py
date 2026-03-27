# backend/tests/e2e/step_test/test_user_dashboard.py
from tests.e2e.pages.dashboard_page import DashboardPage
from pytest_bdd import given, scenarios, then, when
from tests.e2e.conftest import replace_variables

scenarios("user-dashboard.feature")


@given("I am on the dashboard")
def given_on_dashboard(page):
    dashboard = DashboardPage(page)
    dashboard.wait_for_dashboard()
    return dashboard


@when("I click Create New Circle")
def when_click_create_circle(given_on_dashboard):
    dashboard: DashboardPage = given_on_dashboard
    dashboard.click_create_circle()


@then('I should see my username "<TEST_USER>" in the navbar')
def then_see_username_navbar(given_on_dashboard):
    dashboard: DashboardPage = given_on_dashboard
    expected_username = replace_variables("<TEST_USERNAME>")
    username = dashboard.get_username()
    assert username == f"@{expected_username}", (
        f"Expected username '@{expected_username}', but got '{username}'"
    )
