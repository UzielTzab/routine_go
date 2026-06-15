import { apiClient } from './client'

export const authApi = {
  login: (data: { email: string; password: string }) => apiClient.post('/auth/token/', { username: data.email, password: data.password }),
  register: (data: any) => apiClient.post('/auth/register/', data),
  logout: () => apiClient.post('/auth/logout/')
}
