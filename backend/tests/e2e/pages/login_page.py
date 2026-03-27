# backend/tests/e2e/pages/login_page.py
"""Page Object Model for Login page."""

from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.form = page.locator("form.login-form")
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.get_by_role("button", name="Login")
        self.register_link = page.get_by_text("Don't have an account? Register here")

    # ======================
    # PAGE LOAD / NAVIGATION
    # ======================
    def goto(self):
        self.page.goto("/login")
        self.page.wait_for_load_state("networkidle")
        expect(self.form).to_be_visible()

    # ======================
    # FORM ACTIONS
    # ======================
    def fill_username(self, username: str):
        self.username_input.fill(username)

    def fill_password(self, password: str):
        self.password_input.fill(password)

    def click_login(self):
        expect(self.login_button).to_be_enabled()
        self.login_button.click()

    def login_as(self, username: str, password: str):
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()

    def click_register_link(self):
        self.register_link.click()
        self.page.wait_for_load_state("networkidle")

    # ======================
    # ASSERTIONS
    # ======================
    def expect_login_button_enabled(self):
        expect(self.login_button).to_be_enabled()

    def expect_login_button_disabled(self):
        expect(self.login_button).to_be_disabled()

    def expect_form_visible(self):
        expect(self.form).to_be_visible()

    def expect_error_message(self, message: str):
        expect(self.page.get_by_text(message)).to_be_visible()
