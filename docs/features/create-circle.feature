Feature: Create Circle
  As a logged-in user
  I want to create a new circle
  So that I can collaborate with others

  Background:
    Given I am logged in as "<TEST_USERNAME>" with password "<TEST_PASSWORD>"
    And I am on the dashboard page

  @ui @create
  Scenario: Create circle from dashboard
    When I click the "Create New Circle" button
    Then I should see the create circle form
    When I fill in circle name "My Awesome Circle"
    And I fill in circle description "For testing purposes"
    And I click the "Create Circle" button
    Then I should see success message "Circle created successfully"
    And I should be on the circle page