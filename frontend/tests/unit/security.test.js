// frontend/tests/unit/security.test.js
import { describe, it, expect, beforeEach } from 'vitest';
import { 
  validateUsername, 
  validateEmail, 
  validatePassword,
  validateSearchQuery,
  sanitizeInput,
  sanitizeUsername,
  sanitizeEmail,
  sanitizeSearchQuery,
  escapeHtml,
  escapeJsString,
  RateLimiter,
  loginRateLimiter,
  registerRateLimiter,
  searchRateLimiter,
  isInputSafe,
  getValidationErrorMessage
} from '../../src/utils/security';

describe('Security Utilities - Unit Tests', () => {
  
  // ==================== VALIDATION TESTS ====================
  
  describe('validateUsername', () => {
    it('should return true for valid usernames', () => {
      expect(validateUsername('john_doe')).toBe(true);
      expect(validateUsername('john123')).toBe(true);
      expect(validateUsername('JOHN_DOE')).toBe(true);
      expect(validateUsername('a'.repeat(3))).toBe(true); // min length
      expect(validateUsername('a'.repeat(30))).toBe(true); // max length
    });

    it('should return false for invalid usernames', () => {
      expect(validateUsername('')).toBe(false);
      expect(validateUsername('jo')).toBe(false); // too short
      expect(validateUsername('a'.repeat(31))).toBe(false); // too long
      expect(validateUsername('john@doe')).toBe(false); // invalid char
      expect(validateUsername('john doe')).toBe(false); // contains space
      expect(validateUsername('john-doe')).toBe(false); // contains dash
      expect(validateUsername('john.doe')).toBe(false); // contains dot
      expect(validateUsername(null)).toBe(false);
      expect(validateUsername(undefined)).toBe(false);
    });
  });

  describe('validateEmail', () => {
    it('should return true for valid emails', () => {
      expect(validateEmail('user@example.com')).toBe(true);
      expect(validateEmail('user.name@example.co.uk')).toBe(true);
      expect(validateEmail('user+tag@example.com')).toBe(true);
      expect(validateEmail('user123@example.io')).toBe(true);
    });

    it('should return false for invalid emails', () => {
      expect(validateEmail('')).toBe(false);
      expect(validateEmail('user@')).toBe(false);
      expect(validateEmail('user@domain')).toBe(false);
      expect(validateEmail('user')).toBe(false);
      expect(validateEmail('user@domain.')).toBe(false);
      expect(validateEmail('user@.com')).toBe(false);
      expect(validateEmail(null)).toBe(false);
    });
  });

  describe('validatePassword', () => {
    it('should return true for passwords >= 8 characters', () => {
      expect(validatePassword('SecurePass123!')).toBe(true);
      expect(validatePassword('Pass123!')).toBe(true); // 8 chars
      expect(validatePassword('P@ssw0rd')).toBe(true);
      expect(validatePassword('MyP@ssw0rd2024')).toBe(true);
    });

    it('should return false for passwords < 8 characters', () => {
      expect(validatePassword('')).toBe(false);
      expect(validatePassword('Pass123')).toBe(false); // 7 chars
      expect(validatePassword('Short1!')).toBe(false); // 7 chars
      expect(validatePassword(null)).toBe(false);
    });

    it('should return false for passwords without uppercase letter', () => {
    expect(validatePassword('password123!')).toBe(false);
    expect(validatePassword('pass123!')).toBe(false);
  });

  it('should return false for passwords without lowercase letter', () => {
    expect(validatePassword('PASSWORD123!')).toBe(false);
    expect(validatePassword('PASS123!')).toBe(false);
  });

  it('should return false for passwords without number', () => {
    expect(validatePassword('Password!')).toBe(false);
    expect(validatePassword('SecurePass!')).toBe(false);
  });

  it('should return false for passwords without special character', () => {
    expect(validatePassword('Password123')).toBe(false);
    expect(validatePassword('SecurePass123')).toBe(false);
  });
  });

  describe('validateSearchQuery', () => {
    it('should return true for valid search queries', () => {
      expect(validateSearchQuery('hello world')).toBe(true);
      expect(validateSearchQuery('react hooks')).toBe(true);
      expect(validateSearchQuery('user123')).toBe(true);
      expect(validateSearchQuery('a'.repeat(200))).toBe(true); // max length
    });

    it('should return false for SQL injection attempts', () => {
      expect(validateSearchQuery("SELECT * FROM users")).toBe(false);
      expect(validateSearchQuery("DROP TABLE users")).toBe(false);
      expect(validateSearchQuery("INSERT INTO users")).toBe(false);
      expect(validateSearchQuery("DELETE FROM users")).toBe(false);
      expect(validateSearchQuery("UNION SELECT")).toBe(false);
      expect(validateSearchQuery("'; --")).toBe(false);
    });

    it('should return false for XSS attempts', () => {
      expect(validateSearchQuery("<script>alert('xss')</script>")).toBe(false);
      expect(validateSearchQuery("javascript:alert('xss')")).toBe(false);
      expect(validateSearchQuery("onclick=alert('xss')")).toBe(false);
      expect(validateSearchQuery("onerror=alert('xss')")).toBe(false);
    });

    it('should return false for queries exceeding length limit', () => {
      const longQuery = 'a'.repeat(201);
      expect(validateSearchQuery(longQuery)).toBe(false);
    });

    it('should return false for empty queries', () => {
      expect(validateSearchQuery('')).toBe(false);
      expect(validateSearchQuery(null)).toBe(false);
    });
  });

  // ==================== SANITIZATION TESTS ====================

  describe('sanitizeInput', () => {
    it('should remove angle brackets', () => {
      expect(sanitizeInput('<script>alert("xss")</script>'))
        .toBe('scriptalert("xss")/script');
      expect(sanitizeInput('hello <world>')).toBe('hello world');
    });

    it('should trim whitespace', () => {
      expect(sanitizeInput('  hello  ')).toBe('hello');
      expect(sanitizeInput('\nhello\n')).toBe('hello');
    });

    it('should limit length to 500 characters', () => {
      const longString = 'a'.repeat(600);
      const result = sanitizeInput(longString);
      expect(result.length).toBe(500);
      expect(result).toBe('a'.repeat(500));
    });

    it('should handle null/undefined inputs', () => {
      expect(sanitizeInput(null)).toBe('');
      expect(sanitizeInput(undefined)).toBe('');
      expect(sanitizeInput('')).toBe('');
    });

    it('should handle non-string inputs', () => {
      expect(sanitizeInput(123)).toBe('');
      expect(sanitizeInput({})).toBe('');
    });
  });

  describe('sanitizeUsername', () => {
    it('should keep only alphanumeric and underscore', () => {
      expect(sanitizeUsername('john_doe123')).toBe('john_doe123');
      expect(sanitizeUsername('john@doe')).toBe('johndoe');
      expect(sanitizeUsername('john doe')).toBe('johndoe');
      expect(sanitizeUsername('john-doe')).toBe('johndoe');
      expect(sanitizeUsername('john.doe')).toBe('johndoe');
    });

    it('should handle empty inputs', () => {
      expect(sanitizeUsername('')).toBe('');
      expect(sanitizeUsername(null)).toBe('');
    });
  });

  describe('sanitizeEmail', () => {
    it('should trim whitespace and convert to lowercase', () => {
      expect(sanitizeEmail('  USER@EXAMPLE.COM  ')).toBe('user@example.com');
      expect(sanitizeEmail('John.Doe@Example.com')).toBe('john.doe@example.com');
    });

    it('should handle empty inputs', () => {
      expect(sanitizeEmail('')).toBe('');
      expect(sanitizeEmail(null)).toBe('');
    });
  });

  describe('sanitizeSearchQuery', () => {
    it('should remove dangerous characters', () => {
      expect(sanitizeSearchQuery('<script>test</script>')).toBe('scripttest/script');
      expect(sanitizeSearchQuery('hello <world>')).toBe('hello world');
    });

    it('should remove SQL patterns', () => {
      expect(sanitizeSearchQuery('SELECT * FROM users')).toBe(' * FROM users');
      expect(sanitizeSearchQuery('DROP TABLE users')).toBe(' TABLE users');
    });

    it('should limit length to 200', () => {
      const longQuery = 'a'.repeat(250);
      expect(sanitizeSearchQuery(longQuery).length).toBe(200);
    });
  });

  // ==================== ESCAPE TESTS ====================

  // tests/unit/security.test.js
  describe('escapeHtml', () => {
  it('should escape HTML special characters', () => {
    // Funcția escapează slash-ul doar în tag-urile de închidere
    expect(escapeHtml('<div>Hello</div>'))
      .toBe('&lt;div&gt;Hello&lt;&#x2F;div&gt;');
    expect(escapeHtml('"quote"')).toBe('&quot;quote&quot;');
    expect(escapeHtml("'quote'")).toBe('&#39;quote&#39;');
    expect(escapeHtml('a & b')).toBe('a &amp; b');
    expect(escapeHtml('hello/world')).toBe('hello&#x2F;world');
    });
  });

    it('should handle empty inputs', () => {
      expect(escapeHtml('')).toBe('');
      expect(escapeHtml(null)).toBe('');
    });
  });

  describe('escapeJsString', () => {
    it('should escape JavaScript special characters', () => {
      expect(escapeJsString("It's a test")).toBe("It\\'s a test");
      expect(escapeJsString('He said "hello"')).toBe('He said \\"hello\\"');
      expect(escapeJsString('back\\slash')).toBe('back\\\\slash');
    });
  });

  // ==================== RATE LIMITER TESTS ====================

  describe('RateLimiter', () => {
    let rateLimiter;

    beforeEach(() => {
      rateLimiter = new RateLimiter(3, 1000); // 3 attempts per second
    });

    it('should allow attempts within limit', () => {
      expect(rateLimiter.canAttempt()).toBe(true);
      expect(rateLimiter.canAttempt()).toBe(true);
      expect(rateLimiter.canAttempt()).toBe(true);
      expect(rateLimiter.canAttempt()).toBe(false); // 4th attempt fails
    });

    it('should calculate correct wait time', () => {
      for (let i = 0; i < 3; i++) {
        rateLimiter.canAttempt();
      }
      
      const waitTime = rateLimiter.getTimeToWait();
      expect(waitTime).toBeGreaterThan(0);
      expect(waitTime).toBeLessThanOrEqual(1000);
    });

    it('should reset attempts', () => {
      for (let i = 0; i < 3; i++) {
        rateLimiter.canAttempt();
      }
      expect(rateLimiter.canAttempt()).toBe(false);
      
      rateLimiter.reset();
      expect(rateLimiter.canAttempt()).toBe(true);
    });
  });

  describe('Pre-configured Rate Limiters', () => {
    it('should have login rate limiter with correct config', () => {
      expect(loginRateLimiter.limit).toBe(5);
      expect(loginRateLimiter.intervalMs).toBe(300000); // 5 minutes
    });

    it('should have register rate limiter with correct config', () => {
      expect(registerRateLimiter.limit).toBe(3);
      expect(registerRateLimiter.intervalMs).toBe(3600000); // 1 hour
    });

    it('should have search rate limiter with correct config', () => {
      expect(searchRateLimiter.limit).toBe(10);
      expect(searchRateLimiter.intervalMs).toBe(60000); // 1 minute
    });
  });

  // ==================== HELPER TESTS ====================

  describe('isInputSafe', () => {
    it('should return true for safe inputs', () => {
      expect(isInputSafe('hello world')).toBe(true);
      expect(isInputSafe('user123')).toBe(true);
    });

    it('should return false for unsafe inputs', () => {
      expect(isInputSafe('<script>alert("xss")</script>')).toBe(false);
      expect(isInputSafe('javascript:alert("xss")')).toBe(false);
      expect(isInputSafe('onclick=alert("xss")')).toBe(false);
    });
  });

  describe('getValidationErrorMessage', () => {
    it('should return correct error messages', () => {
      expect(getValidationErrorMessage('username', 'required')).toBe('Username is required');
      expect(getValidationErrorMessage('username', 'length')).toBe('Username must be 3-30 characters');
      expect(getValidationErrorMessage('email', 'format')).toBe('Please enter a valid email address');
      expect(getValidationErrorMessage('password', 'length')).toBe('Password must be at least 8 characters');
      expect(getValidationErrorMessage('search', 'query')).toBe('Invalid search query');
      expect(getValidationErrorMessage('unknown', 'unknown')).toBe('Invalid input');
    });
  });
