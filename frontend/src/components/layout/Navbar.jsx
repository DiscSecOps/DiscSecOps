// frontend/src/components/layout/Navbar.jsx
import { useAuth } from '../../contexts/useAuth.js'; // 👈 Import useAuth for user info and logou   t
import './Navbar.css';

function Navbar() {
  const { user, logout } = useAuth();
  
  const handleLogout = async () => {
    if (window.confirm('Are you sure you want to logout?')) {
      try {
        await logout(); // 👈 wait logout
        //After logout, the DashboardPage will handle redirection to /login
      } catch (error) {
        console.error('Logout failed:', error);
        alert('Logout failed. Please try again.');
      }
    }
  };
  
  // If no user, show a minimal navbar (though DashboardPage should redirect to /login)
  if (!user) {
    return (
      <header className="navbar">
        <div className="navbar-left">
          <div className="navbar-logo">Social Circles</div>
        </div>
        <div className="navbar-right">
          <span>Not logged in</span>
        </div>
      </header>
    );
  }
  
  return (
    <header className="navbar">
      <div className="navbar-left">
        <div className="navbar-logo">Social Circles</div>
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

        <div className="navbar-user">
          <div className="user-avatar">
            {user.username?.charAt(0).toUpperCase() || 'U'}
          </div>
          <span className="user-name">@{user.username}</span>
          
          <div className="user-dropdown">
            <button className="dropdown-item">Profile</button>
            <button className="dropdown-item">Settings</button>
            <div className="dropdown-divider"></div>
            <button className="dropdown-item logout" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Navbar;