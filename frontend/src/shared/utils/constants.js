const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const API_ENDPOINTS = {
  // Autenticación
  REGISTER: `${API_BASE_URL}/api/auth/register`,
  LOGIN: `${API_BASE_URL}/api/auth/login`,
  REFRESH: `${API_BASE_URL}/api/auth/refresh`,
  LOGOUT: `${API_BASE_URL}/api/auth/logout`,
  PROFILE: `${API_BASE_URL}/api/auth/profile`,
};

export const APP_CONFIG = {
  APP_NAME: 'Edificio Multifuncional',
  TOKEN_KEY: 'edificio_token',
  REFRESH_TOKEN_KEY: 'edificio_refresh_token',
  USER_KEY: 'edificio_user',
};

export const ROLES = {
  ADMIN: 'admin',
  USER: 'user',
  EMPLOYEE: 'employee',
};
