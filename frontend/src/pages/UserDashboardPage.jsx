// frontend/src/pages/UserDashboardPage.jsx
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/useAuth.js'; 
import Navbar from '../components/layout/Navbar.jsx';
import UserSidebar from '../components/layout/UserSidebar.jsx';
import CreateCircleModal from '../components/layout/CreateCircleModal.jsx';
import CreatePost from '../components/layout/CreatePost.jsx';
import { userDashboardService } from '../services/userDashboard.service.js';
import './UserDashboardPage.css';

// Component for displaying a circle card in the dashboard
const CircleCard = ({ circle, onClick }) => {
  const getBadge = (role) => {
    const badges = {
      'owner': '👑',
      'moderator': '🛡️',
      'member': '👤'
    };
    return badges[role] || '👤';
  };

  return (
    <div className="circle-card" onClick={onClick}>
      <h3>{circle.name}</h3>
      <p>{circle.description || 'No description'}</p>
      <div className="circle-meta">
        <span className="badge">{circle.badge || getBadge(circle.role)}</span>
        <span className="role">{circle.role}</span>
        <span className="member-count">{circle.member_count || 0} members</span>
      </div>
    </div>
  );
};

// Component for displaying a post card in the recent activity feed
const PostCard = ({ post }) => {
  return (
    <div className="post-card">
      <h4>{post.title}</h4>
      <p className="post-content">{post.content}</p>
      <div className="post-meta">
        <span>Posted by {post.author_name}</span>
        <span>in {post.circle_name || 'General'}</span>
        <span>{new Date(post.created_at).toLocaleDateString()}</span>
      </div>
    </div>
  );
};

function UserDashboardPage() {
  const { user, logout, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  
  // State for dashboard data
  const [userDashboardData, setUserDashboardData] = useState({
    user: null,
    circles: [],
    posts: [],
    circlesCount: 0,
    postsCount: 0,
    notificationsCount: 0
  });
  
  // State for modals
  const [isCreateCircleModalOpen, setIsCreateCircleModalOpen] = useState(false);
  const [showCreatePost, setShowCreatePost] = useState(false);
  
  // Loading and error states
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // 📌 DEBUG: Log state changes
  useEffect(() => {
    console.log('📌 isCreateCircleModalOpen changed to:', isCreateCircleModalOpen);
  }, [isCreateCircleModalOpen]);

  // Redirect if not authenticated
  useEffect(() => {
    if (!authLoading && !user) {
      navigate('/login');
    }
  }, [user, authLoading, navigate]);

  // Load dashboard data
  useEffect(() => {
    const loadUserDashboard = async () => {
      if (!user) return;
      
      try {
        setLoading(true);
        console.log('📡 Loading dashboard data...');
        const data = await userDashboardService.getUserDashboardData();
        console.log('✅ Dashboard data loaded:', data);
        setUserDashboardData(data);
      } catch (error) {
        console.error('❌ Failed to load user dashboard:', error);
        setError('Failed to load user dashboard data');
      } finally {
        setLoading(false);
      }
    };
    
    loadUserDashboard();
  }, [user]);

  // Handler for when a new circle is created
  const handleCircleCreated = (newCircle) => {
    console.log('🟢 New circle created:', newCircle);
    setUserDashboardData(prev => ({
      ...prev,
      circles: [newCircle, ...prev.circles],
      circlesCount: prev.circlesCount + 1
    }));
  };

  // Handler for when a new post is created
  const handlePostCreated = (newPost) => {
    console.log('🟢 New post created:', newPost);
    setUserDashboardData(prev => ({
      ...prev,
      posts: [newPost, ...prev.posts],
      postsCount: prev.postsCount + 1
    }));
  };

  // Handler for create circle button
  const handleCreateCircleClick = () => {
    console.log('🟢 Create Circle button clicked!');
    console.log('Current state before change:', isCreateCircleModalOpen);
    setIsCreateCircleModalOpen(true);
    console.log('State after set (async, may not show immediately):', isCreateCircleModalOpen);
  };
  
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
        <UserSidebar 
            onCreateCircle={() => setIsCreateCircleModalOpen(true)}
            onCreatePost={() => setShowCreatePost(true)}/>
        
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
                  <p className="stat-number">{userDashboardData.circlesCount}</p>
                </div>
                
                <div className="stat-card">
                  <h3>Recent Posts</h3>
                  <p className="stat-number">{userDashboardData.postsCount}</p>
                </div>
                
                <div className="stat-card">
                  <h3>Notifications</h3>
                  <p className="stat-number">{userDashboardData.notificationsCount}</p>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="action-buttons">
                <button 
                  className="primary-btn"
                  onClick={handleCreateCircleClick}
                >
                  + Create New Circle
                </button>
                
                <button 
                  className="secondary-btn"
                  onClick={() => {
                    console.log('🟢 Toggle post form:', !showCreatePost);
                    setShowCreatePost(!showCreatePost);
                  }}
                >
                  {showCreatePost ? 'Hide' : 'Create New Post'}
                </button>
              </div>

              {/* Create Post Form (conditional) */}
              {showCreatePost && (
                <div className="create-post-section">
                  <CreatePost 
                    onPostCreated={handlePostCreated}
                    circles={userDashboardData.circles}
                  />
                </div>
              )}

              {/* Circles Section with Cards */}
              <section className="circles-section">
                <div className="section-header">
                  <h2>Your Circles</h2>
                </div>
                
                {userDashboardData.circles?.length > 0 ? (
                  <div className="circles-grid">
                    {userDashboardData.circles.map(circle => (
                      <CircleCard 
                        key={circle.id} 
                        circle={circle} 
                        onClick={() => {
                          console.log('🟢 Navigate to circle:', circle.id);
                          navigate(`/circles/${circle.id}`);
                        }}
                      />
                    ))}
                  </div>
                ) : (
                  <div className="empty-state">
                    <p>You haven't joined any circles yet.</p>
                    <button 
                      className="primary-btn"
                      onClick={handleCreateCircleClick}
                    >
                      Create Your First Circle
                    </button>
                  </div>
                )}
              </section>

              {/* Recent Posts Feed */}
              <section className="feed-section">
                <h2>Recent Activity</h2>
                {userDashboardData.posts?.length > 0 ? (
                  <div className="posts-feed">
                    {userDashboardData.posts.map(post => (
                      <PostCard key={post.id} post={post} />
                    ))}
                  </div>
                ) : (
                  <p className="empty-message">
                    No recent posts in your circles.{' '}
                    <button 
                      className="link-btn"
                      onClick={() => {
                        console.log('🟢 Show create post from empty message');
                        setShowCreatePost(true);
                      }}
                    >
                      Create one now!
                    </button>
                  </p>
                )}
              </section>

              {/* 🔥 Debug info - only in development */}
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

      {/* Create Circle Modal */}
      <CreateCircleModal 
        isOpen={isCreateCircleModalOpen}
        onClose={() => {
          console.log('🔴 Closing modal');
          setIsCreateCircleModalOpen(false);
        }}
        onCircleCreated={handleCircleCreated}
      />
    </div>
  );
}

export default UserDashboardPage;