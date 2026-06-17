/// <reference lib="WebWorker" />
import { precacheAndRoute, cleanupOutdatedCaches } from 'workbox-precaching'

declare let self: ServiceWorkerGlobalScope

cleanupOutdatedCaches()

// Precache resources
precacheAndRoute(self.__WB_MANIFEST || [])

// Listen to Push events
self.addEventListener('push', (event) => {
  let payload: any = { title: 'RoutineGo', body: 'Nueva notificación' }
  
  if (event.data) {
    try {
      payload = event.data.json()
    } catch (e) {
      payload.body = event.data.text()
    }
  }

  const title = payload.title || 'RoutineGo'
  const options = {
    body: payload.body,
    icon: '/images/routine_go_logo.png',
    badge: '/images/routine_go_logo.png',
    data: payload.data || {},
    actions: payload.actions || []
  }

  // Notify any open clients that a new notification arrived
  self.clients.matchAll().then(clients => {
    clients.forEach(client => client.postMessage({ type: 'NEW_NOTIFICATION' }))
  })

  event.waitUntil(self.registration.showNotification(title, options))
})

// Listen to Notification clicks
self.addEventListener('notificationclick', (event) => {
  event.notification.close()

  const action = event.action
  const urlToOpen = new URL('/', self.location.origin)
  
  if (action) {
    urlToOpen.searchParams.set('action', action)
  }
  
  if (event.notification.data && event.notification.data.url) {
      urlToOpen.pathname = event.notification.data.url
  }

  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then((windowClients) => {
      for (let i = 0; i < windowClients.length; i++) {
        const client = windowClients[i]
        if (client.url === urlToOpen.href && 'focus' in client) {
          return client.focus()
        }
      }
      if (self.clients.openWindow) {
        return self.clients.openWindow(urlToOpen.href)
      }
    })
  )
})
