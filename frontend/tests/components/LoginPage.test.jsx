// frontend/tests/components/LoginPage.test.jsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import LoginPage from '../../src/pages/LoginPage.jsx';
import { authService } from '../../src/services/auth.service.js';

// Mock auth service
vi.mock('../../src/services/auth.service.js');

// Test suite for LoginPage component
describe('LoginPage', () => {
  it('should render login form', () => {
    render(<LoginPage />);
    
    expect(screen.getByText('Login to Social Circles')).toBeInTheDocument();
    expect(screen.getByLabelText('Username')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Login' })).toBeInTheDocument();
  });

  it('should show error on failed login', async () => {
    authService.login.mockRejectedValue({ error: 'Invalid credentials' });
    
    render(<LoginPage />);
    
    fireEvent.change(screen.getByLabelText('Username'), {
      target: { value: 'wronguser' }
    });
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'wrongpass' }
    });
    fireEvent.click(screen.getByRole('button', { name: 'Login' }));
    
    await waitFor(() => {
      expect(screen.getByText('Invalid credentials')).toBeInTheDocument();
    });
  });

  it('should disable button when loading', async () => {
    authService.login.mockImplementation(() => new Promise(() => {})); // Never resolves
    
    render(<LoginPage />);
    
    fireEvent.change(screen.getByLabelText('Username'), {
      target: { value: 'testuser' }
    });
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'pass123' }
    });
    fireEvent.click(screen.getByRole('button', { name: 'Login' }));
    
    await waitFor(() => {
      expect(screen.getByRole('button')).toBeDisabled();
      expect(screen.getByText('Logging in...')).toBeInTheDocument();
    });
  });
});