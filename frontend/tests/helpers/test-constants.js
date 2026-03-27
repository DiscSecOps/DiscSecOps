// frontend/tests/helpers/test-constants.js

export const TEST_USERS = {
  validUser: {
    username: 'john_doe',
    email: 'john@example.com',
    password: 'SecurePass123!',
    fullName: 'John Doe'
  },
  wrongPassword: {
    username: 'john_doe',
    password: 'WrongPass123!'
  },
  invalidUser: {
    username: 'unknown_user',
    password: 'anypass'
  },
  caseInsensitiveUser: {
    username: 'JOHN_DOE',
    password: 'SecurePass123!'
  },
  newUser: {
    username: 'newuser',
    email: 'newuser@example.com',
    password: 'NewUserPass123!',
    fullName: 'New User'
  },
  // New test users for circle membership tests
  alice: {
    id: 1,
    username: 'alice',
    email: 'alice@example.com',
    password: 'AlicePass123!',
    fullName: 'Alice Smith'
  },
  bob: {
    id: 2,
    username: 'bob',
    email: 'bob@example.com',
    password: 'BobPass123!',
    fullName: 'Bob Johnson'
  },
  charlie: {
    id: 3,
    username: 'charlie',
    email: 'charlie@example.com',
    password: 'CharliePass123!',
    fullName: 'Charlie Brown'
  }
};

export const TEST_VALIDATION = {
  shortUsername: 'jo',
  longUsername: 'a'.repeat(31),
  invalidUsername: 'john@doe',
  shortPassword: '1234567',
  validPassword: 'SecurePass123!',
  invalidEmail: 'invalid-email',
  validEmail: 'test@example.com'
};

export const TEST_MEMBERS = {
  // Alice is not a member of any circle, Bob is a member of Family and Friends, Charlie is a member of Work
  alice: {
    id: TEST_USERS.alice.id,
    username: TEST_USERS.alice.username,
    email: TEST_USERS.alice.email,
    is_already_member: false  
  },
  bob: {
    id: TEST_USERS.bob.id,
    username: TEST_USERS.bob.username,
    email: TEST_USERS.bob.email,
    is_already_member: false
  },
  charlie: {
    id: TEST_USERS.charlie.id,
    username: TEST_USERS.charlie.username,
    email: TEST_USERS.charlie.email,
    is_already_member: false
  },
  // For compatibility with existing tests, we can also define aliases
  existingMember: {
    id: TEST_USERS.alice.id,
    username: TEST_USERS.alice.username,
    email: TEST_USERS.alice.email,
    is_already_member: true
  },
  // aliases for non-member and new member
  nonMember: {
    id: TEST_USERS.bob.id,
    username: TEST_USERS.bob.username,
    email: TEST_USERS.bob.email,
    is_already_member: false
  },
  newMember: {
    id: TEST_USERS.charlie.id,
    username: TEST_USERS.charlie.username,
    email: TEST_USERS.charlie.email,
    is_already_member: false
  }
};

export const TEST_CIRCLES = {
  testCircleId: 1,  // id of the circle used in tests
  familyCircle: {
    id: 1,
    name: 'Family',
    owner: TEST_USERS.alice.username,
    members: [TEST_USERS.bob.username, TEST_USERS.charlie.username]
  },
  friendsCircle: {
    id: 2,
    name: 'Friends',
    owner: TEST_USERS.alice.username,
    members: [TEST_USERS.bob.username, TEST_USERS.charlie.username]
  },
  workCircle: {
    id: 3,
    name: 'Work',
    owner: TEST_USERS.alice.username,
    members: [TEST_USERS.bob.username]
  }
};

export const TEST_SEARCH = {
  validQuery: 'react',
  invalidQuery: '<script>',
  sqlInjection: "SELECT * FROM users"
};