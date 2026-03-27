// frontend/tests/unit/AddMemberModal.test.jsx
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// ==========================================
// ALL MOCKS MUST BE AT TOP LEVEL
// ==========================================

// Mock api first (top level)
vi.mock('../../src/services/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  }
}));

// Mock config (top level - don't use mockConfig function)
vi.mock('../../src/config', () => ({
  API_BASE_URL: 'http://mocked-for-tests.local'
}));

// Mock circleMemberService (top level)
vi.mock('../../src/services/circleMember.service', () => ({
  circleMemberService: {
    searchUsers: vi.fn(),
    addMember: vi.fn(),
    removeMember: vi.fn(),
    updateRole: vi.fn(),
    updateCircleName: vi.fn(),
  }
}));

// ==========================================
// IMPORTS AFTER MOCKS
// ==========================================
import AddMemberModal from '../../src/components/circles/AddMemberModal';
import { TEST_MEMBERS, TEST_CIRCLES } from '../helpers/test-constants';
import { circleMemberService } from '../../src/services/circleMember.service';

describe('AddMemberModal', () => {
  const mockOnClose = vi.fn();
  const mockOnMemberAdded = vi.fn();
  const defaultProps = {
    isOpen: true,
    onClose: mockOnClose,
    circleId: TEST_CIRCLES.testCircleId,
    onMemberAdded: mockOnMemberAdded,
  };

  beforeEach(() => {
    circleMemberService.searchUsers.mockReset();
    circleMemberService.addMember.mockReset();
    circleMemberService.removeMember.mockReset();
    circleMemberService.updateRole.mockReset();
    circleMemberService.updateCircleName.mockReset();

  });

  it('searches for users when search button is clicked', async () => {
    const mockUsers = [
      TEST_MEMBERS.nonMember,
      TEST_MEMBERS.newMember,
    ];
    
    circleMemberService.searchUsers.mockResolvedValue(mockUsers);

    render(<AddMemberModal {...defaultProps} />);

    // Așteaptă să apară modal-ul
    await waitFor(() => {
      expect(screen.getByText('Add Member to Circle')).toBeInTheDocument();
    });

    const searchInput = screen.getByPlaceholderText(/search by username/i);
    const searchButton = screen.getByRole('button', { name: /search/i });

    await userEvent.type(searchInput, TEST_MEMBERS.newMember.username);
    fireEvent.click(searchButton);

    await waitFor(() => {
      expect(circleMemberService.searchUsers).toHaveBeenCalledWith(
        TEST_MEMBERS.newMember.username, 
        TEST_CIRCLES.testCircleId
      );
    });

    await waitFor(() => {
      expect(screen.getByText(TEST_MEMBERS.nonMember.username)).toBeInTheDocument();
      expect(screen.getByText(TEST_MEMBERS.nonMember.email)).toBeInTheDocument();
      expect(screen.getByText(TEST_MEMBERS.newMember.username)).toBeInTheDocument();
      expect(screen.getByText(TEST_MEMBERS.newMember.email)).toBeInTheDocument();
    });
  });

  it('shows no results message when search returns empty', async () => {
    circleMemberService.searchUsers.mockResolvedValue([]);

    render(<AddMemberModal {...defaultProps} />);

    await waitFor(() => {
      expect(screen.getByText('Add Member to Circle')).toBeInTheDocument();
    });

    const searchInput = screen.getByPlaceholderText(/search by username/i);
    const searchButton = screen.getByRole('button', { name: /search/i });

    await userEvent.type(searchInput, 'nonexistent');
    fireEvent.click(searchButton);

    await waitFor(() => {
      expect(screen.getByText(/no users found matching/i)).toBeInTheDocument();
    });
  });

  it('handles search error gracefully', async () => {
    circleMemberService.searchUsers.mockRejectedValue(new Error('API Error'));

    render(<AddMemberModal {...defaultProps} />);

    await waitFor(() => {
      expect(screen.getByText('Add Member to Circle')).toBeInTheDocument();
    });

    const searchInput = screen.getByPlaceholderText(/search by username/i);
    const searchButton = screen.getByRole('button', { name: /search/i });

    await userEvent.type(searchInput, TEST_MEMBERS.newMember.username);
    fireEvent.click(searchButton);

    await waitFor(() => {
      expect(screen.getByText(/search failed/i)).toBeInTheDocument();
    });
  });
});