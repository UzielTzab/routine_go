import axios from 'axios';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Si obtenemos 401 Unauthorized y no es la ruta de refrescar token ni un intento previo repetido
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      if (originalRequest.url === '/auth/token/refresh/') {
        // Falló al refrescar el token, la sesión expiró completamente
        localStorage.removeItem('isAuthenticated');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(error);
      }
      
      originalRequest._retry = true;
      try {
        // Intentar refrescar el token
        await apiClient.post('/auth/token/refresh/');
        
        // Si el refresco es exitoso, las cookies se actualizan solas. 
        // Reintentamos la petición original.
        return apiClient(originalRequest);
      } catch (refreshError) {
        // Si no se puede refrescar, mandamos al login
        localStorage.removeItem('isAuthenticated');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    // Fallos que no son 401 (o 401 después de intentar refrescar)
    if (error.response && (error.response.status === 401 || error.response.status === 403) && originalRequest.url !== '/auth/token/refresh/') {
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
