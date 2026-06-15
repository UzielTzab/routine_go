<script setup lang="ts">
import { defineProps, defineEmits, computed } from 'vue'
import { useAuthStore } from '../../../features/auth/stores/useAuthStore'

const authStore = useAuthStore()

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close-drawer'])

const handleLogout = () => {
  emit('close-drawer')
  authStore.logout()
}

const userInitial = computed(() => {
  return authStore.user?.name?.charAt(0).toUpperCase() || 'U'
})
</script>

<template>
  <div class="drawer-container" :class="{ 'is-open': isOpen }">
    <!-- Overlay/Backdrop -->
    <div class="drawer-backdrop" @click="emit('close-drawer')"></div>
    
    <!-- Sidebar Content -->
    <aside class="drawer-panel">
      <div class="drawer-header">
        <button class="icon-btn close-btn" @click="emit('close-drawer')">
          <span class="material-symbols-outlined">close</span>
        </button>
      </div>

      <div class="user-profile">
        <div class="avatar-fallback">
          <span class="avatar-initial">{{ userInitial }}</span>
        </div>
        <div class="user-info">
          <h4 class="user-name">{{ authStore.user?.name || 'Usuario' }}</h4>
          <span class="user-role">{{ authStore.user?.email || 'High Performance' }}</span>
        </div>
      </div>

      <nav class="sidebar-nav" @click="emit('close-drawer')">
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
        <button class="btn-start-routine" @click="emit('close-drawer')">
          <span class="material-symbols-outlined">play_arrow</span> Start Routine
        </button>
        <button class="btn-logout" @click="handleLogout">
          <span class="material-symbols-outlined">logout</span> Cerrar Sesión
        </button>
      </div>
    </aside>
  </div>
</template>

<style scoped>
.drawer-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 200;
  pointer-events: none; /* Let clicks pass through when closed */
}

.drawer-container.is-open {
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
  left: -280px;
  width: 280px;
  height: 100%;
  background-color: var(--sidebar-bg);
  color: var(--color-white);
  display: flex;
  flex-direction: column;
  padding: var(--space-4);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 2px 0 12px rgba(0,0,0,0.15);
}

.is-open .drawer-panel {
  transform: translateX(280px);
}

.drawer-header {
  display: flex;
  justify-content: flex-end;
  margin-bottom: var(--space-4);
}

.icon-btn {
  background: none;
  border: none;
  color: var(--color-white);
  cursor: pointer;
  opacity: 0.7;
}

.icon-btn:hover {
  opacity: 1;
}

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
  border-radius: var(--radius-lg);
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

.btn-start-routine {
  width: 100%;
  padding: 1rem;
  background-color: var(--color-primary);
  color: var(--sidebar-bg);
  border: none;
  border-radius: var(--radius-lg);
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--space-2);
}

.btn-start-routine .material-symbols-outlined {
  font-size: 1.25rem;
}

.btn-logout {
  width: 100%;
  padding: 1rem;
  background-color: transparent;
  color: var(--status-expired, #EF4444);
  border: 1px solid var(--status-expired, #EF4444);
  border-radius: var(--radius-lg);
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--space-2);
  margin-top: var(--space-3);
  transition: background-color 0.2s;
}

.btn-logout:hover {
  background-color: rgba(239, 68, 68, 0.1);
}

.avatar-initial {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--sidebar-bg);
}

@media (min-width: 769px) {
  .drawer-container {
    display: none;
  }
}
</style>
