// frontend/src/services/post.service.js
import api from './api';

const BASE_URL = '/posts';

export const postService = {
  // Get feed (recent posts from user's circles)
  getFeed: async (limit = 20, offset = 0) => {
    try {
      const response = await api.get(`${BASE_URL}/feed?limit=${limit}&offset=${offset}`, {
        withCredentials: true
      });
      return response.data; // Array of posts
    } catch (error) {
      console.error('Error fetching feed:', error);
      throw error;
    }
  },

  // Create post
  createPost: async (postData) => {
    try {
      const response = await api.post(BASE_URL, postData, {
        withCredentials: true
      });
      return response.data;
    } catch (error) {
      console.error('Error creating post:', error);
      throw error;
    }
  }
};