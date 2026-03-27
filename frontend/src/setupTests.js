// frontend/src/setupTests.js
import '@testing-library/jest-dom';
import { afterEach, vi } from 'vitest';

// Clear mocks after each test to prevent interference between tests
afterEach(() => {
  vi.clearAllMocks();
  vi.restoreAllMocks();
});