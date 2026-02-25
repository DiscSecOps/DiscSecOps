// frontend/src/components/layout/UserSidebar.jsx
import { useNavigate, useLocation } from 'react-router-dom';
import './UserSidebar.css';

function UserSidebar() {
  const navigate = useNavigate();
  const location = useLocation();
  
  const menuItems = [
    { icon: '🏠', label: 'Home', path: '/user-dashboard' },
    { icon: '👥', label: 'My Circles', path: '/circles' },
    { icon: '🔍', label: 'Explore', path: '/explore' },
    { icon: '✏️', label: 'Create Post', path: '/user-dashboard' }, // redirect to dashboard (modal)
    { icon: '➕', label: 'Create Circle', path: '/user-dashboard' }, // redirect to dashboard (modal)
  ];
  
  const secondaryItems = [
    { icon: '⚙️', label: 'Settings', path: '/settings' },
    { icon: '❓', label: 'Help & Support', path: '/help' },
  ];

  const handleItemClick = (path, label) => {
    if (label === 'Create Post') {
      // TODO: Trigger create post modal
      console.log('Open create post modal');
      // U can also set some state here to indicate which modal to open if you want to reuse the same modal component
    } else if (label === 'Create Circle') {
      // TODO: Trigger create circle modal
      console.log('Open create circle modal');
    } else {
      navigate(path);
    }
  };

  const isActive = (path) => {
    if (path === '/user-dashboard' && location.pathname === '/user-dashboard') return true;
    if (path === '/circles' && location.pathname.includes('/circles')) return true;
    if (path === '/explore' && location.pathname.includes('/explore')) return true;
    if (path === '/settings' && location.pathname.includes('/settings')) return true;
    if (path === '/help' && location.pathname.includes('/help')) return true;
    return false;
  };
  
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h3 className="sidebar-title">Navigation</h3>
      </div>
      
      <nav className="sidebar-nav">
        {menuItems.map((item, index) => (
          <button 
            key={index}
            className={`sidebar-item ${isActive(item.path) ? 'active' : ''}`}
            onClick={() => handleItemClick(item.path, item.label)}
            title={item.label}
          >
            <span className="sidebar-icon">{item.icon}</span>
            <span className="sidebar-label">{item.label}</span>
          </button>
        ))}
        
        <div className="sidebar-divider"></div>
        
        {secondaryItems.map((item, index) => (
          <button 
            key={index} 
            className={`sidebar-item ${isActive(item.path) ? 'active' : ''}`}
            onClick={() => navigate(item.path)}
            title={item.label}
          >
            <span className="sidebar-icon">{item.icon}</span>
            <span className="sidebar-label">{item.label}</span>
          </button>
        ))}
      </nav>
      
      <div className="sidebar-footer">
        <div className="user-status">
          <span className="status-dot online"></span>
          <small>Online</small>
        </div>
        <small className="sidebar-hint">Click any item to navigate</small>
      </div>
    </aside>
  );
}

export default UserSidebar;