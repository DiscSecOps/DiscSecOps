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

export const TEST_SEARCH = {
  validQuery: 'react',
  invalidQuery: '<script>',
  sqlInjection: "SELECT * FROM users"
};

