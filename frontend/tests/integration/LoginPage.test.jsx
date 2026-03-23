// frontend/tests/integration/LoginPage.test.jsx
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import LoginPage from '../../src/pages/LoginPage';
import AuthProvider from '../../src/contexts/AuthProvider';
import { TEST_USERS} from '../helpers/test-constants';
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

describe('LoginPage - Integration Tests', () => {
  const mockHandleLogin = vi.fn();
  const mockClearError = vi.fn();
  const mockClearErrors = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    
    // Reset mock implementations
    mockHandleLogin.mockReset();
    mockClearError.mockReset();
    mockClearErrors.mockReset();
    
    // Default mock return value
    useAuthForm.mockReturnValue({
      loading: false,
      errors: {},
      handleLogin: mockHandleLogin,
      handleRegister: vi.fn(),
      clearError: mockClearError,
      clearErrors: mockClearErrors
    });
  });

  const renderLoginPage = () => {
    return render(
      <BrowserRouter>
        <AuthProvider>
          <LoginPage />
        </AuthProvider>
      </BrowserRouter>
    );
  };

  it('should render login form correctly', () => {
    renderLoginPage();
    expect(screen.getByLabelText(/Username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Login/i })).toBeInTheDocument();
  });

  it('should show validation error for empty fields', async () => {
    useAuthForm.mockReturnValue({
      loading: false,
      errors: {
        username: 'Username is required',
        password: 'Password is required'
      },
      handleLogin: mockHandleLogin,
      handleRegister: vi.fn(),
      clearError: mockClearError,
      clearErrors: mockClearErrors
    });
    
    renderLoginPage();
    
    await waitFor(() => {
      expect(screen.getByText(/Username is required/i)).toBeInTheDocument();
      expect(screen.getByText(/Password is required/i)).toBeInTheDocument();
    });
  });

  it('should show validation error for short username', async () => {
    useAuthForm.mockReturnValue({
      loading: false,
      errors: {
        username: 'Username must be 3-30 characters (letters, numbers, underscore)'
      },
      handleLogin: mockHandleLogin,
      handleRegister: vi.fn(),
      clearError: mockClearError,
      clearErrors: mockClearErrors
    });
    
    renderLoginPage();
    
    await waitFor(() => {
      expect(screen.getByText(/Username must be 3-30 characters/i)).toBeInTheDocument();
    });
  });

  it('should show validation error for short password', async () => {
    useAuthForm.mockReturnValue({
      loading: false,
      errors: {
        password: 'Password must be at least 8 characters'
      },
      handleLogin: mockHandleLogin,
      handleRegister: vi.fn(),
      clearError: mockClearError,
      clearErrors: mockClearErrors
    });
    
    renderLoginPage();
    
    await waitFor(() => {
      expect(screen.getByText(/Password must be at least 8 characters/i)).toBeInTheDocument();
    });
  });

  it('should call login API and navigate on success', async () => {
    mockHandleLogin.mockResolvedValue(true);
    
    useAuthForm.mockReturnValue({
      loading: false,
      errors: {},
      handleLogin: mockHandleLogin,
      handleRegister: vi.fn(),
      clearError: mockClearError,
      clearErrors: mockClearErrors
    });
    
    renderLoginPage();
    
    const usernameInput = screen.getByLabelText(/Username/i);
    const passwordInput = screen.getByLabelText(/Password/i);
    const submitButton = screen.getByRole('button', { name: /Login/i });
    
    await userEvent.type(usernameInput, TEST_USERS.validUser.username);
    await userEvent.type(passwordInput, TEST_USERS.validUser.password);
    await userEvent.click(submitButton);
    
    await waitFor(() => {
      expect(mockHandleLogin).toHaveBeenCalledWith(
        TEST_USERS.validUser.username,
        TEST_USERS.validUser.password
      );
      expect(mockNavigate).toHaveBeenCalledWith('/user-dashboard');
    });
  });

  it('should show error message on login failure', async () => {
    mockHandleLogin.mockResolvedValue(false);
    
    useAuthForm.mockReturnValue({
      loading: false,
      errors: {
        general: 'Invalid username or password'
      },
      handleLogin: mockHandleLogin,
      handleRegister: vi.fn(),
      clearError: mockClearError,
      clearErrors: mockClearErrors
    });
    
    renderLoginPage();
    
    const usernameInput = screen.getByLabelText(/Username/i);
    const passwordInput = screen.getByLabelText(/Password/i);
    const submitButton = screen.getByRole('button', { name: /Login/i });
    
    await userEvent.type(usernameInput, TEST_USERS.validUser.username);
    await userEvent.type(passwordInput, TEST_USERS.wrongPassword.password);
    await userEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Invalid username or password/i)).toBeInTheDocument();
    });
  });
});