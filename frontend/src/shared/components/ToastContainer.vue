<script setup lang="ts">
import { useToast } from '../composables/useToast'

const { toasts, removeToast } = useToast()

const getIcon = (type: string) => {
  switch (type) {
    case 'success': return 'check_circle'
    case 'error': return 'error'
    default: return 'info'
  }
}
</script>

<template>
  <div class="toast-container">
    <TransitionGroup name="toast">
      <div 
        v-for="toast in toasts" 
        :key="toast.id" 
        class="toast"
        :class="`toast-${toast.type}`"
        @click="removeToast(toast.id)"
      >
        <span class="material-symbols-outlined">{{ getIcon(toast.type) }}</span>
        <span class="toast-message">{{ toast.message }}</span>
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-container {
  position: fixed;
  bottom: var(--space-6);
  right: var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  z-index: var(--z-toast);
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 1rem 1.5rem;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
  color: var(--color-white);
  pointer-events: auto;
  cursor: pointer;
  min-width: 300px;
}

.toast-message {
  font-weight: 600;
  font-size: 0.95rem;
}

.toast-success { background-color: var(--color-exercise); }
.toast-error { background-color: var(--status-expired); }
.toast-info { background-color: var(--color-primary); }

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.toast-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
</style>
