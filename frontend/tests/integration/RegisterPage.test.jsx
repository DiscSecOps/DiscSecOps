// frontend/tests/integration/RegisterPage.test.jsx
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import RegisterPage from '../../src/pages/RegisterPage';
import AuthProvider from '../../src/contexts/AuthProvider';
import { TEST_USERS, TEST_VALIDATION } from '../helpers/test-constants';
import { useAuthForm } from '../../src/hooks/useAuthForm';

// Mock useAuthForm
vi.mock('../../src/hooks/useAuthForm', () => ({
  useAuthForm: vi.fn()
}));

// Mock auth service
vi.mock('../../src/services/auth.service', () => ({
  authService: {
    login: vi.fn(),
    register: vi.fn(),
    logout: vi.fn(),
    checkAuth: vi.fn().mockResolvedValue({ authenticated: false, user: null })
  }
}));

// Mock navigation
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
    useLocation: () => ({ state: null })
  };
});

describe('RegisterPage - Integration Tests', () => {
  const mockHandleRegister = vi.fn();
  const mockClearError = vi.fn();
  const mockClearErrors = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    
    // Reset mock implementations
    mockHandleRegister.mockReset();
    mockClearError.mockReset();
    mockClearErrors.mockReset();
    
    // Default mock return value
    useAuthForm.mockReturnValue({
      loading: false,
      errors: {},
      handleLogin: vi.fn(),
      handleRegister: mockHandleRegister,
      clearError: mockClearError,
      clearErrors: mockClearErrors
    });
  });

  const renderRegisterPage = () => {
    return render(
      <BrowserRouter>
        <AuthProvider>
          <RegisterPage />
        </AuthProvider>
      </BrowserRouter>
    );
  };

  // ==================== RENDERING TESTS ====================
  
  it('should render registration form correctly', () => {
    renderRegisterPage();
    
    expect(screen.getByLabelText(/Username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^Password/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Confirm Password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Create Account/i })).toBeInTheDocument();
    expect(screen.getByText(/Already have an account/i)).toBeInTheDocument();
  });

  it('should render optional full name field', () => {
    renderRegisterPage();
    expect(screen.getByLabelText(/Full Name/i)).toBeInTheDocument();
  });

  // ==================== VALIDATION TESTS ====================

  it('should show validation error for empty username', async () => {
    useAuthForm.mockReturnValue({
      loading: false,
      errors: {
        username: 'Username is required'
      },
      handleLogin: vi.fn(),
      handleRegister: mockHandleRegister,
      clearError: mockClearError,
      clearErrors: mockClearErrors
    });
    
    renderRegisterPage();
    
    await waitFor(() => {
      expect(screen.getByText(/Username is required/i)).toBeInTheDocument();
    });
  });

  it('should show validation error for short username', async () => {
    useAuthForm.mockReturnValue({
      loading: false,
      errors: {
        username: 'Username must be 3-30 characters (letters, numbers, underscore)'
      },
      handleLogin: vi.fn(),
      handleRegister: mockHandleRegister,
      clearError: mockClearError,
      clearErrors: mockClearErrors
    });
    
    renderRegisterPage();
    
    await waitFor(() => {
      expect(screen.getByText(/Username must be 3-30 characters/i)).toBeInTheDocument();
    });
  });

  it('should show validation error for invalid email', async () => {
    useAuthForm.mockReturnValue({
      loading: false,
      errors: {
        email: 'Please enter a valid email address'
      },
      handleLogin: vi.fn(),
      handleRegister: mockHandleRegister,
      clearError: mockClearError,
      clearErrors: mockClearErrors
    });
    
    renderRegisterPage();
    
    await waitFor(() => {
      expect(screen.getByText(/Please enter a valid email address/i)).toBeInTheDocument();
    });
  });

  it('should show validation error for empty email', async () => {
    useAuthForm.mockReturnValue({
      loading: false,
      errors: {
        email: 'Email is required'
      },
      handleLogin: vi.fn(),
      handleRegister: mockHandleRegister,
      clearError: mockClearError,
      clearErrors: mockClearErrors
    });
    
    renderRegisterPage();
    
    await waitFor(() => {
      expect(screen.getByText(/Email is required/i)).toBeInTheDocument();
    });
  });

  it('should show validation error for short password', async () => {
    useAuthForm.mockReturnValue({
      loading: false,
      errors: {
        password: 'Password must be at least 8 characters'
      },
      handleLogin: vi.fn(),
      handleRegister: mockHandleRegister,
      clearError: mockClearError,
      clearErrors: mockClearErrors
    });
    
    renderRegisterPage();
    
    await waitFor(() => {
      expect(screen.getByText(/Password must be at least 8 characters/i)).toBeInTheDocument();
    });
  });

  it('should show validation error for empty password', async () => {
    useAuthForm.mockReturnValue({
      loading: false,
      errors: {
        password: 'Password is required'
      },
      handleLogin: vi.fn(),
      handleRegister: mockHandleRegister,
      clearError: mockClearError,
      clearErrors: mockClearErrors
    });
    
    renderRegisterPage();
    
    await waitFor(() => {
      expect(screen.getByText(/Password is required/i)).toBeInTheDocument();
    });
  });

  it('should show validation error when passwords do not match', async () => {
    useAuthForm.mockReturnValue({
      loading: false,
      errors: {
        confirmPassword: 'Passwords do not match'
      },
      handleLogin: vi.fn(),
      handleRegister: mockHandleRegister,
      clearError: mockClearError,
      clearErrors: mockClearErrors
    });
    
    renderRegisterPage();
    
    await waitFor(() => {
      expect(screen.getByText(/Passwords do not match/i)).toBeInTheDocument();
    });
  });

  // ==================== SUCCESSFUL REGISTRATION ====================

  it('should call register API and navigate to login on success', async () => {
    mockHandleRegister.mockResolvedValue(true);
    
    useAuthForm.mockReturnValue({
      loading: false,
      errors: {},
      handleLogin: vi.fn(),
      handleRegister: mockHandleRegister,
      clearError: mockClearError,
      clearErrors: mockClearErrors
    });
    
    renderRegisterPage();
    
    const usernameInput = screen.getByLabelText(/Username/i);
    const emailInput = screen.getByLabelText(/Email/i);
    const passwordInput = screen.getByLabelText(/^Password/i);
    const confirmPasswordInput = screen.getByLabelText(/Confirm Password/i);
    const submitButton = screen.getByRole('button', { name: /Create Account/i });
    
    await userEvent.type(usernameInput, TEST_USERS.newUser.username);
    await userEvent.type(emailInput, TEST_USERS.newUser.email);
    await userEvent.type(passwordInput, TEST_USERS.newUser.password);
    await userEvent.type(confirmPasswordInput, TEST_USERS.newUser.password);
    await userEvent.click(submitButton);
    
    await waitFor(() => {
      expect(mockHandleRegister).toHaveBeenCalledWith(
        TEST_USERS.newUser.username,
        TEST_USERS.newUser.email,
        TEST_USERS.newUser.password,
        TEST_USERS.newUser.password
      );
      expect(mockNavigate).toHaveBeenCalledWith('/login', {
        state: { success: `Account created for ${TEST_USERS.newUser.username}! You can now login.` }
      });
    });
  });

  // ==================== ERROR HANDLING ====================

  it('should show error message when username already exists', async () => {
    mockHandleRegister.mockResolvedValue(false);
    
    useAuthForm.mockReturnValue({
      loading: false,
      errors: {
        general: 'Username already exists'
      },
      handleLogin: vi.fn(),
      handleRegister: mockHandleRegister,
      clearError: mockClearError,
      clearErrors: mockClearErrors
    });
    
    renderRegisterPage();
    
    const usernameInput = screen.getByLabelText(/Username/i);
    const emailInput = screen.getByLabelText(/Email/i);
    const passwordInput = screen.getByLabelText(/^Password/i);
    const confirmPasswordInput = screen.getByLabelText(/Confirm Password/i);
    const submitButton = screen.getByRole('button', { name: /Create Account/i });
    
    await userEvent.type(usernameInput, TEST_USERS.validUser.username);
    await userEvent.type(emailInput, TEST_USERS.newUser.email);
    await userEvent.type(passwordInput, TEST_USERS.newUser.password);
    await userEvent.type(confirmPasswordInput, TEST_USERS.newUser.password);
    await userEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Username already exists/i)).toBeInTheDocument();
    });
  });

  it('should show error message when email already exists', async () => {
    mockHandleRegister.mockResolvedValue(false);
    
    useAuthForm.mockReturnValue({
      loading: false,
      errors: {
        general: 'Email already exists'
      },
      handleLogin: vi.fn(),
      handleRegister: mockHandleRegister,
      clearError: mockClearError,
      clearErrors: mockClearErrors
    });
    
    renderRegisterPage();
    
    const usernameInput = screen.getByLabelText(/Username/i);
    const emailInput = screen.getByLabelText(/Email/i);
    const passwordInput = screen.getByLabelText(/^Password/i);
    const confirmPasswordInput = screen.getByLabelText(/Confirm Password/i);
    const submitButton = screen.getByRole('button', { name: /Create Account/i });
    
    await userEvent.type(usernameInput, TEST_USERS.newUser.username);
    await userEvent.type(emailInput, TEST_USERS.validUser.email);
    await userEvent.type(passwordInput, TEST_USERS.newUser.password);
    await userEvent.type(confirmPasswordInput, TEST_USERS.newUser.password);
    await userEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Email already exists/i)).toBeInTheDocument();
    });
  });

  it('should clear field error when user starts typing', async () => {
    // First, mock with an error
    useAuthForm.mockReturnValue({
      loading: false,
      errors: {
        username: 'Username is required'
      },
      handleLogin: vi.fn(),
      handleRegister: mockHandleRegister,
      clearError: mockClearError,
      clearErrors: mockClearErrors
    });
    
    renderRegisterPage();
    
    const usernameInput = screen.getByLabelText(/Username/i);
    
    // Type something in the field
    await userEvent.type(usernameInput, 'test');
    
    // clearError should be called for the username field
    expect(mockClearError).toHaveBeenCalledWith('username');
  });
});