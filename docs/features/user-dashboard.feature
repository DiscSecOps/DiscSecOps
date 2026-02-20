# features/user-dashboard-access-control.feature
Feature: User Dashboard
  As a logged-in user
  I want to see my dashboard
  So that I can access my circles and content

  @smoke
  Scenario: Dashboard displays user circles with correct roles
    Given a user "john_doe" exists
    And user "john_doe" is owner of circle "Family"
    And user "john_doe" is moderator of circle "Friends"
    And user "john_doe" is member of circle "Work"
    When I login as "john_doe"
    Then I should be on the UserDashboard
    And I should see in my circles list:
      | circle_name | role      | badge |
      | Family      | Owner     | 👑    |
      | Friends     | Moderator | 🛡️    |
      | Work        | Member    | 👤    |

  @smoke
  Scenario: Dashboard shows recent activity
    Given I am logged in as "john_doe"
    And there are recent posts in my circles
    When I view the dashboard
    Then I should see recent activity feed
    And I should see posts from my circles

  Scenario: Navigate to circle from dashboard
    Given I am logged in as "john_doe"
    And I am member of circle "Book Club"
    When I click on "Book Club" from dashboard
    Then I should be on the circle page