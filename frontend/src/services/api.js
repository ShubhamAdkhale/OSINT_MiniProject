import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('token');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export const analysisService = {
  analyzePhone: async (phoneNumber, deepScan = false) => {
    const response = await api.post('/api/analyze', {
      phone_number: phoneNumber,
      deep_scan: deepScan,
    });
    return response.data;
  },

  getReport: async (analysisId) => {
    const response = await api.get(`/api/report/${analysisId}`);
    return response.data;
  },

  getHistory: async (page = 1, perPage = 10) => {
    const response = await api.get('/api/history', {
      params: { page, per_page: perPage },
    });
    return response.data;
  },

  searchAnalyses: async (phoneNumber, riskLevel) => {
    const response = await api.post('/api/search', {
      phone_number: phoneNumber,
      risk_level: riskLevel,
    });
    return response.data;
  },

  getStatistics: async () => {
    const response = await api.get('/api/statistics');
    return response.data;
  },

  deleteAnalysis: async (analysisId) => {
    const response = await api.delete(`/api/report/${analysisId}`);
    return response.data;
  },

  clearAllHistory: async () => {
    const response = await api.delete('/api/history/clear');
    return response.data;
  },
};

export const healthService = {
  checkHealth: async () => {
    const response = await api.get('/health');
    return response.data;
  },

  getApiStatus: async () => {
    const response = await api.get('/api/status');
    return response.data;
  },
};

export default api;
