/**
 * Axios client configuration with interceptors
 */
import axios, { AxiosError, type InternalAxiosRequestConfig } from 'axios';

const API_BASE_URL = '/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - can add auth token here if needed
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Add auth token if available
    // const token = localStorage.getItem('auth_token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error: AxiosError) => Promise.reject(error)
);

// Response interceptor - handle errors globally
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response) {
      // Server responded with error status
      const errorData = error.response.data as { error?: string; message?: string; details?: Record<string, string> };
      console.error(`API Error [${error.response.status}]:`, errorData.message || error.message);
    } else if (error.request) {
      // Network error
      console.error('Network Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default apiClient;