import { defineStore } from 'pinia'
import { ref } from 'vue'
import { notificationsApi } from '../../../shared/api/notifications.api'

function urlBase64ToUint8Array(base64String: string) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4)
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/')

  const rawData = window.atob(base64)
  const outputArray = new Uint8Array(rawData.length)

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i)
  }
  return outputArray
}

export const useNotificationStore = defineStore('notification', () => {
  const isSupported = ref('serviceWorker' in navigator && 'PushManager' in window)
  const permissionGranted = ref(Notification.permission === 'granted')
  const notifications = ref<any[]>([])
  const loading = ref(false)
  const unreadCount = ref(0)

  const requestPermission = async () => {
    if (!isSupported.value) return false
    
    try {
      const permission = await Notification.requestPermission()
      permissionGranted.value = permission === 'granted'
      
      if (permissionGranted.value) {
        await subscribeToPush()
      }
      return permissionGranted.value
    } catch (e) {
      console.error('Error requesting notification permission:', e)
      return false
    }
  }

  const subscribeToPush = async () => {
    try {
      const registration = await navigator.serviceWorker.ready
      let subscription = await registration.pushManager.getSubscription()
      
      if (!subscription) {
        const vapidPublicKey = import.meta.env.VITE_VAPID_PUBLIC_KEY
        if (!vapidPublicKey) {
          console.error('VITE_VAPID_PUBLIC_KEY no encontrada en entorno.')
          return
        }
        const convertedVapidKey = urlBase64ToUint8Array(vapidPublicKey)
        subscription = await registration.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey: convertedVapidKey
        })
      }
      
      // Parse subscription to extract keys
      const subJson = subscription.toJSON()
      const payload = {
        endpoint: subJson.endpoint,
        p256dh: subJson.keys?.p256dh,
        auth: subJson.keys?.auth
      }
      
      // Enviar suscripción al backend
      await notificationsApi.subscribe(payload as any)
      console.log('Suscripción Web Push enviada al backend exitosamente.')
    } catch (e) {
      console.error('Error al suscribirse al Web Push:', e)
    }
  }

  const fetchNotifications = async () => {
    loading.value = true
    try {
      const response = await notificationsApi.getNotifications()
      notifications.value = response.data
      unreadCount.value = notifications.value.filter(n => !n.is_read).length
    } catch (e) {
      console.error('Error al obtener notificaciones:', e)
    } finally {
      loading.value = false
    }
  }

  const markAsRead = async (id: string) => {
    try {
      await notificationsApi.markAsRead(id)
      const notif = notifications.value.find(n => n.id === id)
      if (notif && !notif.is_read) {
        notif.is_read = true
        unreadCount.value = Math.max(0, unreadCount.value - 1)
      }
    } catch (e) {
      console.error('Error al marcar notificación como leída:', e)
    }
  }

  return {
    isSupported,
    permissionGranted,
    notifications,
    unreadCount,
    loading,
    requestPermission,
    subscribeToPush,
    fetchNotifications,
    markAsRead
  }
})
