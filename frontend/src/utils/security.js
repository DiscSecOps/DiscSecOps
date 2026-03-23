// frontend/src/utils/security.js

/**
 * Security Utilities for Input Validation, Sanitization, and XSS Prevention
 * Used across authentication (login/register) and search functionality
 */

// ==================== VALIDATION FUNCTIONS ====================

/**
 * Validates username format
 * Rules: 3-30 characters, only letters, numbers, and underscores
 * @param {string} username - The username to validate
 * @returns {boolean} - True if valid, false otherwise
 */
export const validateUsername = (username) => {
  if (!username) return false;
  if (username.length < 3 || username.length > 30) return false;
  if (!/^[a-zA-Z0-9_]+$/.test(username)) return false;
  return true;
};

/**
 * Validates email format using regex pattern
 * @param {string} email - The email to validate
 * @returns {boolean} - True if valid email format, false otherwise
 */
export const validateEmail = (email) => {
  if (!email) return false;
  // Basic email format validation
  const emailRegex = /^[^\s@]+@([^\s@]+\.)+[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Validates password strength on frontend (basic validation)
 * Note: Full password complexity should be enforced on backend
 * @param {string} password - The password to validate
 * @returns {boolean} - True if password meets minimum requirements
 */
export const validatePassword = (password) => {
  if (!password) return false;
  
  // Minimum length check
  if (password.length < 8) return false;
  
  // At least one uppercase letter
  if (!/[A-Z]/.test(password)) return false;
  
  // At least one lowercase letter
  if (!/[a-z]/.test(password)) return false;
  
  // At least one number
  if (!/[0-9]/.test(password)) return false;
  
  // At least one special character
  if (!/[!@#$%^&*]/.test(password)) return false;
  
  return true;
};

/**
 * Validates search query to prevent injection attempts
 * @param {string} query - The search query to validate
 * @returns {boolean} - True if query is safe and within limits
 */
export const validateSearchQuery = (query) => {
  if (!query) return false;
  // Limit query length to prevent DoS attacks
  if (query.length > 200) return false;
  
  // Block common SQL injection patterns
  const sqlPatterns = /(\bSELECT\b|\bINSERT\b|\bUPDATE\b|\bDELETE\b|\bDROP\b|\bUNION\b|\b--\b|;)/i;
  if (sqlPatterns.test(query)) return false;
  
  // Block XSS patterns
  const xssPatterns = /(<script|javascript:|onclick|onerror|onload|onmouseover)/i;
  if (xssPatterns.test(query)) return false;
  
  return true;
};

// ==================== SANITIZATION FUNCTIONS ====================

/**
 * General input sanitizer - removes dangerous characters
 * Use before sending data to backend
 * @param {string} input - The input string to sanitize
 * @returns {string} - Sanitized string safe for transmission
 */
export const sanitizeInput = (input) => {
  if (!input || typeof input !== 'string') return '';
  
  // Trim whitespace
  let sanitized = input.trim();
  
  // Prevent DoS by limiting length
  if (sanitized.length > 500) {
    sanitized = sanitized.substring(0, 500);
  }
  
  // Remove angle brackets to prevent HTML injection
  sanitized = sanitized.replace(/[<>]/g, '');
  
  return sanitized;
};

/**
 * Specialized username sanitizer - only allows alphanumeric and underscore
 * @param {string} username - The username to sanitize
 * @returns {string} - Cleaned username
 */
export const sanitizeUsername = (username) => {
  if (!username) return '';
  // Keep only letters, numbers, and underscores
  return username.replace(/[^a-zA-Z0-9_]/g, '');
};

/**
 * Sanitizes email address - removes whitespace and converts to lowercase
 * @param {string} email - The email to sanitize
 * @returns {string} - Sanitized email
 */
export const sanitizeEmail = (email) => {
  if (!email) return '';
  return email.trim().toLowerCase();
};

/**
 * Sanitizes search query - removes dangerous characters and limits length
 * @param {string} query - The search query to sanitize
 * @returns {string} - Sanitized query safe for search
 */
export const sanitizeSearchQuery = (query) => {
  if (!query) return '';
  
  let sanitized = query.trim();
  
  // Limit length
  if (sanitized.length > 200) {
    sanitized = sanitized.substring(0, 200);
  }
  
  // Remove dangerous characters
  sanitized = sanitized.replace(/[<>]/g, '');
  
  // Remove SQL injection patterns
  sanitized = sanitized.replace(/(\bSELECT\b|\bINSERT\b|\bUPDATE\b|\bDELETE\b|\bDROP\b|\bUNION\b)/gi, '');
  
  return sanitized;
};

// ==================== OUTPUT ESCAPING ====================

/**
 * Escape HTML special characters to prevent XSS when displaying user-generated content
 * Use when rendering any user input or data from API
 * @param {string} text - The text to escape
 * @returns {string} - HTML-escaped text safe for rendering
 */
export const escapeHtml = (text) => {
  if (!text) return '';
  
  const htmlEscapeMap = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
    '/': '&#x2F;',
    '`': '&#x60;',
    '=': '&#x3D;'
  };
  
  return String(text).replace(/[&<>"'/`=]/g, (char) => htmlEscapeMap[char]);
};

/**
 * Escape content for use in JavaScript strings (prevents injection)
 * @param {string} text - The text to escape for JS
 * @returns {string} - JS-safe string
 */
export const escapeJsString = (text) => {
  if (!text) return '';
  return text.replace(/[\\'"]/g, (char) => {
    if (char === '\\') return '\\\\';
    if (char === "'") return "\\'";
    if (char === '"') return '\\"';
    return char;
  });
};

// ==================== RATE LIMITING UTILITY ====================

/**
 * Rate limiter class for UI-level throttling
 * Note: This is UI-only, backend should have its own rate limiting
 */
export class RateLimiter {
  constructor(limit = 5, intervalMs = 60000) {
    this.limit = limit;           // Maximum attempts allowed
    this.intervalMs = intervalMs; // Time window in milliseconds
    this.attempts = [];           // Timestamps of attempts
  }

  /**
   * Check if a new attempt is allowed
   * @returns {boolean} - True if attempt is allowed, false if rate limited
   */
  canAttempt() {
    const now = Date.now();
    // Remove attempts outside the time window
    this.attempts = this.attempts.filter(timestamp => now - timestamp < this.intervalMs);
    
    if (this.attempts.length < this.limit) {
      this.attempts.push(now);
      return true;
    }
    return false;
  }

  /**
   * Get time remaining until next allowed attempt
   * @returns {number} - Milliseconds until next attempt is allowed
   */
  getTimeToWait() {
    if (this.attempts.length === 0) return 0;
    const oldestAttempt = this.attempts[0];
    const timeElapsed = Date.now() - oldestAttempt;
    return Math.max(0, this.intervalMs - timeElapsed);
  }

  /**
   * Reset all attempts (useful after successful action)
   */
  reset() {
    this.attempts = [];
  }
}

// ==================== PRE-DEFINED RATE LIMITERS ====================

// Rate limiter for login attempts (5 attempts per 5 minutes)
export const loginRateLimiter = new RateLimiter(5, 300000);

// Rate limiter for registration attempts (3 attempts per hour)
export const registerRateLimiter = new RateLimiter(3, 3600000);

// Rate limiter for search requests (10 searches per minute)
export const searchRateLimiter = new RateLimiter(10, 60000);

// ==================== HELPER FUNCTIONS ====================

/**
 * Check if a string contains any suspicious patterns
 * @param {string} input - The input to check
 * @returns {boolean} - True if input appears safe
 */
export const isInputSafe = (input) => {
  if (!input) return true;
  
  const dangerousPatterns = [
    /<script/i,
    /javascript:/i,
    /onclick/i,
    /onerror/i,
    /onload/i,
    /eval\(/i,
    /document\.cookie/i
  ];
  
  return !dangerousPatterns.some(pattern => pattern.test(input));
};

/**
 * Get user-friendly error message for validation failures
 * @param {string} field - The field that failed validation
 * @param {string} rule - The validation rule that failed
 * @returns {string} - User-friendly error message
 */
export const getValidationErrorMessage = (field, rule) => {
  const messages = {
    username_required: 'Username is required',
    username_length: 'Username must be 3-30 characters',
    username_format: 'Username can only contain letters, numbers, and underscores',
    email_required: 'Email is required',
    email_format: 'Please enter a valid email address',
    password_required: 'Password is required',
    password_length: 'Password must be at least 8 characters',
    search_query: 'Invalid search query',
    rate_limit: 'Too many attempts. Please try again later.'
  };
  
  return messages[`${field}_${rule}`] || 'Invalid input';
};