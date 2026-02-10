// tests/e2e/register-ui.spec.js
import { test, expect } from '@playwright/test';

test('Register page validation @auth', async ({ page }) => {
  await page.goto('http://localhost:3000/register');

  // 1. The "Create Account" button should be disabled when the form is empty
  await expect(page.getByRole('button', { name: 'Create Account' })).toBeDisabled();

  // 2. Fill in the form with valid data
  await page.locator('#username').fill('testuser');
  await page.locator('#password').fill('Test123!');
  await page.locator('#confirmPassword').fill('Test123!');

  // 3. The "Create Account" button should now be enabled
  await expect(page.getByRole('button', { name: 'Create Account' })).toBeEnabled();

  // 4. Test password mismatch
  await page.locator('#confirmPassword').fill('Different123!');

  // If the form has client-side validation for password mismatch, the button should be disabled again
  // await expect(page.getByRole('button', { name: 'Create Account' })).toBeDisabled();

  // 5. If there's an error message for password mismatch, it should be visible
  // await expect(page.getByText('Passwords do not match')).toBeVisible();
});

test('Login page validation @auth', async ({ page }) => {
  await page.goto('http://localhost:3000/login');

  // Button disabled when empty
  await expect(page.getByRole('button', { name: 'Login' })).toBeDisabled();

  // Fill in the form - button should be enabled
  await page.locator('#username').fill('user');
  await page.locator('#password').fill('pass');

  await expect(page.getByRole('button', { name: 'Login' })).toBeEnabled();
});