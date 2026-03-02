Feature: User Dashboard
  As a logged-in user
  I want to see my dashboard
  So that I can access my circles and content

  Background:
    # 1. Standardize the user setup
    Given a user exists with username "john_doe" and password "SecurePass123!"
    And I am logged in as "john_doe"
    
    # 2. Consolidate the database seeding into ONE step using a Data Table!
    And the user "john_doe" belongs to the following circles:
      | circle_name | role      |
      | Family      | owner     |
      | Friends     | moderator |
      | Work        | member    |
      | Book Club   | member    |
    
    And the following posts exist in the circles:
      | circle_name | author       | title              | content                        |
      | Family      | john_doe     | Weekend BBQ        | Bringing ribs and potato salad |
      | Book Club   | john_doe     | Chapter 4 thoughts | That plot twist was crazy!     |
      | Book Club   | circle_admin | Chapter 5 thoughts | The ending was unexpected!     |
      | Work        | circle_admin | Project Update     | Final report is due next week  |
      | Work        | john_doe     | Meeting Notes      | Discussed project milestones   |
      | Work        | john_doe     | New Idea           | Let's try a new approach!      |
      
    # 3. Move the navigation here since all tests need it
    And I navigate to the dashboard

  @smoke @ui @bug
  Scenario: Dashboard displays user circles with correct roles and badges
    # Notice how we skip straight to 'Then' because 'When' is now in the Background
    Then I should see the following in my circles list:
      | circle_name | role      | badge |
      | Family      | owner     | 👑    |
      | Friends     | moderator | 🛡️    |
      | Work        | member    | 👤    |
      | Book Club   | member    | 👤    |

  @smoke @content
  Scenario: Dashboard shows recent activity feed
    Then I should see the recent activity feed
    And I should see posts from the "Family" circle

  @navigation
  Scenario: Navigate to a circle from the dashboard
    When I click on the "Book Club" circle card
    Then I should be redirected to the circle page for "Book Club"