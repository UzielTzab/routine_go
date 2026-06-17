<script setup lang="ts">
import { watch } from 'vue'
import { useNotificationStore } from '../stores/useNotificationStore'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

const notificationStore = useNotificationStore()

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    notificationStore.fetchNotifications()
  }
})
</script>

<template>
  <div class="notification-drawer-container" :class="{ 'is-open': isOpen }">
    <!-- Overlay -->
    <div class="drawer-backdrop" @click="emit('close')"></div>
    
    <!-- Drawer Panel -->
    <aside class="drawer-panel">
      <div class="drawer-header">
        <h3>Notificaciones</h3>
        <button class="icon-btn close-btn" @click="emit('close')">
          <span class="material-symbols-outlined">close</span>
        </button>
      </div>

      <div class="drawer-content">
        <div v-if="notificationStore.loading" class="empty-state">
          <p>Cargando...</p>
        </div>
        <div v-else-if="notificationStore.notifications.length === 0" class="empty-state">
          <span class="material-symbols-outlined empty-icon">notifications_off</span>
          <p>No tienes notificaciones nuevas</p>
        </div>
        <div v-else class="notification-list">
          <div 
            v-for="notif in notificationStore.notifications" 
            :key="notif.id"
            class="notification-item"
            :class="{ 'is-unread': !notif.is_read }"
            @click="notificationStore.markAsRead(notif.id)"
          >
            <div class="notif-content">
              <h4>{{ notif.title || 'RoutineGo' }}</h4>
              <p>{{ notif.message }}</p>
              <span class="notif-time">{{ new Date(notif.created_at).toLocaleTimeString() }}</span>
            </div>
            <div v-if="!notif.is_read" class="unread-dot"></div>
          </div>
        </div>
      </div>
    </aside>
  </div>
</template>

<style scoped>
.notification-drawer-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 300;
  pointer-events: none;
}

.notification-drawer-container.is-open {
  pointer-events: auto;
}

.drawer-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.is-open .drawer-backdrop {
  opacity: 1;
}

.drawer-panel {
  position: absolute;
  top: 0;
  right: -320px;
  width: 320px;
  height: 100%;
  background-color: var(--bg-app);
  color: var(--text-primary);
  display: flex;
  flex-direction: column;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: -2px 0 12px rgba(0,0,0,0.15);
}

.is-open .drawer-panel {
  transform: translateX(-320px);
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-4);
  border-bottom: 1px solid var(--border-color);
}

.drawer-header h3 {
  margin: 0;
  font-size: 1.2rem;
}

.icon-btn {
  background: none;
  border: none;
  color: var(--text-primary);
  cursor: pointer;
}

.drawer-content {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-4);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--text-gray);
  text-align: center;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: var(--space-2);
  opacity: 0.5;
}

.notification-item {
  display: flex;
  align-items: center;
  padding: var(--space-3);
  background-color: var(--color-white);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-3);
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  cursor: pointer;
  transition: background-color 0.2s;
}

.notification-item:hover {
  background-color: #f9fafb;
}

.notification-item.is-unread {
  border-left: 4px solid var(--color-primary);
}

.notif-content {
  flex: 1;
}

.notif-content h4 {
  margin: 0 0 4px 0;
  font-size: 0.95rem;
}

.notif-content p {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-gray);
}

.notif-time {
  font-size: 0.75rem;
  color: #9ca3af;
  margin-top: 4px;
  display: block;
}

.unread-dot {
  width: 8px;
  height: 8px;
  background-color: var(--color-primary);
  border-radius: 50%;
  margin-left: var(--space-2);
}
</style>
