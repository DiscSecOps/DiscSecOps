// frontend/src/pages/RegisterPage.jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthForm } from '../hooks/useAuthForm';
import './RegisterPage.css';

function RegisterPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [fullName, setFullName] = useState('');
  
  // Use useAuthForm instead of direct useAuth
  // This gives us validation, sanitization, and error handling
  const { loading, errors, handleRegister, clearError } = useAuthForm();
  const navigate = useNavigate();

  /**
   * Handle form submission
   * Validation and sanitization are handled by useAuthForm
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Clear previous errors before attempting registration
    clearError('general');
    
    // handleRegister includes:
    // - Rate limiting check
    // - Input validation
    // - Input sanitization
    // - API call via auth context
    const registerSuccess = await handleRegister(
      username,
      email,
      password,
      confirmPassword
    );
    
    if (registerSuccess) {
      const message = `Account created for ${username}! You can now login.`;
      navigate('/login', { state: { success: message } });
    }
  };

  /**
   * Handle input field changes
   * Clear specific field error when user starts typing
   */
  const handleFieldChange = (field, value) => {
    if (field === 'username') setUsername(value);
    if (field === 'email') setEmail(value);
    if (field === 'password') setPassword(value);
    if (field === 'confirmPassword') setConfirmPassword(value);
    if (field === 'fullName') setFullName(value);
    
    // Clear error for this field when user starts typing
    if (errors[field]) {
      clearError(field);
    }
  };

  // Check if submit button should be disabled
  const isSubmitDisabled = loading || !username || !email || !password || !confirmPassword;

  return (
    <div className="register-page">
      <div className="register-container">
        <h1 className="register-title">Create Account</h1>
        
        <form onSubmit={handleSubmit} className="register-form" noValidate>
          {/* Username Field */}
          <div className="form-group">
            <label htmlFor="username">Username *</label>
            <input
              id="username"
              name="username"
              type="text"
              value={username}
              onChange={(e) => handleFieldChange('username', e.target.value)}
              placeholder="Choose a username"
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
            <small className="form-hint">3-30 characters, letters, numbers and underscores only</small>
          </div>
          
          {/* Full Name Field (Optional) */}
          <div className="form-group">
            <label htmlFor="fullName">Full Name (Optional)</label>
            <input
              id="fullName"
              name="fullName"
              type="text"
              value={fullName}
              onChange={(e) => handleFieldChange('fullName', e.target.value)}
              placeholder="Your full name"
              disabled={loading}
            />
          </div>
          
          {/* Email Field */}
          <div className="form-group">
            <label htmlFor="email">Email *</label>
            <input
              id="email"
              name="email"
              type="email"
              value={email}
              onChange={(e) => handleFieldChange('email', e.target.value)}
              placeholder="Your email address"
              disabled={loading}
              className={errors.email ? 'error' : ''}
              aria-invalid={!!errors.email}
              aria-describedby={errors.email ? 'email-error' : undefined}
            />
            {errors.email && (
              <div className="field-error" id="email-error" role="alert">
                {errors.email}
              </div>
            )}
            <small className="form-hint">Required. Please use a valid email address.</small>
          </div>

          {/* Password Field */}
          <div className="form-group">
            <label htmlFor="password">Password *</label>
            <input
              id="password"
              name="password"
              type="password"
              value={password}
              onChange={(e) => handleFieldChange('password', e.target.value)}
              placeholder="Create a password"
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
            <small className="form-hint">At least 8 characters</small>
          </div>
          
          {/* Confirm Password Field */}
          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password *</label>
            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              value={confirmPassword}
              onChange={(e) => handleFieldChange('confirmPassword', e.target.value)}
              placeholder="Confirm your password"
              disabled={loading}
              className={errors.confirmPassword ? 'error' : ''}
              aria-invalid={!!errors.confirmPassword}
              aria-describedby={errors.confirmPassword ? 'confirm-password-error' : undefined}
            />
            {errors.confirmPassword && (
              <div className="field-error" id="confirm-password-error" role="alert">
                {errors.confirmPassword}
              </div>
            )}
          </div>
          
          {/* General error message (API errors, rate limiting, etc.) */}
          {errors.general && (
            <div className="error-message" role="alert">
              {errors.general}
            </div>
          )}
          
          <button
            type="submit"
            className="submit-button"
            disabled={isSubmitDisabled}
          >
            {loading ? 'Creating account...' : 'Create Account'}
          </button>
        </form>
        
        <div className="register-links">
          <p>Already have an account? <a href="/login">Login here</a></p>
          <p className="terms-note">
            By registering, you agree to our <a href="/terms">Terms of Service</a> and <a href="/privacy">Privacy Policy</a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default RegisterPage;