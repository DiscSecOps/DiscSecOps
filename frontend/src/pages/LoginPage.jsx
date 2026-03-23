// frontend/src/pages/LoginPage.jsx
import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuthForm } from '../hooks/useAuthForm'; 
import './LoginPage.css';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  
  // Get form handling logic from custom hook
  const { loading, errors, handleLogin, clearError } = useAuthForm();
  const navigate = useNavigate();
  const location = useLocation();
  const success = location.state?.success || null;

  /**
   * Handle form submission
   * Validation and sanitization are handled by useAuthForm
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Clear previous errors before attempting login
    clearError('general');
    
    // handleLogin includes:
    // - Rate limiting check
    // - Input validation
    // - Input sanitization
    // - API call via auth context
    const loginSuccess = await handleLogin(username, password);
    
    if (loginSuccess) {
      navigate('/user-dashboard');
    }
  };

  /**
   * Handle input field changes
   * Clear specific field error when user starts typing
   */
  const handleFieldChange = (field, value) => {
    if (field === 'username') setUsername(value);
    if (field === 'password') setPassword(value);
    
    // Clear error for this field when user starts typing
    if (errors[field]) {
      clearError(field);
    }
  };

  // Check if submit button should be disabled
  const isSubmitDisabled = loading || !username || !password;

  return (
    <div className="login-page">
      <div className="login-container">
        <h1 className="login-title">Login to Social Circles</h1>
        
        <form onSubmit={handleSubmit} className="login-form" noValidate>
          {/* Username Field */}
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              name="username"
              type="text"
              value={username}
              onChange={(e) => handleFieldChange('username', e.target.value)}
              placeholder="Enter your username"
              disabled={loading}
              className={errors.username ? 'error' : ''}
              aria-invalid={!!errors.username}
              aria-describedby={errors.username ? 'username-error' : undefined}
            />
            {errors.username && (
              <div className="field-error" id="username-error" role="alert">
                {errors.username}
              </div>
            )}
          </div>
          
          {/* Password Field */}
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              value={password}
              onChange={(e) => handleFieldChange('password', e.target.value)}
              placeholder="Enter your password"
              disabled={loading}
              className={errors.password ? 'error' : ''}
              aria-invalid={!!errors.password}
              aria-describedby={errors.password ? 'password-error' : undefined}
            />
            {errors.password && (
              <div className="field-error" id="password-error" role="alert">
                {errors.password}
              </div>
            )}
          </div>
          
          {/* Success message (from registration) */}
          {success && (
            <div className="success-message" role="status">
              {success}
            </div>
          )}
          
          {/* General error message (API errors, rate limiting, etc.) */}
          {errors.general && (
            <div className="error-message" role="alert">
              {errors.general}
            </div>
          )}
          
          {/* Submit Button */}
          <button 
            type="submit"
            className="submit-button"
            disabled={isSubmitDisabled}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        
        {/* Links */}
        <div className="login-links">
          <p>Don't have an account? <a href="/register">Register here</a></p>
          <p><a href="/forgot-password">Forgot password?</a></p>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;