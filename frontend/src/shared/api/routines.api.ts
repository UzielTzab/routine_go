import { apiClient } from './client'

export const routinesApi = {
  getCategories: () => apiClient.get('/routines/categories/'),
  getTemplates: () => apiClient.get('/routines/templates/'),
  createTemplate: (data: any) => apiClient.post('/routines/templates/', data),
  updateTemplate: (id: string, data: any) => apiClient.patch(`/routines/templates/${id}/`),
  deleteTemplate: (id: string) => apiClient.delete(`/routines/templates/${id}/`)
}
