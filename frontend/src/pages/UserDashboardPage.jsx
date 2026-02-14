// frontend/src/pages/UserDashboardPage.jsx
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/useAuth.js'; 
import Navbar from '../components/layout/Navbar.jsx';
import UserSidebar from '../components/layout/UserSidebar.jsx';
import { userDashboardService } from '../services/userDashboard.service.js';
import './UserDashboardPage.css';

function UserDashboardPage() {
  const { user, logout, loading: authLoading } = useAuth();
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
      if (!user) return;
      
      try {
        const data = await userDashboardService.getUserDashboardData();
        setUserDashboardData(data);
      } catch (error) {
        console.error('Failed to load user dashboard:', error);
        setError('Failed to load user dashboard data');
      } finally {
        setLoading(false);
      }
    };
    
    loadUserDashboard();
  }, [user]);
  
  if (authLoading) {
    return (
      <div className="dashboard-layout">
        <div className="loading-spinner">Loading...</div>
      </div>
    );
  }
  
  if (!user) {
    return null;
  }
  
  return (
    <div className="dashboard-layout">
      <Navbar user={user} onLogout={logout} />
      
      <div className="dashboard-content">
        <UserSidebar />
        
        <main className="dashboard-main">
          <div className="welcome-section">
            <h1>Welcome back, {user.full_name || user.username}! 👋</h1>
            <p>Here's what's happening in your circles.</p>
          </div>
          
          {error && <div className="error-message">{error}</div>}
          
          {loading ? (
            <div className="loading-spinner">Loading dashboard data...</div>
          ) : (
            <>
              {/* Statistics */}
              <div className="stats-grid">
                <div className="stat-card">
                  <h3>Your Circles</h3>
                  <p className="stat-number">
                    {userDashboardData?.circlesCount || 0}
                  </p>
                </div>
                
                <div className="stat-card">
                  <h3>Recent Posts</h3>
                  <p className="stat-number">
                    {userDashboardData?.postsCount || 0}
                  </p>
                </div>
                
                <div className="stat-card">
                  <h3>Notifications</h3>
                  <p className="stat-number">
                    {userDashboardData?.notificationsCount || 0}
                  </p>
                </div>
              </div>

              {/* Sections for recent content */}
              <div className="recent-content">
                <section className="content-section">
                  <h2>Your Circles</h2>
                  {userDashboardData?.circles?.length > 0 ? (
                    <ul className="items-list">
                      {userDashboardData.circles.map(circle => (
                        <li key={circle.id}>{circle.name}</li>
                      ))}
                    </ul>
                  ) : (
                    <p className="empty-message">You haven't joined any circles yet.</p>
                  )}
                </section>

                <section className="content-section">
                  <h2>Recent Posts</h2>
                  {userDashboardData?.posts?.length > 0 ? (
                    <ul className="items-list">
                      {userDashboardData.posts.map(post => (
                        <li key={post.id}>{post.title}</li>
                      ))}
                    </ul>
                  ) : (
                    <p className="empty-message">No recent posts to show.</p>
                  )}
                </section>
              </div>

              {/* 🔥 Optional, data  in JSON format for development only - debbuging*/}
              {import.meta.env.DEV && (  
                <details className="debug-info">
                  <summary>Debug: Raw Data</summary>
                  <pre>{JSON.stringify(userDashboardData, null, 2)}</pre>
                </details>
              )}
            </>
          )}
        </main>
      </div>
    </div>
  );
}

export default UserDashboardPage;