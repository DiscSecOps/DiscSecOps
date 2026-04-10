Feature: Create Post
  As a logged-in user
  I want to create a post in a circle
  So that I can share content

  Background:
    Given I am logged in as "<TEST_USERNAME>" with password "<TEST_PASSWORD>"
    And I am on the dashboard page

  @ui @create
  Scenario: Create post from dashboard
    When I click the "Create New Post" button
    Then I should see the create post form
    When I select a circle "My Awesome Circle"
    And I fill in post title "Important update"
    And I fill in post content "This is my first post"
    And I click the "Create Post" button
    Then I should see success message "Post created successfully"