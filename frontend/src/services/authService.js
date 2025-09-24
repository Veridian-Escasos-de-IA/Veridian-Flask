import apiClient from './apiClient';
import { API_ENDPOINTS, APP_CONFIG } from '../utils/constants';

class AuthService {
  /**
   * Registrar nueva persona
   */
  async register(userData) {
    try {
      const response = await apiClient.post(API_ENDPOINTS.REGISTER, userData);
      
      if (response.data.success) {
        const { access_token, refresh_token, persona } = response.data.data;
        
        // Guardar tokens y datos del usuario
        localStorage.setItem(APP_CONFIG.TOKEN_KEY, access_token);
        localStorage.setItem(APP_CONFIG.REFRESH_TOKEN_KEY, refresh_token);
        localStorage.setItem(APP_CONFIG.USER_KEY, JSON.stringify(persona));
        
        return { success: true, data: response.data.data };
      }
      
      return { success: false, message: response.data.message };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.message || 'Error al registrar usuario',
        errors: error.response?.data?.errors
      };
    }
  }

  /**
   * Iniciar sesión
   */
  async login(credentials) {
    try {
      const response = await apiClient.post(API_ENDPOINTS.LOGIN, credentials);
      
      if (response.data.success) {
        const { access_token, refresh_token, persona } = response.data.data;
        
        // Guardar tokens y datos del usuario
        localStorage.setItem(APP_CONFIG.TOKEN_KEY, access_token);
        localStorage.setItem(APP_CONFIG.REFRESH_TOKEN_KEY, refresh_token);
        localStorage.setItem(APP_CONFIG.USER_KEY, JSON.stringify(persona));
        
        return { success: true, data: response.data.data };
      }
      
      return { success: false, message: response.data.message };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.message || 'Error al iniciar sesión',
        errors: error.response?.data?.errors
      };
    }
  }

  /**
   * Cerrar sesión
   */
  async logout() {
    try {
      await apiClient.post(API_ENDPOINTS.LOGOUT);
    } catch (error) {
      console.warn('Error al cerrar sesión en el servidor:', error);
    } finally {
      // Limpiar storage local independientemente del resultado del servidor
      localStorage.removeItem(APP_CONFIG.TOKEN_KEY);
      localStorage.removeItem(APP_CONFIG.REFRESH_TOKEN_KEY);
      localStorage.removeItem(APP_CONFIG.USER_KEY);
    }
  }

  /**
   * Obtener perfil del usuario actual
   */
  async getProfile() {
    try {
      const response = await apiClient.get(API_ENDPOINTS.PROFILE);
      
      if (response.data.success) {
        // Actualizar datos del usuario en localStorage
        localStorage.setItem(APP_CONFIG.USER_KEY, JSON.stringify(response.data.data.persona));
        return { success: true, data: response.data.data.persona };
      }
      
      return { success: false, message: response.data.message };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.message || 'Error al obtener perfil'
      };
    }
  }

  /**
   * Verificar si el usuario está autenticado
   */
  isAuthenticated() {
    const token = localStorage.getItem(APP_CONFIG.TOKEN_KEY);
    return !!token;
  }

  /**
   * Obtener datos del usuario desde localStorage
   */
  getCurrentUser() {
    const userStr = localStorage.getItem(APP_CONFIG.USER_KEY);
    if (userStr) {
      try {
        return JSON.parse(userStr);
      } catch (error) {
        console.error('Error al parsear datos del usuario:', error);
        return null;
      }
    }
    return null;
  }

  /**
   * Obtener token de acceso
   */
  getAccessToken() {
    return localStorage.getItem(APP_CONFIG.TOKEN_KEY);
  }

  /**
   * Verificar si el usuario tiene un rol específico
   */
  hasRole(role) {
    const user = this.getCurrentUser();
    return user?.role === role;
  }

  /**
   * Verificar si el usuario es administrador
   */
  isAdmin() {
    return this.hasRole('admin');
  }

  /**
   * Login con Google OAuth
   */
  async loginWithGoogle(googleToken) {
    try {
      const response = await apiClient.post('/api/auth/google/user', {
        id_token: googleToken
      });
      
      if (response.data.success) {
        const { access_token, refresh_token, user } = response.data.data;
        
        // Guardar tokens y datos del usuario
        localStorage.setItem(APP_CONFIG.TOKEN_KEY, access_token);
        localStorage.setItem(APP_CONFIG.REFRESH_TOKEN_KEY, refresh_token);
        localStorage.setItem(APP_CONFIG.USER_KEY, JSON.stringify(user));
        
        return { success: true, data: response.data.data };
      }
      
      return { success: false, message: response.data.message };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.message || 'Error al iniciar sesión con Google',
        errors: error.response?.data?.errors
      };
    }
  }

  /**
   * Obtener URL de login con Google (redirect)
   */
  getGoogleLoginUrl() {
    const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000';
    return `${API_BASE}/api/auth/google/login`;
  }
}

// Exportar instancia singleton
const authService = new AuthService();
export default authService;
