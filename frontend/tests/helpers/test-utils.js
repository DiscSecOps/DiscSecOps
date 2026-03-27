// frontend/tests/helpers/test-utils.js
import { vi } from 'vitest';
import { render } from '@testing-library/react';

// ==========================================
// RE-EXPORT 
// ==========================================
export * from '@testing-library/react';
export { default as userEvent } from '@testing-library/user-event';

// ==========================================
// MOCK UTILITIES
// ==========================================

// Mock for API config values
export const mockConfig = () => {
  vi.mock('../../src/config', () => ({
    API_BASE_URL: 'http://mocked-for-tests.local'
  }));
};

// Mock API service methods
export const mockApi = () => {
  vi.mock('../../src/services/api', () => ({
    default: {
      get: vi.fn(),
      post: vi.fn(),
      put: vi.fn(),
      delete: vi.fn(),
    }
  }));
};

// Mock for circleMemberService
export const mockCircleMemberService = () => {
  vi.mock('../../src/services/circleMember.service', () => ({
    circleMemberService: {
      searchUsers: vi.fn(),
      addMember: vi.fn(),
      removeMember: vi.fn(),
      updateRole: vi.fn(),
      updateCircleName: vi.fn(),
    }
  }));
};

// Mock for authService
export const mockAuthService = () => {
  vi.mock('../../src/services/auth.service', () => ({
    authService: {
      login: vi.fn(),
      register: vi.fn(),
      logout: vi.fn(),
      checkAuth: vi.fn(),
      requestPasswordReset: vi.fn(),
      resetPassword: vi.fn(),
      verifyEmail: vi.fn(),
      resendVerificationEmail: vi.fn(),
    }
  }));
};

// ==========================================
// ASYNC UTILITIES
// ==========================================

// Awaits for all pending promises to resolve (utils for async operations in tests)
export const flushPromises = () => new Promise(resolve => setTimeout(resolve, 0));

// Awaits for a specific time (util for animations, etc.)
export const wait = (ms = 100) => new Promise(resolve => setTimeout(resolve, ms));

// ==========================================
// MOCK UTILITIES (Browser APIs)
// ==========================================

// Mock for localStorage
export const mockLocalStorage = () => {
  const storage = {};
  return {
    getItem: vi.fn(key => storage[key] || null),
    setItem: vi.fn((key, value) => { storage[key] = value; }),
    removeItem: vi.fn(key => delete storage[key]),
    clear: vi.fn(() => { Object.keys(storage).forEach(key => delete storage[key]); }),
  };
};

// Mock for window.confirm
export const mockConfirm = (returnValue = true) => {
  const originalConfirm = window.confirm;
  window.confirm = vi.fn(() => returnValue);
  return () => { window.confirm = originalConfirm; };
};

// Mock for window.alert
export const mockAlert = () => {
  const originalAlert = window.alert;
  window.alert = vi.fn();
  return () => { window.alert = originalAlert; };
};

// ==========================================
// RENDER UTILITIES
// ==========================================

// Render with providers (if needed)
export const renderWithProviders = (ui, { ...options } = {}) => {
  return render(ui, { ...options });
};

// ==========================================
// RESET UTILITIES
// ==========================================

// Reset all mocks
export const resetAllMocks = () => {
  vi.clearAllMocks();
  vi.restoreAllMocks();
};