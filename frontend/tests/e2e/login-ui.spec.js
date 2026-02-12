// tests/e2e/login-ui.spec.js
import { test, expect } from '@playwright/test';

test('Login page UI @auth', async ({ page }) => {
  await page.goto('http://localhost:3000/login');

  await expect(page.getByText('Login to Social Circles')).toBeVisible();
  await expect(page.locator('#email')).toBeVisible();
  await expect(page.locator('#password')).toBeVisible();
  await expect(page.getByRole('button', { name: 'Login' })).toBeVisible();

  // Button state
  await expect(page.getByRole('button', { name: 'Login' })).toBeDisabled();

  await page.locator('#email').fill('test@example.com');
  await page.locator('#password').fill('test');

  await expect(page.getByRole('button', { name: 'Login' })).toBeEnabled();
});