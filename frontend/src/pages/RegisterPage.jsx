// frontend/src/pages/RegisterPage.jsx
import { useState } from 'react';
import { useAuth } from '../contexts/useAuth.js'; 
import './RegisterPage.css';

function RegisterPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [fullName, setFullName] = useState(''); 
  const [email, setEmail] = useState('');
  
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
  
  if (username.length < 3 || username.length > 20) {
    setError('Username must be between 3 and 20 characters');
    return;
  }

  if (email && !/\S+@\S+\.\S+/.test(email)) {
  setError('Please enter a valid email address');
  return;
}

if (fullName && fullName.length < 2) {
  setError('Full name must be at least 2 characters if provided');
  return;
}

  try {
    // Construct the user data object to send to the backend
    const userData = {
      username,
      password,
      full_name: fullName, 
      email
    };
    
    const result = await register(userData);  // send the whole object to the register function
    console.log('Registration successful:', result);
    
    setSuccess(`Account created for ${result.username || username}! You can now login.`);
    
    // Clear form
    setUsername('');
    setPassword('');
    setConfirmPassword('');
    setFullName('');
    setEmail('');
    
  } catch (err) {
    setError(err.message || 'Registration failed');
    console.error('Registration error:', err);
  }
};

  return (
    <div className="register-page">
      <div className="register-container">
        <h1 className="register-title">Create Account</h1>
        
        <form onSubmit={handleSubmit} className="register-form">

          {/* Username Field */}
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
            <small className="form-hint">3-20 characters, letters,numbers and underscores only</small>
          </div>
          
          {/* Full Name Field */}
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
          
          {/* Email Field */}
          <div className="form-group">
            <label htmlFor="email">Email *</label>
            <input
              name='email'
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Your email address"
              required
              disabled={loading}
            />
            <small className="form-hint">Required. Please use a valid email address.</small>
          </div>

          {/* Password Field */}
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
            <small className="form-hint">At least 8 characters must include letters,numbers and special characters</small>
          </div>
          
          {/* Confirm Password Field */}
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