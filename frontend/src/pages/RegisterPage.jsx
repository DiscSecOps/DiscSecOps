// frontend/src/pages/RegisterPage.jsx
import { useState } from 'react';
import { useAuth } from '../contexts/useAuth.js';
import './RegisterPage.css';

function RegisterPage() {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [fullName, setFullName] = useState('');

  const { register, loading } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Validation
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    // Optional username validation if provided
    if (username && (username.length < 3 || username.length > 20)) {
      setError('Username must be between 3 and 20 characters');
      return;
    }

    // Call registration via AuthContext
    try {
      const result = await register(email, password, username, fullName);
      console.log('Registration successful:', result);

      setSuccess(`Account created for ${email}! You can now login.`);

      // Clear form
      setEmail('');
      setUsername('');
      setPassword('');
      setConfirmPassword('');
      setFullName('');

    } catch (err) {
      // err is expected to be an Error object with a message property
      setError(err.message || 'Registration failed');
      console.error('Registration error:', err);
    }
  };

  return (
    <div className="register-page">
      <div className="register-container">
        <h1 className="register-title">Create Account</h1>

        <form onSubmit={handleSubmit} className="register-form">
          <div className="form-group">
            <label htmlFor="email">Email *</label>
            <input
              name='email'
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="username">Username (Optional)</label>
            <input
              name='username'
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Choose a username"
              disabled={loading}
              minLength="3"
              maxLength="20"
            />
            <small className="form-hint">3-20 characters, letters and numbers only</small>
          </div>

          <div className="form-group">
            <label htmlFor="fullName">Full Name (Optional)</label>
            <input
              name='fullName'
              id="fullName"
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="Your full name"
              disabled={loading}
            />
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
            disabled={loading || !email || !password || !confirmPassword}
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