# frontend/tests/e2e/feature/user-dashboard.feature

Feature: User Dashboard
  As a logged-in user
  I want to view my dashboard
  So that I can see my circles, posts, and notifications

  Background:
    Given I am logged in as "<TEST_USERNAME>" with password "<TEST_PASSWORD>"
    And I am on the dashboard page

  @ui @smoke
  Scenario: Dashboard is accessible and displays key elements
    Then I should see a welcome message with "<TEST_USERNAME>!"
    And I should see the statistics section with circles and posts count
    And I should see a "Create New Circle" button
    And I should see a "Create New Post" button

  @ui @critical
  Scenario: Dashboard shows empty state when no circles or posts
    Then I should see "You haven't joined any circles yet."
    And I should see a "Create Your First Circle" button
    And I should see "No recent posts in your circles."

  