<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

const close = () => {
  emit('update:modelValue', false)
}
</script>

<template>
  <Teleport defer to="body">
    <Transition name="modal">
      <div v-if="modelValue" class="modal-overlay" @click.self="close">
        <div class="modal-container">
          <header class="modal-header">
            <slot name="title">
              <h2 class="modal-title" v-if="title">{{ title }}</h2>
            </slot>
            <button class="modal-close-btn" @click="close">
              <span class="material-symbols-outlined">close</span>
            </button>
          </header>

          <main class="modal-content">
            <slot></slot>
          </main>

          <footer class="modal-footer" v-if="$slots.footer">
            <slot name="footer"></slot>
          </footer>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
}

.modal-container {
  background-color: var(--bg-card, #ffffff);
  color: var(--text-primary, #333333);
  width: 90%;
  max-width: 500px;
  border-radius: var(--radius-lg, 12px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-4, 1rem) var(--space-5, 1.25rem);
  border-bottom: 1px solid var(--border-color, #e2e8f0);
}

.modal-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.modal-close-btn {
  background: none;
  border: none;
  color: var(--text-gray, #64748b);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-1, 0.25rem);
  border-radius: var(--radius-sm, 4px);
  transition: background-color 0.2s, color 0.2s;
}

.modal-close-btn:hover {
  background-color: var(--bg-hover, #f1f5f9);
  color: var(--text-primary, #333333);
}

.modal-content {
  padding: var(--space-5, 1.25rem);
  font-size: 1rem;
  line-height: 1.5;
}

.modal-footer {
  padding: var(--space-4, 1rem) var(--space-5, 1.25rem);
  border-top: 1px solid var(--border-color, #e2e8f0);
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3, 0.75rem);
}

/* Animations */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.95);
}
</style>
