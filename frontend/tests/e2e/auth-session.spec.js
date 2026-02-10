import { test, expect } from '@playwright/test';

test.describe('Authentication Session', () => {
  test('Login should set session cookie and redirect to dashboard', async ({ page, context }) => {
    // Navigate to login page
    await page.goto('/login');

    // Fill login form
    // Note: Depends on seeded user 'testuser' with password 'password123'
    await page.locator('#username').fill('testuser');
    await page.locator('#password').fill('password123');

    // Submit
    await page.getByRole('button', { name: 'Login' }).click();

    // Verify redirection to dashboard
    await expect(page).toHaveURL('/dashboard');

    // Verify session cookie
    const cookies = await context.cookies();
    const sessionCookie = cookies.find(c => c.name === 'session_token');
    
    expect(sessionCookie, 'Session cookie "session_token" should be present').toBeDefined();
    if (sessionCookie) {
        expect(sessionCookie.httpOnly, 'Cookie should be HttpOnly').toBe(true);
        expect(sessionCookie.sameSite, 'Cookie SameSite should be Lax').toBe('Lax');
    }
  });
});
