// frontend/tests/helpers/mock-config.js
import { vi } from 'vitest';

export const mockConfig = () => {
  vi.mock('../../src/config', () => ({
    API_BASE_URL: 'http://mocked-for-tests.local'
  }));
};