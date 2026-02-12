// frontend/src/pages/UserDashboardPage.jsx
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // 👈 Import useNavigate for redirection
import { useAuth } from '../contexts/useAuth.js'; 
import Navbar from '../components/layout/Navbar.jsx';
import UserSidebar from '../components/layout/UserSidebar.jsx';
import { userDashboardService } from '../services/userDashboard.service.js';
import './UserDashboardPage.css';

function UserDashboardPage() {
  const { user, logout, loading: authLoading } = useAuth(); // 👈 Include logout
  const navigate = useNavigate();
  
  const [userDashboardData, setUserDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Redirect if not authenticated
  useEffect(() => {
    if (!authLoading && !user) {
      navigate('/login');
    }
  }, [user, authLoading, navigate]);

  useEffect(() => {
    const loadUserDashboard = async () => {
      if (!user) return; // Don't load if no user
      
      try {
        // 👇 userDashboardService must use withCredentials: true!
        const data = await userDashboardService.getUserDashboardData();
        setUserDashboardData(data);
      } catch (error) {
        console.error('Failed to load user dashboard:', error);
        setError('Failed to load user dashboard data');
        
        // If 401/403, user might be logged out
        if (error.response?.status === 401 || error.response?.status === 403) {
          // Optional: auto-logout
          // logout();
          // navigate('/login');
        }
      } finally {
        setLoading(false);
      }
    };
    
    loadUserDashboard();
  }, [user]); // 👈 Re-load when user changes
  
  // Show loading while checking auth
  if (authLoading) {
    return (
      <div className="dashboard-layout">
        <div className="loading-spinner">Loading...</div>
      </div>
    );
  }
  
  // Show message if no user (though redirect should happen)
  if (!user) {
    return null; // Redirect will happen
  }
  
  return (
    <div className="dashboard-layout">
      <Navbar user={user} onLogout={logout} /> {/* 👈  logout function passed down */}
      
      <div className="dashboard-content">
        <UserSidebar />
        
        <main className="dashboard-main">
          <div className="welcome-section">
            <h1>Welcome back, {user.username}!{user.full_name ? ` (${user.full_name})` : ''} 👋</h1>
            <p>Here's what's happening in your circles.</p>
          </div>
          
          {error && <div className="error-message">{error}</div>}
          
          {loading ? (
            <div className="loading-spinner">Loading dashboard data...</div>
          ) : (
            <div className="dashboard-cards">
              <div className="card">Your Circles (0)</div>
              <div className="card">Recent Posts (0)</div>
              <div className="card">Notifications (0)</div>
              
              {/* Show actual dashboard data if available */}
              {userDashboardData && (
                <div className="dashboard-stats">
                  <pre>{JSON.stringify(userDashboardData, null, 2)}</pre>
                </div>
              )}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default UserDashboardPage;