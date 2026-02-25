// frontend/src/components/layout/Navbar.jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/useAuth.js';
import './Navbar.css';

function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [showDropdown, setShowDropdown] = useState(false);
  
  const handleLogout = async () => {
    if (window.confirm('Are you sure you want to logout?')) {
      try {
        await logout();
        navigate('/login');
      } catch (error) {
        console.error('Logout failed:', error);
        alert('Logout failed. Please try again.');
      }
    }
  };
  
  // If no user, show a minimal navbar
  if (!user) {
    return (
      <header className="navbar">
        <div className="navbar-left">
          <div className="navbar-logo" onClick={() => navigate('/')}>
            Social Circles
          </div>
        </div>
        <div className="navbar-right">
          <button className="nav-btn" onClick={() => navigate('/login')}>
            Login
          </button>
          <button className="nav-btn primary" onClick={() => navigate('/register')}>
            Register
          </button>
        </div>
      </header>
    );
  }
  
  return (
    <header className="navbar">
      <div className="navbar-left">
        <div className="navbar-logo" onClick={() => navigate('/user-dashboard')}>
          Social Circles
        </div>
        <div className="navbar-search">
          <input 
            type="text" 
            placeholder="Search circles, posts, people..." 
            className="search-input"
          />
        </div>
      </div>
      
      <div className="navbar-right">
        <button className="navbar-icon" title="Notifications">
          <span className="icon">🔔</span>
          <span className="badge">3</span>
        </button>
        
        <button className="navbar-icon" title="Messages">
          <span className="icon">✉️</span>
        </button>

        <div className="navbar-user" onClick={() => setShowDropdown(!showDropdown)}>
          <div className="user-avatar">
            {user.username?.charAt(0).toUpperCase() || 'U'}
          </div>
          <span className="user-name">@{user.username}</span>
          <span className="dropdown-arrow">{showDropdown ? '▲' : '▼'}</span>
          
          {showDropdown && (
            <div className="user-dropdown">
              <button 
                className="dropdown-item" 
                onClick={() => {
                  setShowDropdown(false);
                  navigate('/profile');
                }}
              >
                Profile
              </button>
              <button 
                className="dropdown-item" 
                onClick={() => {
                  setShowDropdown(false);
                  navigate('/settings');
                }}
              >
                Settings
              </button>
              <div className="dropdown-divider"></div>
              <button className="dropdown-item logout" onClick={handleLogout}>
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

export default Navbar;