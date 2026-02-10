// frontend/tests/unit/auth.service.test.js
import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';
import { authService } from '../../src/services/auth.service.js';

vi.mock('axios');

describe('Auth Service', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('login', () => {
    it('should login successfully', async () => {
      const mockResponse = {
        data: {
          success: true,
          user: { username: 'testuser', id: 1 }
        }
      };
      
      axios.post.mockResolvedValue(mockResponse);

      const result = await authService.login('testuser', 'pass123');
      
      // CORECTAT: include withCredentials
      expect(axios.post).toHaveBeenCalledWith(
        'http://localhost:8000/api/auth/login',
        { username: 'testuser', password: 'pass123' },
        { withCredentials: true }
      );
      
      expect(result).toEqual(mockResponse.data);
    });

    it('should handle login error', async () => {
      const errorResponse = {
        response: {
          data: { detail: 'Invalid credentials' }
        }
      };
      
      axios.post.mockRejectedValue(errorResponse);

      // CORECTAT: expect Error object
      await expect(authService.login('wrong', 'pass'))
        .rejects.toThrow('Invalid credentials');
    });
  });

  describe('register', () => {
    it('should register successfully', async () => {
      const mockResponse = {
        data: {
          success: true,
          username: 'newuser'
        }
      };
      
      axios.post.mockResolvedValue(mockResponse);

      const result = await authService.register('newuser', 'pass123');
      
      // CORECTAT: include full_name default
      expect(axios.post).toHaveBeenCalledWith(
        'http://localhost:8000/api/auth/register',
        { username: 'newuser', password: 'pass123', full_name: '' }
      );
      
      expect(result).toEqual(mockResponse.data);
    });
  });
});