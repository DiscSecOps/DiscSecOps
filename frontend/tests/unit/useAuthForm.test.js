// frontend/tests/unit/useAuthForm.test.js
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useAuthForm } from '../../src/hooks/useAuthForm';
import { useAuth } from '../../src/contexts/useAuth';
import { TEST_USERS, TEST_VALIDATION } from '../helpers/test-constants';

// Mock the useAuth hook
vi.mock('../../src/contexts/useAuth', () => ({
  useAuth: vi.fn()
}));

// Mock rate limiters
vi.mock('../../src/utils/security', async () => {
  const actual = await vi.importActual('../../src/utils/security');
  return {
    ...actual,
    loginRateLimiter: {
      canAttempt: vi.fn(() => true),
      getTimeToWait: vi.fn(() => 0),
      reset: vi.fn()
    },
    registerRateLimiter: {
      canAttempt: vi.fn(() => true),
      getTimeToWait: vi.fn(() => 0),
      reset: vi.fn()
    }
  };
});

// Import the actual validation functions for testing
describe('useAuthForm - Unit Tests', () => {
  const mockLogin = vi.fn();
  const mockRegister = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    mockLogin.mockReset();
    mockRegister.mockReset();
    
    useAuth.mockReturnValue({
      login: mockLogin,
      register: mockRegister,
      user: null,
      loading: false
    });
  });

  // Test cases for useAuthForm
  describe('Initial State', () => {
    it('should initialize with default values', () => {
      const { result } = renderHook(() => useAuthForm());
      
      expect(result.current.loading).toBe(false);
      expect(result.current.errors).toEqual({});
      expect(typeof result.current.handleLogin).toBe('function');
      expect(typeof result.current.handleRegister).toBe('function');
      expect(typeof result.current.clearError).toBe('function');
      expect(typeof result.current.clearErrors).toBe('function');
    });
  });

  // Validation tests for handleLogin
  describe('handleLogin - Validation', () => {
    it('should return false and set error when username is empty', async () => {
      const { result } = renderHook(() => useAuthForm());
      
      let success;
      await act(async () => {
        success = await result.current.handleLogin('', TEST_VALIDATION.validPassword);
      });
      
      expect(success).toBe(false);
      expect(result.current.errors.username).toBe('Username is required');
      expect(mockLogin).not.toHaveBeenCalled();
    });

    it('should return false and set error when username is too short', async () => {
      const { result } = renderHook(() => useAuthForm());
      
      await act(async () => {
        await result.current.handleLogin(TEST_VALIDATION.shortUsername, TEST_VALIDATION.validPassword);
      });
      
      expect(result.current.errors.username).toBe('Username must be 3-30 characters (letters, numbers, underscore)');
      expect(mockLogin).not.toHaveBeenCalled();
    });

    it('should return false and set error when password is empty', async () => {
      const { result } = renderHook(() => useAuthForm());
      
      await act(async () => {
        await result.current.handleLogin(TEST_USERS.validUser.username, '');
      });
      
      expect(result.current.errors.password).toBe('Password is required');
      expect(mockLogin).not.toHaveBeenCalled();
    });
  });

  // Validation tests for handleRegister
  describe('handleLogin - Successful Login', () => {
    it('should call login with valid credentials and return true', async () => {
      mockLogin.mockResolvedValue({ user: { id: 1 } });
      
      const { result } = renderHook(() => useAuthForm());
      
      let success;
      await act(async () => {
        success = await result.current.handleLogin(
          TEST_USERS.validUser.username, 
          TEST_USERS.validUser.password
        );
      });
      
      expect(success).toBe(true);
      expect(mockLogin).toHaveBeenCalledTimes(1);
      expect(mockLogin).toHaveBeenCalledWith({
        username: TEST_USERS.validUser.username,
        password: TEST_USERS.validUser.password
      });
    });
  });

  describe('handleLogin - Error Handling', () => {
    it('should handle invalid credentials error', async () => {
      mockLogin.mockRejectedValue(new Error('Invalid username or password'));
      
      const { result } = renderHook(() => useAuthForm());
      
      let success;
      await act(async () => {
        success = await result.current.handleLogin(
          TEST_USERS.validUser.username,
          TEST_USERS.wrongPassword.password
        );
      });
      
      expect(success).toBe(false);
      expect(result.current.errors.general).toBe('Invalid username or password');
    });

    it('should handle account locked error', async () => {
      mockLogin.mockRejectedValue(new Error('Account locked'));
      
      const { result } = renderHook(() => useAuthForm());
      
      await act(async () => {
        await result.current.handleLogin(
          TEST_USERS.validUser.username,
          TEST_USERS.wrongPassword.password
        );
      });
      
      expect(result.current.errors.general).toBe('Account locked. Try again in 15 minutes');
    });

    it('should handle generic error message', async () => {
      mockLogin.mockRejectedValue(new Error('Network error'));
      
      const { result } = renderHook(() => useAuthForm());
      
      await act(async () => {
        await result.current.handleLogin(
          TEST_USERS.validUser.username,
          TEST_USERS.validUser.password
        );
      });
      
      expect(result.current.errors.general).toBe('Network error');
    });
  });

  describe('Error Clearing', () => {
    it('should clear specific error field', async () => {
      const { result } = renderHook(() => useAuthForm());
      
      await act(async () => {
        await result.current.handleLogin(TEST_VALIDATION.shortUsername, TEST_VALIDATION.validPassword);
      });
      expect(result.current.errors.username).toBeDefined();
      
      act(() => {
        result.current.clearError('username');
      });
      
      expect(result.current.errors.username).toBeUndefined();
    });

    it('should clear all errors', async () => {
      const { result } = renderHook(() => useAuthForm());
      
      await act(async () => {
        await result.current.handleLogin(TEST_VALIDATION.shortUsername, TEST_VALIDATION.shortPassword);
      });
      expect(Object.keys(result.current.errors).length).toBeGreaterThan(0);
      
      act(() => {
        result.current.clearErrors();
      });
      
      expect(result.current.errors).toEqual({});
    });
  });
});