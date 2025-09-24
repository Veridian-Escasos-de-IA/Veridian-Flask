import React, { createContext, useContext, useState, useEffect } from 'react';
import Cookies from 'js-cookie';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de un AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  // Verificar si hay un token guardado al cargar la aplicación
  useEffect(() => {
    const token = Cookies.get('token');
    if (token) {
      // Verificar el token con el backend
      verifyToken(token);
    } else {
      setLoading(false);
    }
  }, []);

  const verifyToken = async (token) => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/verify`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setUser(data.data.user);
        setIsAuthenticated(true);
      } else {
        // Token inválido, limpiar cookies
        Cookies.remove('token');
        setUser(null);
        setIsAuthenticated(false);
      }
    } catch (error) {
      console.error('Error verificando token:', error);
      Cookies.remove('token');
      setUser(null);
      setIsAuthenticated(false);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ correo: email, password }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        // Guardar token en cookies
        Cookies.set('token', data.data.access_token, { expires: 7 });
        setUser(data.data.user || data.data.persona);
        setIsAuthenticated(true);
        return { success: true, user: data.data.user || data.data.persona };
      } else {
        return { success: false, message: data.message || 'Error al iniciar sesión' };
      }
    } catch (error) {
      console.error('Error en login:', error);
      return { success: false, message: 'Error de conexión' };
    }
  };

  const register = async (userData) => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        // Guardar token en cookies
        Cookies.set('token', data.data.access_token, { expires: 7 });
        setUser(data.data.user || data.data.persona);
        setIsAuthenticated(true);
        return { success: true, user: data.data.user || data.data.persona };
      } else {
        return { success: false, message: data.message || 'Error al registrarse' };
      }
    } catch (error) {
      console.error('Error en registro:', error);
      return { success: false, message: 'Error de conexión' };
    }
  };

  const loginWithGoogle = async (credential) => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/google/user`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id_token: credential }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        // Guardar token en cookies
        Cookies.set('token', data.data.access_token, { expires: 7 });
        setUser(data.data.user);
        setIsAuthenticated(true);
        return { success: true, user: data.data.user };
      } else {
        return { success: false, message: data.message || 'Error al iniciar sesión con Google' };
      }
    } catch (error) {
      console.error('Error en login con Google:', error);
      return { success: false, message: 'Error de conexión' };
    }
  };

  const logout = () => {
    Cookies.remove('token');
    setUser(null);
    setIsAuthenticated(false);
  };

  // Funciones de utilidad para roles
  const hasRole = (role) => {
    return user?.role === role;
  };

  const isAdmin = () => {
    return hasRole('admin');
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    login,
    register,
    loginWithGoogle,
    logout,
    hasRole,
    isAdmin,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;