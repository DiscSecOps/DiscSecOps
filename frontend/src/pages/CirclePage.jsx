// frontend/src/pages/CirclePage.jsx
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/useAuth.js';
import Navbar from '../components/layout/Navbar.jsx';
import UserSidebar from '../components/layout/UserSidebar.jsx';
import CreatePost from '../components/layout/CreatePost.jsx';
import { circleService } from '../services/circle.service';
import { postService } from '../services/post.service';
import './CirclePage.css';

// Component for displaying a member with badge
const MemberCard = ({ member, isOwner }) => {
  const getBadge = (role) => {
    const badges = {
      'owner': '👑',
      'moderator': '🛡️',
      'member': '👤'
    };
    return badges[role] || '👤';
  };

  return (
    <div className="member-card">
      <div className="member-avatar">
        {member.username?.charAt(0).toUpperCase() || 'U'}
      </div>
      <div className="member-info">
        <div className="member-name">
          {member.username}
          {isOwner && <span className="owner-tag"> (Owner)</span>}
        </div>
        <div className="member-role">
          <span className="member-badge">{member.badge || getBadge(member.role)}</span>
          <span className="member-role-text">{member.role}</span>
        </div>
      </div>
      <div className="member-joined">
        Joined: {new Date(member.joined_at).toLocaleDateString()}
      </div>
    </div>
  );
};

// Component for displaying a post in the circle
const PostCard = ({ post }) => {
  return (
    <div className="circle-post-card">
      <div className="post-header">
        <div className="post-author-avatar">
          {post.author_name?.charAt(0).toUpperCase() || 'U'}
        </div>
        <div className="post-author-info">
          <div className="post-author">{post.author_name}</div>
          <div className="post-date">{new Date(post.created_at).toLocaleDateString()}</div>
        </div>
      </div>
      <div className="post-content">
        <h4>{post.title}</h4>
        <p>{post.content}</p>
      </div>
      <div className="post-actions">
        <button className="post-action-btn">❤️ Like</button>
        <button className="post-action-btn">💬 Comment</button>
        <button className="post-action-btn">🔄 Share</button>
      </div>
    </div>
  );
};

function CirclePage() {
  const { circleId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [circle, setCircle] = useState(null);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreatePost, setShowCreatePost] = useState(false);
  const [activeTab, setActiveTab] = useState('posts');

  // Load circle data when circleId changes
  useEffect(() => {
    const fetchCircleData = async () => {
      try {
        setLoading(true);
        setError('');
        
        const [circleData, postsData] = await Promise.all([
          circleService.getCircle(circleId),
          postService.getCirclePosts(circleId)
        ]);
        
        setCircle(circleData);
        setPosts(postsData || []);
      } catch (err) {
        console.error('Failed to load circle:', err);
        if (err.response?.status === 403) {
          setError('You are not a member of this circle');
        } else if (err.response?.status === 404) {
          setError('Circle not found');
        } else {
          setError('Failed to load circle data');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchCircleData();
  }, [circleId]); // ✅ dependența corectă

  const handlePostCreated = (newPost) => {
    setPosts([newPost, ...posts]);
    setShowCreatePost(false);
  };

  const getCurrentUserRole = () => {
    if (!circle || !user) return null;
    const currentMember = circle.members?.find(m => m.user_id === user.id);
    return currentMember?.role || null;
  };

  if (loading) {
    return (
      <div className="dashboard-layout">
        <Navbar />
        <div className="dashboard-content">
          <UserSidebar />
          <main className="dashboard-main">
            <div className="loading-spinner">Loading circle...</div>
          </main>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-layout">
        <Navbar />
        <div className="dashboard-content">
          <UserSidebar />
          <main className="dashboard-main">
            <div className="error-container">
              <h2>Error</h2>
              <p>{error}</p>
              <button className="primary-btn" onClick={() => navigate('/user-dashboard')}>
                Back to Dashboard
              </button>
            </div>
          </main>
        </div>
      </div>
    );
  }

  if (!circle) return null;

  const currentUserRole = getCurrentUserRole();
  const isOwner = currentUserRole === 'owner';
  const isModerator = currentUserRole === 'moderator';

  return (
    <div className="dashboard-layout">
      <Navbar />
      
      <div className="dashboard-content">
        <UserSidebar />
        
        <main className="dashboard-main circle-page">
          {/* Circle Header */}
          <div className="circle-header">
            <div className="circle-header-content">
              <button className="back-btn" onClick={() => navigate('/user-dashboard')}>
                ← Back to Dashboard
              </button>
              
              <div className="circle-title-section">
                <h1>{circle.name}</h1>
                <div className="circle-badge">
                  {isOwner && '👑 Owner'}
                  {isModerator && '🛡️ Moderator'}
                </div>
              </div>
              
              <p className="circle-description">{circle.description || 'No description'}</p>
              
              <div className="circle-stats">
                <div className="stat">
                  <span className="stat-value">{circle.member_count}</span>
                  <span className="stat-label">Members</span>
                </div>
                <div className="stat">
                  <span className="stat-value">{posts.length}</span>
                  <span className="stat-label">Posts</span>
                </div>
                <div className="stat">
                  <span className="stat-value">📅</span>
                  <span className="stat-label">
                    Created {new Date(circle.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="circle-actions">
                <button 
                  className="primary-btn"
                  onClick={() => setShowCreatePost(!showCreatePost)}
                >
                  {showCreatePost ? 'Cancel' : '+ Create Post'}
                </button>
                
                {(isOwner || isModerator) && (
                  <button className="secondary-btn">
                    Manage Members
                  </button>
                )}
                
                {isOwner && (
                  <button className="secondary-btn danger">
                    Settings
                  </button>
                )}
              </div>

              {/* Create Post Form */}
              {showCreatePost && (
                <div className="create-post-section">
                  <CreatePost 
                    onPostCreated={handlePostCreated}
                    circles={[circle]}
                    selectedCircleId={circle.id}
                  />
                </div>
              )}
            </div>
          </div>

          {/* Tabs */}
          <div className="circle-tabs">
            <button 
              className={`tab ${activeTab === 'posts' ? 'active' : ''}`}
              onClick={() => setActiveTab('posts')}
            >
              Posts ({posts.length})
            </button>
            <button 
              className={`tab ${activeTab === 'members' ? 'active' : ''}`}
              onClick={() => setActiveTab('members')}
            >
              Members ({circle.member_count})
            </button>
          </div>

          {/* Tab Content */}
          <div className="tab-content">
            {activeTab === 'posts' && (
              <div className="posts-section">
                {posts.length > 0 ? (
                  posts.map(post => (
                    <PostCard key={post.id} post={post} />
                  ))
                ) : (
                  <div className="empty-state">
                    <p>No posts in this circle yet.</p>
                    <button 
                      className="primary-btn"
                      onClick={() => setShowCreatePost(true)}
                    >
                      Create First Post
                    </button>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'members' && (
              <div className="members-section">
                <div className="members-grid">
                  {circle.members?.map(member => (
                    <MemberCard 
                      key={member.user_id} 
                      member={member}
                      isOwner={member.role === 'owner'}
                    />
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Debug info */}
          {import.meta.env.DEV && (
            <details className="debug-info">
              <summary>Debug: Circle Data</summary>
              <pre>{JSON.stringify(circle, null, 2)}</pre>
            </details>
          )}
        </main>
      </div>
    </div>
  );
}

export default CirclePage;