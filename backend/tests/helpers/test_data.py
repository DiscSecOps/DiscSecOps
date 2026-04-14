# backend/tests/helpers/test_data.py
"""
Test data constants and helpers for backend tests
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env.test")

# ============================================================================
# TEST CIRCLES
# ============================================================================

# Get usernames from environment
ALICE = os.getenv("ALICE_USERNAME", "alice")
BOB = os.getenv("BOB_USERNAME", "bob")
CHARLIE = os.getenv("CHARLIE_USERNAME", "charlie")

ALICE_PASSWORD = os.getenv("ALICE_PASSWORD", "AlicePass123!")
BOB_PASSWORD = os.getenv("BOB_PASSWORD", "BobPass123!")
CHARLIE_PASSWORD = os.getenv("CHARLIE_PASSWORD", "CharliePass123!")

TEST_CIRCLES = {
    "family": {
        "name": "Family",
        "description": "Family circle for sharing memories",
        "owner": ALICE,
        "members": [
            {"username": BOB, "password": BOB_PASSWORD, "role": "moderator"},
            {"username": CHARLIE, "password": CHARLIE_PASSWORD, "role": "member"},
        ],
    },
    "friends": {
        "name": "Friends",
        "description": "Close friends circle",
        "owner": ALICE,
        "members": [
            {"username": BOB, "password": BOB_PASSWORD, "role": "member"},
            {"username": CHARLIE, "password": CHARLIE_PASSWORD, "role": "member"},
        ],
    },
    "work": {
        "name": "Work",
        "description": "Work colleagues",
        "owner": ALICE,
        "members": [
            {"username": BOB, "password": BOB_PASSWORD, "role": "member"},
        ],
    },
}

# ============================================================================
# TEST POSTS
# ============================================================================

TEST_POSTS = {
    "family_welcome": {
        "circle": "Family",
        "author": ALICE,
        "title": "Welcome to Family Circle!",
        "content": "Welcome everyone! This is our family circle where we can share memories and stay connected.",
    },
    "friends_meetup": {
        "circle": "Friends",
        "author": ALICE,
        "title": "Weekend Meetup",
        "content": "Let's plan a get-together this weekend! What day works for everyone?",
    },
    "work_update": {
        "circle": "Work",
        "author": ALICE,
        "title": "Project Update",
        "content": "New project deadline is next Friday. Please submit your updates by Wednesday.",
    },
    "bob_family_post": {
        "circle": "Family",
        "author": BOB,
        "title": "Family Dinner",
        "content": "Anyone free for dinner this Sunday? Let me know!",
    },
    "charlie_friends_post": {
        "circle": "Friends",
        "author": CHARLIE,
        "title": "Movie Night",
        "content": "Anyone want to catch a movie this week?",
    },
    "public_post": {
        "circle": None,
        "author": ALICE,
        "title": "Hello Social Circles!",
        "content": "This is a public post visible to everyone. Welcome to the platform!",
    },
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def get_user(username: str) -> dict:
    """Get user data by username from environment variables"""

    key = username.upper()

    username_value = os.getenv(f"{key}_USERNAME")
    password_value = os.getenv(f"{key}_PASSWORD")
    email_value = os.getenv(f"{key}_EMAIL")

    if not username_value:
        raise ValueError(f"No user data found for username '{username}' in .env.test")

    return {
        "username": username_value,
        "password": password_value,
        "email": email_value,
        "full_name": os.getenv(f"{key}_FULL_NAME", username.capitalize()),
        "is_active": True,
    }


def get_circle(name: str) -> dict:
    """Get circle data by name"""
    for circle_data in TEST_CIRCLES.values():
        if circle_data.get("name") == name:
            return circle_data
    raise ValueError(f"Circle {name} not found in TEST_CIRCLES")


def get_post(title: str) -> dict:
    """Get post data by title"""
    for post_data in TEST_POSTS.values():
        if post_data.get("title") == title:
            return post_data
    raise ValueError(f"Post with title '{title}' not found in TEST_POSTS")


def get_user_by_role(role: str) -> dict:
    """Get user by role (owner, moderator, member)"""
    role_map = {
        "owner": "alice",
        "moderator": "bob",
        "member": "charlie",
    }
    username = role_map.get(role)
    if username:
        return get_user(username)
    raise ValueError(f"User with role {role} not found")
