// frontend/tests/unit/auth.service.test.js
import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';
import { authService } from '../../src/services/auth.service.js';

// Mock axios
vi.mock('axios');

// Unit tests for Auth Service
describe('Auth Service', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  // Tests for login method
  describe('login', () => {
    it('should login successfully', async () => {
      const mockResponse = {
        data: { success: true, username: 'testuser' }
      };
      axios.post.mockResolvedValue(mockResponse);

      // Call the login method
      const result = await authService.login('testuser', 'pass123');
      
      // Assertions
      expect(axios.post).toHaveBeenCalledWith(
        'http://localhost:5000/api/auth/login',
        { username: 'testuser', password: 'pass123' }
      );
      
      expect(result).toEqual(mockResponse.data);
    });

    // Test for login failure
    it('should handle login error', async () => {
      const errorResponse = {
        response: { data: { error: 'Invalid credentials' } }
      };
      axios.post.mockRejectedValue(errorResponse);

      await expect(authService.login('wrong', 'pass'))
        .rejects.toEqual({ error: 'Invalid credentials' });
    });
  });

    // Tests for register method
  describe('register', () => {
    it('should register successfully', async () => {
      const mockResponse = {
        data: { success: true, username: 'newuser' }
      };
      axios.post.mockResolvedValue(mockResponse);

      // Call the register method
      const result = await authService.register('newuser', 'pass123');
      
      expect(axios.post).toHaveBeenCalledWith(
        'http://localhost:5000/api/auth/register',
        { username: 'newuser', password: 'pass123' }
      );
      expect(result).toEqual(mockResponse.data);
    });
  });
});