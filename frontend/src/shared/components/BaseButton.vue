<script setup lang="ts">
defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value: string) => ['primary', 'secondary', 'outline', 'ghost'].includes(value)
  },
  block: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  }
})
</script>

<template>
  <button 
    class="base-button" 
    :class="[`variant-${variant}`, { 'is-block': block, 'is-disabled': disabled }]"
    :disabled="disabled"
    @click="$emit('click')"
  >
    <slot name="icon"></slot>
    <slot></slot>
  </button>
</template>

<style scoped>
.base-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius-lg);
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  font-family: var(--font-sans);
}

.is-block {
  width: 100%;
}

.is-disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: var(--color-disable) !important;
  color: var(--text-gray) !important;
}

/* Variants */
.variant-primary {
  background-color: var(--color-primary);
  color: var(--sidebar-bg); /* Dark color text for the purple primary according to design */
}

.variant-primary:hover:not(.is-disabled) {
  filter: brightness(0.95);
}

.variant-secondary {
  background-color: var(--bg-status-info);
  color: var(--status-in-progress);
}

.variant-outline {
  background-color: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-primary);
}

.variant-ghost {
  background-color: transparent;
  color: var(--text-secondary);
}

.variant-ghost:hover:not(.is-disabled) {
  background-color: var(--bg-app);
}
</style>
