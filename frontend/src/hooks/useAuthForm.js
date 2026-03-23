// frontend/src/hooks/useAuthForm.js
import { useState, useCallback } from 'react';
import { useAuth } from '../contexts/useAuth'; 
import { 
  validateUsername, 
  validateEmail, 
  validatePassword,
  sanitizeInput,
  sanitizeUsername,
  sanitizeEmail,
  loginRateLimiter,
  registerRateLimiter
} from '../utils/security';

/**
 * Custom hook for authentication forms (login and register)
 * Handles validation, sanitization, and rate limiting before calling auth context
 * This is an INTERMEDIARY layer between pages and useAuth context
 */
export const useAuthForm = () => {
  // Get auth functions from existing context
  const { login: authLogin, register: authRegister } = useAuth();
  
  // Local state for form handling
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  /**
   * Validate login form fields
   * @param {string} username - Username to validate
   * @param {string} password - Password to validate
   * @returns {object} - Object containing validation errors
   */
  const validateLoginForm = useCallback((username, password) => {
    const newErrors = {};
    
    if (!username) {
      newErrors.username = 'Username is required';
    } else if (!validateUsername(username)) {
      newErrors.username = 'Username must be 3-30 characters (letters, numbers, underscore)';
    }
    
    if (!password) {
      newErrors.password = 'Password is required';
    } else if (!validatePassword(password)) {
      newErrors.password = 'Password must be at least 8 characters and include uppercase, lowercase, number, and special character';
    }
    
    return newErrors;
  }, []);

  /**
   * Validate register form fields
   * @param {string} username - Username to validate
   * @param {string} email - Email to validate
   * @param {string} password - Password to validate
   * @param {string} confirmPassword - Password confirmation
   * @returns {object} - Object containing validation errors
   */
  const validateRegisterForm = useCallback((username, email, password, confirmPassword) => {
    const newErrors = {};
    
    // Validate username
    if (!username) {
      newErrors.username = 'Username is required';
    } else if (!validateUsername(username)) {
      newErrors.username = 'Username must be 3-30 characters (letters, numbers, underscore)';
    }
    
    // Validate email
    if (!email) {
      newErrors.email = 'Email is required';
    } else if (!validateEmail(email)) {
      newErrors.email = 'Please enter a valid email address';
    }
    
    // Validate password
    if (!password) {
      newErrors.password = 'Password is required';
    } else if (!validatePassword(password)) {
      newErrors.password = 'Password must be at least 8 characters and include uppercase, lowercase, number, and special character';
    }
    
    // Validate password confirmation
    if (password !== confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    
    return newErrors;
  }, []);

  /**
   * Handle login with validation and sanitization
   * @param {string} username - Raw username from input
   * @param {string} password - Raw password from input
   * @returns {boolean} - True if login successful, false otherwise
   */
  const handleLogin = useCallback(async (username, password) => {
    // Check rate limiting
    if (!loginRateLimiter.canAttempt()) {
      const waitTime = Math.ceil(loginRateLimiter.getTimeToWait() / 1000);
      setErrors({ general: `Too many login attempts. Please wait ${waitTime} seconds.` });
      return false;
    }

    // Validate form
    const formErrors = validateLoginForm(username, password);
    if (Object.keys(formErrors).length > 0) {
      setErrors(formErrors);
      return false;
    }

    setLoading(true);
    setErrors({});

    try {
      // Sanitize inputs before sending to backend
      const cleanUsername = sanitizeUsername(username);
      const cleanPassword = sanitizeInput(password);
      
      // Call the actual login function from auth context
      await authLogin({ username: cleanUsername, password: cleanPassword });
      
      // Reset rate limiter on successful login
      loginRateLimiter.reset();
      return true;
    } catch (error) {
      console.error('Login error:', error);
      
      // Handle different error types
      let errorMessage = error.message || 'Login failed';
      if (errorMessage.toLowerCase().includes('locked')) {
        errorMessage = 'Account locked. Try again in 15 minutes';
      } else if (errorMessage.toLowerCase().includes('invalid')) {
        errorMessage = 'Invalid username or password';
      }
      
      setErrors({ general: errorMessage });
      return false;
    } finally {
      setLoading(false);
    }
  }, [authLogin, validateLoginForm]);

  /**
   * Handle registration with validation and sanitization
   * @param {string} username - Raw username from input
   * @param {string} email - Raw email from input
   * @param {string} password - Raw password from input
   * @param {string} confirmPassword - Raw password confirmation
   * @returns {boolean} - True if registration successful, false otherwise
   */
  const handleRegister = useCallback(async (username, email, password, confirmPassword) => {
    // Check rate limiting
    if (!registerRateLimiter.canAttempt()) {
      const waitTime = Math.ceil(registerRateLimiter.getTimeToWait() / 1000);
      setErrors({ general: `Too many registration attempts. Please wait ${waitTime} seconds.` });
      return false;
    }

    // Validate form
    const formErrors = validateRegisterForm(username, email, password, confirmPassword);
    if (Object.keys(formErrors).length > 0) {
      setErrors(formErrors);
      return false;
    }

    setLoading(true);
    setErrors({});

    try {
      // Sanitize inputs before sending to backend
      const cleanUsername = sanitizeUsername(username);
      const cleanEmail = sanitizeEmail(email);
      const cleanPassword = sanitizeInput(password);
      
      // Call the actual register function from auth context
      await authRegister({ 
        username: cleanUsername, 
        email: cleanEmail, 
        password: cleanPassword,
        full_name: '' // Optional field
      });
      
      // Reset rate limiter on successful registration
      registerRateLimiter.reset();
      return true;
    } catch (error) {
      console.error('Registration error:', error);
      setErrors({ general: error.message || 'Registration failed' });
      return false;
    } finally {
      setLoading(false);
    }
  }, [authRegister, validateRegisterForm]);

  /**
   * Clear a specific error field
   * @param {string} field - Field name to clear error for
   */
  const clearError = useCallback((field) => {
    setErrors(prev => {
      const newErrors = { ...prev };
      delete newErrors[field];
      return newErrors;
    });
  }, []);

  /**
   * Clear all errors
   */
  const clearErrors = useCallback(() => {
    setErrors({});
  }, []);

  return {
    loading,      // Loading state for buttons
    errors,       // Object containing validation and general errors
    handleLogin,  // Login handler with validation
    handleRegister, // Register handler with validation
    clearError,   // Clear specific field error
    clearErrors   // Clear all errors
  };
};