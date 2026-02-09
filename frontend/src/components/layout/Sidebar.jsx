// frontend/src/components/layout/Sidebar.jsx
import { useNavigate, useLocation } from 'react-router-dom';
import './Sidebar.css';

function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();
  
  // Determină item-ul activ bazat pe URL
  const getActiveItem = () => {
    if (location.pathname === '/dashboard') return 'Home';
    if (location.pathname.includes('/circles')) return 'My Circles';
    if (location.pathname.includes('/explore')) return 'Explore';
    if (location.pathname.includes('/create-post')) return 'Create Post';
    if (location.pathname.includes('/create-circle')) return 'Create Circle';
    if (location.pathname.includes('/settings')) return 'Settings';
    return 'Home';
  };
  
  const activeItem = getActiveItem();
  
  const menuItems = [
    { icon: '🏠', label: 'Home', path: '/dashboard' },
    { icon: '👥', label: 'My Circles', path: '/circles' },
    { icon: '🔍', label: 'Explore', path: '/explore' },
    { icon: '✏️', label: 'Create Post', path: '/create-post' },
    { icon: '➕', label: 'Create Circle', path: '/create-circle' },
  ];
  
  const secondaryItems = [
    { icon: '⚙️', label: 'Settings', path: '/settings' },
    { icon: '❓', label: 'Help & Support', path: '/help' },
  ];

  const handleItemClick = (path) => {
    navigate(path);
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
            className={`sidebar-item ${activeItem === item.label ? 'active' : ''}`}
            onClick={() => handleItemClick(item.path)}
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
            className={`sidebar-item ${activeItem === item.label ? 'active' : ''}`}
            onClick={() => handleItemClick(item.path)}
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

export default Sidebar;