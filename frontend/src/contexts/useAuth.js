// frontend/src/contexts/useAuth.js
import { useContext } from 'react';
import { AuthContext } from './AuthProvider';

// this hook is a simple wrapper around useContext to make sure we are using it within a AuthProvider
// and to provide a nicer API to the components that consume the context
export const useAuth = () => {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  
  return context;
};