// frontend/src/App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage.jsx';
import RegisterPage from './pages/RegisterPage.jsx';
import UserDashboardPage from './pages/UserDashboardPage.jsx'; 
import ProtectedRoute from './routes/ProtectedRoute.jsx'; 
import AuthProvider from './contexts/AuthProvider'; 
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Protected routes */}
          <Route path="/user-dashboard" element={
            <ProtectedRoute>
              <UserDashboardPage />
            </ProtectedRoute>
          } />

              <Route path="/circles" element={
                <ProtectedRoute>
                  <div>My Circles Page (TODO)</div>
                </ProtectedRoute>
              } />
              
              <Route path="/explore" element={
                <ProtectedRoute>
                  <div>Explore Page (TODO)</div>
                </ProtectedRoute>
              } />
              
              <Route path="/create-post" element={
                <ProtectedRoute>
                  <div>Create Post Page (TODO)</div>
                </ProtectedRoute>
              } />
              
              <Route path="/create-circle" element={
                <ProtectedRoute>
                  <div>Create Circle Page (TODO)</div>
                </ProtectedRoute>
              } />
              
              <Route path="/settings" element={
                <ProtectedRoute>
                  <div>Settings Page (TODO)</div>
                </ProtectedRoute>
              } />
              
              <Route path="/help" element={
                <ProtectedRoute>
                  <div>Help & Support Page (TODO)</div>
                </ProtectedRoute>
              } />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;