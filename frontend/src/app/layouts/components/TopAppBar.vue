<script setup lang="ts">
import { defineEmits, computed } from 'vue'
import { useAuthStore } from '../../../features/auth/stores/useAuthStore'

const authStore = useAuthStore()

const emit = defineEmits(['toggle-drawer'])

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
      <button class="icon-btn">
        <span class="material-symbols-outlined">notifications</span>
      </button>
      <button class="icon-btn avatar-btn">
        <span class="avatar-initial-small">{{ userInitial }}</span>
      </button>
    </div>
  </header>
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
</style>
