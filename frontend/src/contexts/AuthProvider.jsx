// frontend/src/contexts/AuthProvider.jsx
import { createContext, useState, useEffect } from 'react';
import { authService } from '../services/auth.service';

// This context will hold the authentication state and functions for login, register, and logout
const AuthContext = createContext(); export { AuthContext };

// The AuthProvider component will wrap the app and provide the authentication context to its children
const AuthProvider = ({ children }) => {

  const [user, setUser] = useState(null); 
  const [loading, setLoading] = useState(true); 

  // On component mount, we check if there is an existing authentication session and set the user state accordingly
  useEffect(() => {
    const checkExistingAuth = async () => {
      try {
        const authResult = await authService.checkAuth();
        if (authResult.authenticated && authResult.user) {
          setUser(authResult.user);
        }
      } catch (error) {
        console.warn('No existing auth session:', error);
      } finally {
        setLoading(false);
      }
    };

    checkExistingAuth();
  }, []);

  // The login function will call the authService to perform login and update the user state
  const login = async (username, password) => {
    try {
      const result = await authService.login(username, password);
      if (result.success) {
        setUser(result.user);
      }
      return result;
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  // The register function will call the authService to perform registration and return the result
  const register = async (username, password, full_name = '') => {
    try {
      const result = await authService.register(username, password, full_name);
      return result;
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    }
  };

  // The logout function will call the authService to perform logout and clear the user state
  const logout = async () => {
    try {
      await authService.logout();
      setUser(null);
    } catch (error) {
      console.warn('Logout error:', error);
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;