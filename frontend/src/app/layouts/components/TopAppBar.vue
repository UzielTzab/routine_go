<script setup lang="ts">
import { computed, ref } from 'vue'
import { useAuthStore } from '../../../features/auth/stores/useAuthStore'
import { useNotificationStore } from '../../../features/notifications/stores/useNotificationStore'
import NotificationPanel from '../../../features/notifications/components/NotificationPanel.vue'

const authStore = useAuthStore()
const notificationStore = useNotificationStore()

const emit = defineEmits(['toggle-drawer'])

const isNotificationsOpen = ref(false)

const userInitial = computed(() => {
  return authStore.user?.name?.charAt(0).toUpperCase() || 'U'
})
</script>

<template>
  <header class="top-app-bar">
    <button class="icon-btn menu-btn" @click="emit('toggle-drawer')">
      <span class="material-symbols-outlined">menu</span>
    </button>
    
    <div class="logo-container">
      <!-- Logo removido por petición del usuario -->
    </div>
    
    <div class="actions-right">
      <div class="notification-wrapper">
        <button class="icon-btn" @click="isNotificationsOpen = true">
          <span class="material-symbols-outlined">notifications</span>
          <span v-if="notificationStore.unreadCount > 0" class="badge">{{ notificationStore.unreadCount }}</span>
        </button>
      </div>
      <button class="icon-btn avatar-btn">
        <span class="avatar-initial-small">{{ userInitial }}</span>
      </button>
    </div>
  </header>

  <NotificationPanel :isOpen="isNotificationsOpen" @close="isNotificationsOpen = false" />
</template>

<style scoped>
.top-app-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  background-color: var(--bg-app);
  padding: 0 var(--space-4);
  position: sticky;
  top: 0;
  z-index: 90;
}

.logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
}

.brand-logo {
  height: 32px;
  object-fit: contain;
}

.actions-right {
  display: flex;
  gap: var(--space-2);
}

.icon-btn {
  background: none;
  border: none;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: var(--space-1);
}

.icon-btn .material-symbols-outlined {
  font-size: 1.5rem;
}

.icon-btn:hover {
  opacity: 1;
}

.avatar-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  margin-left: var(--space-2);
}

.avatar-initial-small {
  color: var(--color-white);
  font-weight: 700;
  font-size: 0.9rem;
}

@media (min-width: 769px) {
  .top-app-bar {
    display: none;
  }
}

.notification-wrapper {
  position: relative;
}

.badge {
  position: absolute;
  top: 4px;
  right: 4px;
  background-color: var(--status-expired, #EF4444);
  color: white;
  border-radius: 50%;
  padding: 2px 6px;
  font-size: 0.65rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
