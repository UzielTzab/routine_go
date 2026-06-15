import { apiClient } from './client'

export const analyticsApi = {
  getDashboard: () => apiClient.get('/analytics/dashboard/'),
  getReports: () => apiClient.get('/analytics/reports/')
}
