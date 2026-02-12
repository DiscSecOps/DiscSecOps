import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Navbar from '../../src/components/layout/Navbar';
import { useAuth } from '../../src/contexts/useAuth';

// Mock useAuth
vi.mock('../../src/contexts/useAuth');

describe('Navbar Component', () => {
  const mockLogout = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('renders full navbar when user is authenticated', () => {
    vi.mocked(useAuth).mockReturnValue({
      user: { username: 'john123' },
      logout: mockLogout,
    });

    render(<Navbar />);

    // Logo
    expect(screen.getByText('Social Circles')).toBeInTheDocument();

    // Username display
    expect(screen.getByText('@john123')).toBeInTheDocument();

    // Avatar initial
    expect(screen.getByText('J')).toBeInTheDocument();

    // Search input
    expect(
      screen.getByPlaceholderText(/search circles/i)
    ).toBeInTheDocument();

    // Dropdown options
    expect(screen.getByText('Profile')).toBeInTheDocument();
    expect(screen.getByText('Settings')).toBeInTheDocument();
    expect(screen.getByText('Logout')).toBeInTheDocument();
  });

  it('calls logout when user confirms logout', async () => {
    vi.mocked(useAuth).mockReturnValue({
      user: { username: 'john123' },
      logout: mockLogout,
    });

    // Mock confirm to return true
    vi.spyOn(window, 'confirm').mockReturnValue(true);

    render(<Navbar />);

    fireEvent.click(screen.getByText('Logout'));

    await waitFor(() => {
      expect(mockLogout).toHaveBeenCalled();
    });
  });

  it('does not call logout when user cancels confirmation', () => {
    vi.mocked(useAuth).mockReturnValue({
      user: { username: 'john123' },
      logout: mockLogout,
    });

    // Mock confirm to return false
    vi.spyOn(window, 'confirm').mockReturnValue(false);

    render(<Navbar />);

    fireEvent.click(screen.getByText('Logout'));

    expect(mockLogout).not.toHaveBeenCalled();
  });

  it('shows alert if logout fails', async () => {
    const failingLogout = vi.fn().mockRejectedValue(new Error('fail'));

    vi.mocked(useAuth).mockReturnValue({
      user: { username: 'john123' },
      logout: failingLogout,
    });

    vi.spyOn(window, 'confirm').mockReturnValue(true);
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {});

    render(<Navbar />);

    fireEvent.click(screen.getByText('Logout'));

    await waitFor(() => {
      expect(alertSpy).toHaveBeenCalledWith(
        'Logout failed. Please try again.'
      );
    });
  });
});
