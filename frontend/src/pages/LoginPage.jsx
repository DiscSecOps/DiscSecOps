// frontend/src/pages/LoginPage.jsx
import { useState } from 'react';
import { authService } from '../services/auth.service.js';
import './LoginPage.css';
 
// LoginPage component
function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
 
  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
 
    // Call login service
    try {
      const result = await authService.login(username, password);
      console.log('Login successful:', result);
      // TODO: Redirect to feed page
      alert(`Welcome ${result.username}!`);
    } catch (err) {
      setError(err.error || 'Login failed');
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };
 
  // Render login form
  return (
    // login page container
    <div className="login-page">
      <div className="login-container">
        <h1 className="login-title">Login to Social Circles</h1>
       
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
              required
              disabled={loading}
            />
          </div>
         
       
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
              disabled={loading}
            />
          </div>
         
          {error && <div className="error-message">{error}</div>}
         
          <button
            type="submit"
            className="submit-button"
            disabled={loading || !username || !password}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
       
        <div className="login-links">
          <p>Don't have an account? <a href="/register">Register here</a></p>
          <p><a href="/forgot-password">Forgot password?</a></p>
        </div>
      </div>
    </div>
  );
}
 
export default LoginPage;