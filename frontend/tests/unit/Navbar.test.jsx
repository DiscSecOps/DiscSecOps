import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Navbar from '../../src/components/layout/Navbar';
import { MemoryRouter } from 'react-router-dom';
import AuthContext from '../../src/contexts/AuthContext';
import DarkModeContext from '../../src/contexts/DarkModeContext';

// Helper method for wrapping Navbar in necessary providers
const renderWithProviders = (ui, { user = null, logout = vi.fn(), isDarkMode = true } = {}) => {
  return render(
        <AuthContext.Provider value={{user, logout}}>
          <DarkModeContext.Provider value={{isDarkMode}}>
            <MemoryRouter>
                {ui}
            </MemoryRouter>
          </DarkModeContext.Provider>
        </AuthContext.Provider>
    );
};

describe('Navbar Component', () => {
  const mockLogout = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  const openUserDropDown = () => {
    fireEvent.click(screen.getByTestId('navbar-user'));
  };

  it('renders full navbar when user is authenticated', () => {
    renderWithProviders(<Navbar />, {
      user:  {username: 'john123' },
      logout: mockLogout,
    });

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
    
    openUserDropDown();

    // Dropdown options
    expect(screen.getByText('Profile')).toBeInTheDocument();
    expect(screen.getByText('Settings')).toBeInTheDocument();
    expect(screen.getByText('Logout')).toBeInTheDocument();
  });

  it('calls logout when user confirms logout', async () => {
    // Mock confirm to return true
    vi.spyOn(window, 'confirm').mockReturnValue(true);

    renderWithProviders(<Navbar />, {
      user:  {username: 'john123' },
      logout: mockLogout,
    });

    openUserDropDown();

    fireEvent.click(screen.getByText('Logout'));

    await waitFor(() => {
      expect(mockLogout).toHaveBeenCalled();
    });
  });

  it('does not call logout when user cancels confirmation', () => {
    // Mock confirm to return false
    vi.spyOn(window, 'confirm').mockReturnValue(false);

    renderWithProviders(<Navbar />, {
      user:  {username: 'john123' },
      logout: mockLogout,
    });

    openUserDropDown();

    fireEvent.click(screen.getByText('Logout'));

    expect(mockLogout).not.toHaveBeenCalled();
  });

  it('shows alert if logout fails', async () => {
    const failingLogout = vi.fn().mockRejectedValue(new Error('fail'));
    
    vi.spyOn(window, 'confirm').mockReturnValue(true);
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {});

    renderWithProviders(<Navbar />, {
      user:  {username: 'john123' },
      logout: failingLogout,
    });

    openUserDropDown();

    fireEvent.click(screen.getByText('Logout'));

    await waitFor(() => {
      expect(alertSpy).toHaveBeenCalledWith(
        'Logout failed. Please try again.'
      );
    });
  });
});
