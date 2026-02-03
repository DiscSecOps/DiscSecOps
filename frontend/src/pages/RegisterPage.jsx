// frontend/src/pages/RegisterPage.jsx
import { useState } from 'react';
import { authService } from '../services/auth.service.js';
import './RegisterPage.css';

// Registration Page Component
function RegisterPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    
    // Validation
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    // Simple username validation add here
    //const usernameRegex = /^[a-zA-Z0-9]{3,20}$/;
    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }
    
    setLoading(true);

    // Call registration service
    try {
      const result = await authService.register(username, password);
      console.log('Registration successful:', result);
      setSuccess(`Account created for ${result.username}! You can now login.`);
      // Clear form
      setUsername('');
      setPassword('');
      setConfirmPassword('');
    } catch (err) {
      setError(err.error || 'Registration failed');
      console.error('Registration error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Render registration form
  return (
    <div className="register-page">
      <div className="register-container">
        <h1 className="register-title">Create Account</h1>
        
        <form onSubmit={handleSubmit} className="register-form">
          <div className="form-group">
            <label htmlFor="username">Username *</label>
            <input
              name='username'
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Choose a username"
              required
              disabled={loading}
              minLength="3"
              maxLength="20"
            />
            <small className="form-hint">3-20 characters, letters and numbers only</small>
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Password *</label>
            <input
              name='password'
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Create a password"
              required
              disabled={loading}
              minLength="6"
            />
            <small className="form-hint">At least 6 characters</small>
          </div>
          
          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password *</label>
            <input
              name='confirmPassword'
              id="confirmPassword"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm your password"
              required
              disabled={loading}
            />
          </div>
          
          {error && <div className="error-message">{error}</div>}
          {success && <div className="success-message">{success}</div>}
          
          <button 
            type="submit" 
            className="submit-button"
            disabled={loading || !username || !password || !confirmPassword}
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