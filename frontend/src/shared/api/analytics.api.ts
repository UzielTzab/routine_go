import { apiClient } from './client'

export const analyticsApi = {
  getReports: () => apiClient.get('/analytics/reports/')
}
