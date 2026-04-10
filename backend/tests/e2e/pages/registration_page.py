# backend/tests/e2e/pages/registration_page.py
"""Page Object Model for Registration page."""

import os
import re

from playwright.sync_api import Page, expect


class RegistrationPage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.get_by_role("heading", name="Create Account")
        self.form = page.locator("form.register-form")
        self.username_input = page.locator("#username")
        self.fullname_input = page.locator("#fullName")
        self.email_input = page.locator("#email")
        self.password_input = page.locator("#password")
        self.confirm_input = page.locator("#confirmPassword")
        self.register_button = page.get_by_role("button", name="Create Account")
        self.login_link = page.locator(".register-links").get_by_role("link", name="Login here")
        self.base_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

    # ======================
    # PAGE LOAD / NAVIGATION
    # ======================
    def goto(self):
        self.page.goto(f"{self.base_url}/register")
        self.page.wait_for_load_state("networkidle")
        expect(self.form).to_be_visible()
        assert self.page.url.endswith("/register"), f"Expected /register, got {self.page.url}"

    # ======================
    # FORM ACTIONS
    # ======================
    def expect_title_visible(self):
        expect(self.title).to_be_visible()

    def fill_username(self, username: str):
        self.username_input.fill(username)

    def fill_fullname(self, fullname: str):
        self.fullname_input.fill(fullname)

    def fill_email(self, email: str):
        self.email_input.fill(email)

    def fill_password(self, password: str):
        self.password_input.fill(password)

    def fill_confirm_password(self, confirm: str):
        self.confirm_input.fill(confirm)

    def click_register(self):
        expect(self.register_button).to_be_enabled()
        self.register_button.click()

    def register_as(self, username: str, fullname: str, email: str, password: str, confirm: str):
        self.fill_username(username)
        if fullname:
            self.fill_fullname(fullname)
        self.fill_email(email)
        self.fill_password(password)
        self.fill_confirm_password(confirm)
        self.click_register()

    def click_login_link(self):
        self.login_link.click()
        expect(self.page).to_have_url(re.compile(r".*/login$"))
        expect(self.page.get_by_role("heading", name="Login")).to_be_visible()

    # ======================
    # ASSERTIONS
    # ======================
    def expect_form_visible(self):
        expect(self.form).to_be_visible()

    def expect_register_button_enabled(self):
        expect(self.register_button).to_be_enabled()

    def expect_register_button_disabled(self):
        expect(self.register_button).to_be_disabled()

    def expect_success_message(self, username: str):
        message = f"Account created for {username}! You can now login."
        expect(self.page.get_by_text(message)).to_be_visible()

    def expect_error_for_email(self):
        expect(self.page.locator("#email-error")).to_be_visible()

    def expect_error_for_confirm_password(self):
        expect(self.page.locator("#confirm-password-error")).to_be_visible()

    def expect_error_message(self, message: str):
        expect(self.page.get_by_text(message)).to_be_visible()

    def expect_redirect_to_login(self):
        expect(self.page).to_have_url(re.compile(r".*/login$"))
        expect(self.page.get_by_role("heading", name="Login")).to_be_visible()

    def expect_on_register_page(self):
        expect(self.page).to_have_url(re.compile(r".*/register$"))
        self.expect_form_visible()
