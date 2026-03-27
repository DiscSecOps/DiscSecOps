Feature: User Registration 
  As a new user
  I want to create an account
  So that I can join Social Circles

  @ui @smoke  
  Scenario: Register page is accessible
    Given I open the application
    When I go to the register page
    Then I should see the registration form

  @ui @validation
  Scenario: Register button is disabled when form is empty
    Given I am on the registration page
    Then the register button should be disabled
    When I enter a username
    And I enter a full name
    And I enter an email
    And I enter a password
    And I enter a confirm password
    Then the registration button should be enabled

  @smoke @critical
  Scenario: Successful registration with valid data
    When I fill in the registration form with:
      | username   | <TEST_USERNAME> |
      | full_name  | <TEST_FULL_NAME>|
      | email      | <TEST_EMAIL>    |
      | password   | <TEST_PASSWORD> |
      | confirm    | <TEST_PASSWORD> |
    And I click the register button
    Then I should be redirected to the login page
    And I should see "Account created for <TEST_USER>! You can now login." message

  @security @validation
  Scenario: Registration fails with invalid email format (frontend validation)
    When I fill in the registration form with:
      | username   | validuser       |
      | full_name  | Valid User      |
      | email      | invalid-email   |
      | password   | <TEST_PASSWORD> |
      | confirm    | <TEST_PASSWORD> |
    And I click the register button
    Then I should see "Please enter a valid email address" error
    And I should remain on the registration page

  @security @validation
  Scenario: Registration fails with weak password (frontend validation)
    When I fill in the registration form with:
      | username   | validuser       |
      | full_name  | Valid User      |
      | email      | valid@test.com  |
      | password   | weak            |
      | confirm    | weak            |
    And I click the register button
    Then I should see "Password must be at least 8 characters" error
    And I should remain on the registration page

  @security @validation
  Scenario: Registration fails with password missing complexity (frontend validation)
    When I fill in the registration form with:
      | username   | validuser       |
      | full_name  | Valid User      |
      | email      | valid@test.com  |
      | password   | weakpass123     |
      | confirm    | weakpass123     |
    And I click the register button
    Then I should see "Password must be at least 8 characters and include uppercase, lowercase, number, and special character" error
    And I should remain on the registration page

  @security @validation
  Scenario: Registration fails with mismatched passwords
    When I fill in the registration form with:
      | username   | validuser       |
      | full_name  | Valid User      |
      | email      | valid@test.com  |
      | password   | <TEST_PASSWORD> |
      | confirm    | DifferentPass!  |
    And I click the register button
    Then I should see "Passwords do not match" error
    And I should remain on the registration page