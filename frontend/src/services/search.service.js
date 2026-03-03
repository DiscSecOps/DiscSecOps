// frontend/src/services/search.service.js
import api from './api';

// Service for handling search-related API calls
export const searchService = {
  search: async (query, skip, limit) => {
    try {
      // 1. Get all users and filter locally )
      const usersResponse = await api.get('/users', {params: {skip, limit} });
      const allUsers = usersResponse.data || [];
      
      // 2. Filter by username (case insensitive)
      const filteredUsers = allUsers.filter(user => 
        user.username.toLowerCase().includes(query.toLowerCase())
      );

      // 3. Get all circles and filter locally )
      const circlesResponse = await api.get('/circles', {params: {skip, limit} });
      const allCircles = circlesResponse.data || [];
      
      // 4. Filter by name (case insensitive)
      const filteredCircles = allCircles.filter(circle => 
        circle.name.toLowerCase().includes(query.toLowerCase())
      );

      // 5. Get all posts and filter locally )
      const postsResponse = await api.get('/posts', {params: {skip, limit} });
      const allPosts = postsResponse.data || [];
      
      // 6. Filter by title (case insensitive)
      const filteredPosts = allPosts.filter(post => 
        post.title.toLowerCase().includes(query.toLowerCase())
      );

      return {
        users: filteredUsers,
        circles: filteredCircles,
        posts: filteredPosts
      };
    } catch (error) {
      console.error('Search error:', error);
      return { users: [], circles: [], posts: [] };
    }
  }
};