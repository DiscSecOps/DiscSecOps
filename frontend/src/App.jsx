// frontend/src/App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage.jsx';
import RegisterPage from './pages/RegisterPage.jsx';
import UserDashboardPage from './pages/UserDashboardPage.jsx';
import CirclePage from './pages/CirclePage.jsx';
//import ExplorePage from './pages/ExplorePage.jsx';
//import SettingsPage from './pages/SettingsPage.jsx';
//import HelpPage from './pages/HelpPage.jsx';
import ProtectedRoute from './routes/ProtectedRoute.jsx';
import AuthProvider from './contexts/AuthProvider';
import { DarkModeProvider } from './contexts/DarkModeProvider'; 
import './App.css';

function App() {
  return (
    <AuthProvider>
      <DarkModeProvider>
      <Router>
        <Routes>
          {/* Public routes */}
          <Route path="/" element={<LoginPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Protected routes */}
          <Route path="/user-dashboard" element={
            <ProtectedRoute>
              <UserDashboardPage />
            </ProtectedRoute>
          } />

          <Route path="/circles/:circleId" element={
            <ProtectedRoute>
              <CirclePage />
            </ProtectedRoute>
          } />
          
           {/* Commented out until pages are created */}
            {/* 
          <Route path="/explore" element={
            <ProtectedRoute>
              <ExplorePage />
            </ProtectedRoute>
          } />
          
          <Route path="/settings" element={
            <ProtectedRoute>
              <SettingsPage />
            </ProtectedRoute>
          } />
          
          <Route path="/help" element={
            <ProtectedRoute>
              <HelpPage />
            </ProtectedRoute>
          } />
            */}
        </Routes>
      </Router>
      </DarkModeProvider>
    </AuthProvider>
  );
}

export default App;