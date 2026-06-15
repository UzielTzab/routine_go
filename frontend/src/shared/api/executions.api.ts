import { apiClient } from './client'

export const executionsApi = {
  start: (uuid: string) => apiClient.post(`/executions/${uuid}/start/`),
  complete: (uuid: string) => apiClient.post(`/executions/${uuid}/complete/`),
  pause: (uuid: string) => apiClient.post(`/executions/${uuid}/pause/`),
  omit: (uuid: string) => apiClient.post(`/executions/${uuid}/omit/`),
  snooze: (uuid: string) => apiClient.post(`/executions/${uuid}/snooze/`, { minutes: 15 }),
}
