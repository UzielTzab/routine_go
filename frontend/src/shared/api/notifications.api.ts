import { apiClient as api } from './client'

export const notificationsApi = {
  subscribe: (subscription: PushSubscription) => {
    return api.post('/notifications/push-subscriptions/', subscription)
  },
  getNotifications: () => {
    return api.get('/notifications/')
  },
  markAsRead: (id: string) => {
    return api.post(`/notifications/${id}/read/`)
  }
}
