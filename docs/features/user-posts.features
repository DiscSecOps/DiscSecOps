#features/user-posts.feature
Feature: Posts
  As a user of Social Circles
  I want to create and interact with posts
  So that I can share content and engage with my circles

  Business Rules:
    - Posts can be created in circles where user has Member+ role
    - Posts can be text, images, or links
    - Users can edit their own posts within 15 minutes
    - Users can delete their own posts anytime
    - Moderators and Owners can delete any post in their circle
    - Comments can be added to any post
    - Users can like posts (once per user)

  Background:
    Given the following users exist:
      | username | global_role |
      | alice    | User        |
      | bob      | User        |
      | charlie  | User        |
    And alice creates a circle called "Book Club"
    And alice adds bob as moderator of "Book Club"
    And alice adds charlie as member of "Book Club"

  # ============================================
  # CREATE POSTS
  # ============================================
  @smoke @critical
  Scenario: Member can create a text post in a circle
    Given I am logged in as charlie
    And I am on the "Book Club" circle page
    When I click on "Create Post"
    And I fill in:
      | title   | My Favorite Book      |
      | content | I just finished Dune! |
    And I click "Publish"
    Then I should see my post in the circle feed
    And I should see "Posted by charlie" on the post
    And I should see the current timestamp

  Scenario: Member can create a post with an image
    Given I am logged in as charlie
    When I create a new post in "Book Club"
    And I upload an image "book-cover.jpg"
    And I add caption "Check out this cover"
    And I click "Publish"
    Then I should see the image in my post
    And the image should be displayed correctly

  Scenario: Member can create a post with a link
    Given I am logged in as charlie
    When I create a new post in "Book Club"
    And I add a link "https://goodreads.com/book/dune"
    And I click "Publish"
    Then the link should be clickable
    And link preview should be generated

  @security
  Scenario: Non-member cannot create post in circle
    Given a user "dave" exists with no membership in "Book Club"
    When I am logged in as dave
    And I try to create a post in "Book Club"
    Then I should see "You don't have permission to post here"
    And the post form should not be visible

  @validation
  Scenario: Post requires content
    Given I am logged in as charlie
    When I try to create a post with empty content
    And I click "Publish"
    Then I should see "Post content cannot be empty"
    And the post should not be created

  # ============================================
  # VIEW POSTS
  # ============================================
  @smoke
  Scenario: User sees posts in circle feed
    Given the following posts exist in "Book Club":
      | author  | content              |
      | alice   | Welcome everyone!    |
      | bob     | Reading list for June |
    When I am logged in as charlie
    And I view the "Book Club" circle
    Then I should see both posts in the feed
    And posts should be ordered by newest first

  Scenario: User can view single post with details
    Given a post exists in "Book Club" by alice with content "Great book!"
    When I click on that post
    Then I should see the full post
    And I should see:
      | field        | value        |
      | author       | alice        |
      | circle       | Book Club    |
      | content      | Great book!  |
      | comments     | 0 comments   |
      | likes        | 0 likes      |

  # ============================================
  # EDIT POSTS
  # ============================================
  @edit
  Scenario: User can edit their own post within time limit
    Given I am logged in as charlie
    And I created a post 5 minutes ago with content "Original content"
    When I edit the post
    And I change content to "Updated content"
    And I click "Save"
    Then the post should show "Updated content"
    And the post should show "Edited" indicator

  @edit @security
  Scenario: User cannot edit post after 15 minutes
    Given I am logged in as charlie
    And I created a post 20 minutes ago
    When I try to edit the post
    Then the edit option should not be visible
    Or I should see "Edit window has expired"

  @edit @security
  Scenario: User cannot edit someone else's post
    Given a post exists by alice with content "Alice's post"
    When I am logged in as charlie
    And I try to edit alice's post
    Then I should not see an edit button
    And if I try to access edit URL directly, I should see "Permission denied"

  @edit
  Scenario: Moderator can edit any post in their circle
    Given a post exists by charlie with content "Charlie's post"
    When I am logged in as bob (moderator)
    And I edit charlie's post
    Then the edit should be successful
    And the post should show "Edited by moderator" indicator

  # ============================================
  # DELETE POSTS
  # ============================================
  @delete
  Scenario: User can delete their own post
    Given I am logged in as charlie
    And I created a post with content "My post"
    When I delete the post
    Then the post should no longer appear in the feed
    And I should see "Post deleted successfully" message

  @delete @security
  Scenario: Moderator can delete any post in their circle
    Given a post exists by charlie with content "Charlie's post"
    When I am logged in as bob (moderator)
    And I delete charlie's post
    Then the post should be removed
    And charlie should not see it anymore

  @delete @security
  Scenario: Owner can delete any post in their circle
    Given a post exists by bob with content "Bob's post"
    When I am logged in as alice (owner)
    And I delete bob's post
    Then the post should be removed

  @delete @security
  Scenario: Member cannot delete someone else's post
    Given a post exists by alice with content "Alice's post"
    When I am logged in as charlie (member)
    And I try to delete alice's post
    Then the delete option should not be visible
    And the post should still exist

  # ============================================
  # COMMENTS
  # ============================================
  @comments
  Scenario: User can comment on a post
    Given a post exists by alice with content "Great book!"
    When I am logged in as charlie
    And I add a comment "I agree, it's amazing!"
    And I click "Post Comment"
    Then I should see my comment under the post
    And I should see "commented by charlie"

  @comments
  Scenario: User can delete their own comment
    Given I am logged in as charlie
    And I commented "Nice post!" on alice's post
    When I delete my comment
    Then the comment should disappear
    And the comment count should decrease

  @comments @security
  Scenario: Moderator can delete any comment
    Given a comment exists by charlie on alice's post
    When I am logged in as bob (moderator)
    And I delete charlie's comment
    Then the comment should be removed

  @comments
  Scenario: User sees all comments on a post
    Given the following comments exist on alice's post:
      | author  | comment              |
      | bob     | Thanks for sharing!  |
      | charlie | I loved this book    |
    When I view the post
    Then I should see both comments
    And comments should be ordered by oldest first

  # ============================================
  # LIKES / REACTIONS
  # ============================================
  @likes
  Scenario: User can like a post
    Given a post exists by alice
    When I am logged in as charlie
    And I click the "Like" button on the post
    Then the like count should increase to 1
    And the button should show "Liked"

  @likes
  Scenario: User can unlike a post
    Given I am logged in as charlie
    And I previously liked alice's post
    When I click the "Liked" button
    Then the like count should decrease by 1
    And the button should show "Like"

  @likes @security
  Scenario: User cannot like a post twice
    Given I am logged in as charlie
    When I like alice's post
    And I try to like it again
    Then the like count should remain 1
    And I should see "Already liked" message

  @likes
  Scenario: User sees who liked a post
    Given alice's post has likes from bob and charlie
    When I view the post
    And I click on "2 likes"
    Then I should see a list with bob and charlie

  # ============================================
  # POST FEED & FILTERING
  # ============================================
  @feed
  Scenario: User sees feed from all their circles
    Given I am a member of:
      | circle      | role      |
      | Book Club   | Member    |
      | Gaming      | Member    |
    And posts exist in both circles
    When I am on the UserDashboard
    Then I should see a combined feed from all my circles
    And posts should be in chronological order

  @feed
  Scenario: User can filter feed by circle
    Given I am a member of multiple circles
    When I am on the UserDashboard
    And I select filter "Book Club"
    Then I should only see posts from "Book Club"

  @feed
  Scenario: User can search posts
    Given posts exist with content containing "Dune"
    When I search for "Dune"
    Then I should see all posts containing "Dune"
    And results should be relevant

  # ============================================
  # PINNED POSTS
  # ============================================
  @pinned
  Scenario: Moderator can pin a post
    Given I am logged in as bob (moderator)
    When I pin a post in "Book Club"
    Then the post should appear at the top of the feed
    And it should have a "📌 Pinned" indicator

  @pinned
  Scenario: Pinned posts appear first
    Given "Book Club" has:
      | post     | pinned |
      | Welcome  | yes    |
      | Event    | no     |
      | News     | no     |
    When I view the circle
    Then the pinned post "Welcome" should appear first
    Followed by other posts in chronological order

  # ============================================
  # POST REPORTING
  # ============================================
  @moderation
  Scenario: User can report inappropriate post
    Given I am logged in as charlie
    When I click "Report" on alice's post
    And I select reason "Inappropriate content"
    And I submit the report
    Then I should see "Post reported. Thank you."
    And moderators should see the report in moderation queue

  @moderation
  Scenario: Moderator can review reported posts
    Given a post by charlie has been reported
    When I am logged in as bob (moderator)
    And I view moderation queue
    Then I should see the reported post
    And I should have options to:
      | action           |
      | dismiss report   |
      | warn user        |
      | delete post      |

  # ============================================
  # POST ANALYTICS (for owners/admins)
  # ============================================
  @analytics
  Scenario: Owner sees post analytics
    Given I am logged in as alice (owner)
    When I view a post in my circle
    Then I should see:
      | metric        | value |
      | views         | 150   |
      | likes         | 12    |
      | comments      | 5     |
      | engagement    | 11%   |

  # ============================================
  # EDGE CASES
  # ============================================
  @edge
  Scenario: Post with very long content
    Given I am logged in as charlie
    When I create a post with 10,000 characters
    Then the post should be created successfully
    And it should be truncated in feed view with "Read more"

  @edge
  Scenario: Post with special characters
    Given I am logged in as charlie
    When I create a post with emojis and special chars: "🎉 Hello! 你好! مرحبا"
    Then the post should display correctly
    And all characters should render properly

  @edge
  Scenario: User cannot post in deleted circle
    Given circle "Book Club" has been deleted
    When I am logged in as charlie
    And I try to post in "Book Club"
    Then I should see "Circle not found"