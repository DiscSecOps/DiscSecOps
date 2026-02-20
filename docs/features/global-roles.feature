#features/global-roles.features
Feature: Global Roles
  As a platform administrator
  I want to manage users and content
  So that I can maintain platform health

  Background:
    Given the following users exist:
      | username   | global_role  |
      | super      | Super Admin  |
      | admin      | Admin        |
      | regular    | User         |

  @roles @smoke
  Scenario Outline: Login redirects based on global role
    Given a user exists with username "<username>" and global role "<role>"
    When I login with username "<username>" and password "pass123"
    Then I should be redirected to the <dashboard> page

    Examples:
      | role        | username   | dashboard           |
      | User        | regular    | UserDashboard       |
      | Admin       | admin      | AdminDashboard      |
      | Super Admin | super      | SuperAdminDashboard |

  @admin @critical
  Scenario: Admin can moderate content across platform
    Given I am logged in as admin
    When I access the admin panel
    Then I should see reported content
    And I should be able to:
      | action                 |
      | delete_reported_posts  |
      | warn_users             |
      | suspend_users          |

  @super_admin
  Scenario: Super Admin can manage all users
    Given I am logged in as super
    When I access the admin panel
    Then I should be able to:
      | action                 |
      | view_all_users         |
      | promote_user_to_admin  |
      | demote_admin_to_user   |
      | suspend_any_user       |
      | delete_any_circle      |

  @admin @security
  Scenario: Admin cannot manage other admins
    Given I am logged in as admin
    When I try to promote a user to admin
    Then I should see "Permission denied"
    
    When I try to demote another admin
    Then I should see "Permission denied"

  @security
  Scenario: Regular user cannot access admin panel
    Given I am logged in as regular
    When I try to access "/admin"
    Then I should see "404 Not Found" or "403 Forbidden"
    And I should be redirected to UserDashboard