import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://app:8000';

const api = axios.create({
  baseURL: API_URL,
});

export const sendMessage = async (message) => {
  try {
    const response = await api.post('/chat', { message });
    return response.data;
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
};

export default api;