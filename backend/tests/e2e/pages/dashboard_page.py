# backend/tests/e2e/pages/dashboard_page.py
"""Page Object Model for the Dashboard page."""

from playwright.sync_api import Page, expect


class DashboardPage:
    def __init__(self, page: Page):
        self.page = page
        self.main = page.locator("main.dashboard-main")
        self.navbar = page.locator("header.navbar")
        self.sidebar = page.locator("aside.sidebar")
        self.welcome_section = page.locator(".welcome-section")
        self.stats_grid = page.locator(".stats-grid")
        self.circles_section = page.locator(".circles-section")
        self.feed_section = page.locator(".feed-section")

        # Navbar elements
        self.nav_user_name = self.navbar.locator(".navbar-user .user-name")
        self.search_input = self.navbar.get_by_placeholder("Search circles, posts, people...")
        self.notifications_badge = self.navbar.locator(".navbar-right .badge")
        self.dark_mode_btn = self.navbar.get_by_title("Switch to Dark Mode")
        self.notifications_btn = self.navbar.get_by_title("Notifications")
        self.messages_btn = self.navbar.get_by_title("Messages")

        # Sidebar buttons
        self.dashboard_btn = self.sidebar.get_by_role("button", name="Dashboard")
        self.search_btn = self.sidebar.get_by_role("button", name="Search")
        self.settings_btn = self.sidebar.get_by_role("button", name="Settings")
        self.help_btn = self.sidebar.get_by_role("button", name="Help")

        # Action buttons
        self.create_circle_btn = self.main.get_by_role("button", name="+ Create New Circle")
        self.create_post_btn = self.main.get_by_role("button", name="Create New Post")

    # ======================
    # PAGE LOAD / WAITERS
    # ======================
    def wait_for_dashboard(self):
        expect(self.main).to_be_visible()
        expect(self.sidebar).to_be_visible()
        expect(self.navbar).to_be_visible()

    def goto(self):
        """Navigate to the dashboard page and wait for the page to load."""
        self.page.goto("/user-dashboard")
        self.wait_for_dashboard()

    # ======================
    # NAVBAR ACTIONS
    # ======================
    def search(self, query: str):
        self.search_input.fill(query)
        self.search_input.press("Enter")

    def get_username(self) -> str:
        return self.nav_user_name.text_content()

    # ======================
    # DASHBOARD ACTIONS
    # ======================
    def click_create_circle(self):
        expect(self.create_circle_btn).to_be_enabled()
        self.create_circle_btn.click()

    def click_create_post(self):
        expect(self.create_post_btn).to_be_enabled()
        self.create_post_btn.click()

    # ======================
    # ASSERTIONS
    # ======================
    def expect_welcome_section_visible(self):
        expect(self.welcome_section).to_be_visible()

    def expect_empty_circles_state(self):
        empty_state = self.circles_section.locator(".empty-state")
        expect(empty_state).to_be_visible()
        expect(empty_state.locator("button")).to_be_enabled()

    def expect_empty_activity_message(self):
        empty_msg = self.feed_section.locator(".empty-message")
        expect(empty_msg).to_be_visible()
        expect(empty_msg.locator("button")).to_be_enabled()

    def expect_notifications_count_visible(self):
        expect(self.notifications_badge).to_be_visible()
