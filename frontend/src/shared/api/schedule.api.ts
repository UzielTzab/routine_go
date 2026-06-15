import { apiClient } from './client'

export const scheduleApi = {
  getToday: () => apiClient.get('/schedule/today/')
}
