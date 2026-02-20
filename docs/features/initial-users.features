Feature: Frontend - Initial Users & Authentication
  As a developer/tester
  I want to know the default credentials and login flows
  So that I can test the application with different roles

  Business Rules (Frontend):
    - Login page should work with all default accounts
    - First login for default accounts should redirect to change password
    - User should see their role-specific dashboard after login
    - Error messages should be user-friendly
    - Session management should work for all roles

  # ============================================
  # DEFAULT CREDENTIALS DOCUMENTATION
  # ============================================
  @documentation
  Scenario: Default credentials for testing
    Given the application is running in development mode
    Then the following default accounts are available for login:

    | Role        | Username  | Password (dev) | Dashboard          |
    |-------------|-----------|----------------|--------------------|
    | Super Admin | superadmin| [random]*      | SuperAdminDashboard|
    | Admin       | admin     | [random]*      | AdminDashboard     |
    | User        | user      | [random]*      | UserDashboard      |
    | Test User 1 | alice     | Test123!       | UserDashboard      |
    | Test User 2 | bob       | Test123!       | UserDashboard      |
    | Test User 3 | charlie   | Test123!       | UserDashboard      |
    | Test Admin  | mod_jane  | Test123!       | AdminDashboard     |

    *Note: Random passwords are displayed in console on first startup
    Check server logs for: "🔐 DEFAULT USER CREATED"

  # ============================================
  # LOGIN FLOWS FOR DEFAULT USERS
  # ============================================
  @smoke @critical
  Scenario Outline: Login with default test users
    Given I am on the login page
    When I enter username "<username>" and password "<password>"
    And I click the login button
    Then I should be redirected to the <dashboard>
    And I should see my username in the header
    And I should have a valid session cookie

    Examples:
      | username | password | dashboard           |
      | alice    | Test123! | UserDashboard       |
      | bob      | Test123! | UserDashboard       |
      | charlie  | Test123! | UserDashboard       |
      | mod_jane | Test123! | AdminDashboard      |

  @security @first-login
  Scenario: First login for random-password users requires password change
    Given a default account was created with random password
    And I have the credentials from console (username: "superadmin", password: "xyz123")
    When I login for the first time
    Then I should be redirected to "/change-password"
    And I should see a message "Please change your password before continuing"
    And I should not be able to access dashboard until password is changed
    
    When I enter new password "NewSecurePass123!" and confirm it
    And I click "Change Password"
    Then I should be redirected to SuperAdminDashboard
    And my session should be updated with the new credentials

  @security
  Scenario: User cannot bypass password change
    Given I have a default account that requires password change
    When I login
    And I try to navigate directly to "/dashboard"
    Then I should be redirected back to "/change-password"
    And I should see "You must change your password first"

  # ============================================
  # ROLE-SPECIFIC DASHBOARDS
  # ============================================
  @roles
  Scenario Outline: Users see correct dashboard based on role
    Given I am logged in as "<username>"
    Then the URL should be "/<dashboard>"
    And the header should show my role as "<display_role>"
    And I should see menu items specific to my role

    Examples:
      | username  | dashboard           | display_role |
      | superadmin| super-admin         | Super Admin  |
      | admin     | admin               | Admin        |
      | mod_jane  | admin               | Admin        |
      | alice     | dashboard           | User         |
      | user      | dashboard           | User         |

  @super-admin
  Scenario: Super Admin sees admin management options
    Given I am logged in as superadmin
    When I view the sidebar menu
    Then I should see:
      | menu_item           |
      | User Management     |
      | Admin Management    |
      | System Settings     |
      | All Circles         |
      | Platform Analytics  |

  @admin
  Scenario: Admin sees moderation options
    Given I am logged in as admin
    When I view the sidebar menu
    Then I should see:
      | menu_item           |
      | User Management     |
      | Moderation Queue    |
      | Reported Content    |
      | Platform Stats      |
    
    But I should NOT see:
      | menu_item           |
      | Admin Management    |
      | System Settings     |

  @user
  Scenario: Regular user sees their circles
    Given I am logged in as alice
    When I view the sidebar menu
    Then I should see:
      | menu_item           |
      | My Dashboard        |
      | My Circles          |
      | Discover Circles    |
      | Saved Posts         |
    
    But I should NOT see:
      | menu_item           |
      | User Management     |
      | Admin Management    |
      | System Settings     |

  # ============================================
  # SESSION MANAGEMENT
  # ============================================
  @session
  Scenario: Session persists after password change
    Given I changed my password successfully
    When I close and reopen the browser
    And I navigate to the app
    Then I should still be logged in
    And I should be on my dashboard

  @session
  Scenario: Logout works for all roles
    Given I am logged in as "<username>"
    When I click the logout button
    Then I should be redirected to the login page
    And my session cookie should be cleared
    And trying to access dashboard should redirect to login

    Examples:
      | username  |
      | superadmin|
      | admin     |
      | alice     |

  # ============================================
  # ERROR HANDLING
  # ============================================
  @security
  Scenario: Login with wrong password shows error
    Given I am on the login page
    When I enter username "alice" and password "wrongpassword"
    And I click login
    Then I should see "Invalid username or password"
    And I should remain on the login page
    And the password field should be cleared

  @security
  Scenario: Login with non-existent user shows same error
    Given I am on the login page
    When I enter username "nonexistent" and password "anypass"
    And I click login
    Then I should see "Invalid username or password"
    And I should remain on the login page

  # ============================================
  # FRONTEND STATE MANAGEMENT
  # ============================================
  @state
  Scenario: User data is stored in frontend state after login
    Given I login as "alice"
    Then the frontend state should contain:
      | field      | value        |
      | username   | alice        |
      | role       | user         |
      | isLoggedIn | true         |
    
    When I logout
    Then the frontend state should be cleared
    And all user data should be removed

  @state
  Scenario: Page refresh preserves login state
    Given I am logged in as "alice"
    When I refresh the page
    Then I should still be on UserDashboard
    And the frontend state should be restored from the session

  # ============================================
  # UI COMPONENTS FOR DIFFERENT ROLES
  # ============================================
  @ui
  Scenario: Header shows different options based on role
    Given I am logged in as "<username>"
    Then the header should show:
      | element            | visible? |
      | username           | yes      |
      | notifications icon | yes      |
      | settings icon      | yes      |
      | admin link         | <admin>  |

    Examples:
      | username  | admin |
      | superadmin| yes   |
      | admin     | yes   |
      | mod_jane  | yes   |
      | alice     | no    |

  # ============================================
  # DEVELOPMENT VS PRODUCTION BEHAVIOR
  # ============================================
  @environment
  Scenario: Warning about default accounts in production
    Given the application is running in production mode
    And default accounts exist
    When any user logs in
    Then the frontend should NOT display any default credentials
    And if a default account is used, there should be no special messages
    
  @environment
  Scenario: Development helpers are hidden in production
    Given the application is running in production
    When I view the login page
    Then I should NOT see any "Development Credentials" panel
    And I should NOT see "Test123!" or any default passwords displayed