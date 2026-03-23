#feature/circle-context-in-feed.feature
Feature: Circle Context in Feed
  As a circle member
  I want to see which circle each post belongs to in my recent activity feed
  So that I can understand the context of each post

  Background:
    Given the following users exist:
      | username      |
      | john_doe      |
      | alice         |
      | bob           |
    
    And the following circles exist:
      | name         | owner     |
      | Family       | john_doe  |
      | Book Club    | alice     |
      | Gaming       | bob       |
    
    And the following circle memberships exist:
      | user         | circle        | role      |
      | john_doe     | Family        | owner     |
      | john_doe     | Book Club     | member    |
      | john_doe     | Gaming        | member    |
      | alice        | Book Club     | owner     |
      | bob          | Gaming        | owner     |
    
    And the following posts exist:
      | circle_name | author  | title              | content              |
      | Family      | john_doe| Weekend BBQ        | Bringing ribs!       |
      | Book Club   | alice   | Chapter 5 review   | Amazing plot twist!  |
      | Gaming      | bob     | New game release   | Check out this game  |
      | Book Club   | john_doe| My thoughts        | I loved chapter 4    |
    
    And I am logged in as "john_doe"
    And I navigate to the dashboard

  @feed @context @critical @todo
  Scenario: Recent activity feed shows circle name for each post
    Then I should see the recent activity feed
    And I should see the following posts with their circle context:
      | post              | circle_name | author  |
      | Weekend BBQ       | Family      | john_doe|
      | Chapter 5 review  | Book Club   | alice   |
      | New game release  | Gaming      | bob     |
      | My thoughts       | Book Club   | john_doe|
    
    And each post should display "in {circle_name}" under the post content

  @feed @ui
  Scenario: Circle names are displayed as clickable links
    Given I see a post from "Book Club" circle
    When I click on the circle name "Book Club"
    Then I should be redirected to the Book Club circle page

  @feed @filtering
  Scenario: Visual distinction between different circles
    Then posts from different circles should be visually distinct
    And posts from the same circle should have consistent styling
    When I look at two posts from "Book Club"
    Then they should share the same circle indicator style

  @feed @empty_state
  Scenario: Posts without circle (public posts) show no circle context
    Given a public post exists:
      | author  | title        | content         |
      | john_doe| Public post  | Hello everyone! |
    
    When I refresh the dashboard
    Then I should see the public post in my feed
    And the post should NOT display any circle name
    And the post should NOT have a circle indicator

  @feed @mobile @responsive
  Scenario: Circle context displays correctly on mobile devices
    When I view the dashboard on a mobile screen (width: 375px)
    Then the circle name should be displayed below the post content
    And it should not overflow or get cut off
    And it should be easily readable

  @feed @accessibility
  Scenario: Circle context is accessible to screen readers
    When I inspect a post from "Family" circle
    Then the circle indicator should have an aria-label
    And the label should say "Posted in Family circle"

  @feed @performance
  Scenario: Circle names load correctly with pagination
    Given there are 25 posts across different circles
    When I load the first page of the feed
    Then all displayed posts should show their correct circle names
    When I load more posts
    Then the new posts should also display their correct circle names