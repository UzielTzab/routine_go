<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { RouterView } from 'vue-router'
import TopAppBar from './components/TopAppBar.vue'
import BottomNavigation from './components/BottomNavigation.vue'
import MobileDrawer from './components/MobileDrawer.vue'
import { useAuthStore } from '../../features/auth/stores/useAuthStore'
import { useNotificationStore } from '../../features/notifications/stores/useNotificationStore'

const authStore = useAuthStore()
const notificationStore = useNotificationStore()

onMounted(() => {
  // Fetch initial notifications
  notificationStore.fetchNotifications()
  
  // Listen for messages from the service worker
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.addEventListener('message', (event) => {
      if (event.data && event.data.type === 'NEW_NOTIFICATION') {
        notificationStore.fetchNotifications()
      }
    })
  }
})

const isDrawerOpen = ref(false)

const toggleDrawer = () => {
  isDrawerOpen.value = !isDrawerOpen.value
}

const userInitial = computed(() => {
  return authStore.user?.name?.charAt(0).toUpperCase() || 'U'
})
</script>

<template>
  <div class="dashboard-layout">
    <!-- Mobile Navigation Components -->
    <TopAppBar @toggle-drawer="toggleDrawer" />
    <MobileDrawer :is-open="isDrawerOpen" @close-drawer="isDrawerOpen = false" />

    <!-- Desktop Sidebar -->
    <aside class="sidebar desktop-only">
      <div class="user-profile">
        <div class="avatar-fallback">
          <span class="avatar-initial">{{ userInitial }}</span>
        </div>
        <div class="user-info">
          <h4 class="user-name">{{ authStore.user?.name || 'Usuario' }}</h4>
          <span class="user-role">{{ authStore.user?.email || 'High Performance' }}</span>
        </div>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/" class="nav-item" exact-active-class="active">
          <span class="material-symbols-outlined nav-icon">grid_view</span>
          <span>Dashboard</span>
        </router-link>
        <router-link to="/agenda" class="nav-item" exact-active-class="active">
          <span class="material-symbols-outlined nav-icon">calendar_today</span>
          <span>Agenda</span>
        </router-link>
        <router-link to="/active-routine" class="nav-item" exact-active-class="active">
          <span class="material-symbols-outlined nav-icon">play_circle</span>
          <span>Active Routine</span>
        </router-link>
        <router-link to="/create-routine" class="nav-item" exact-active-class="active">
          <span class="material-symbols-outlined nav-icon">add_circle</span>
          <span>Create Routine</span>
        </router-link>
        <router-link to="/reports" class="nav-item" exact-active-class="active">
          <span class="material-symbols-outlined nav-icon">bar_chart</span>
          <span>Reports</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
      </div>
    </aside>

    <main class="main-content">
      <header class="topbar desktop-only">
        <div class="topbar-right">
          <button class="icon-btn">
            <span class="material-symbols-outlined">notifications</span>
          </button>
          <button class="icon-btn">
            <span class="material-symbols-outlined">settings</span>
          </button>
        </div>
      </header>

      <div class="content-wrapper">
        <RouterView />
      </div>
    </main>

    <!-- Mobile Bottom Navigation -->
    <BottomNavigation />
  </div>
</template>

<style scoped>
.dashboard-layout {
  display: flex;
  flex-direction: column; /* Mobile first: stack TopBar and Main Content vertically */
  height: 100dvh;
  width: 100vw;
  overflow: hidden;
  background-color: var(--bg-app);
}

.desktop-only {
  display: none;
}

.main-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.content-wrapper {
  flex-grow: 1;
  overflow-y: auto;
  padding: var(--space-4);
  padding-bottom: 90px; /* Space for bottom navigation */
}

@media (min-width: 769px) {
  .dashboard-layout {
    flex-direction: row;
  }
  
  .desktop-only {
    display: flex;
  }

  .sidebar.desktop-only {
    width: var(--sidebar-width);
    background-color: var(--sidebar-bg);
    color: var(--color-white);
    flex-direction: column;
    padding: var(--space-6) var(--space-4);
  }

  .topbar.desktop-only {
    height: var(--topbar-height);
    align-items: center;
    justify-content: flex-end;
    padding: 0 var(--space-8);
  }

  .content-wrapper {
    padding: 0 var(--space-8) var(--space-8);
    padding-bottom: var(--space-8); /* Reset padding since bottom nav is hidden */
  }
}

/* Original Sidebar Styles applied to desktop-only sidebar */
.user-profile {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-8);
  padding: 0 var(--space-2);
}

.avatar-fallback {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-icon {
  font-size: 1.5rem;
  color: var(--sidebar-bg);
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 600;
  font-size: 1rem;
  margin: 0;
}

.user-role {
  font-size: 0.75rem;
  color: var(--color-primary);
  opacity: 0.8;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  flex-grow: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  color: var(--color-white);
  text-decoration: none;
  border-radius: var(--radius-md);
  font-size: 0.95rem;
  opacity: 0.7;
  transition: all 0.2s;
}

.nav-item:hover, .nav-item.active {
  opacity: 1;
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-item.active {
  background-color: var(--color-primary-deep);
  font-weight: 600;
}

.nav-icon {
  font-size: 1.25rem;
}

.sidebar-footer {
  margin-top: auto;
}

.topbar-right {
  display: flex;
  gap: var(--space-4);
}

.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-primary);
  opacity: 0.7;
  transition: opacity 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-btn:hover {
  opacity: 1;
}
</style>
