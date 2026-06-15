<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  label: {
    type: String,
    required: false
  },
  placeholder: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  icon: {
    type: String,
    default: ''
  },
  error: {
    type: String,
    default: ''
  }
})

defineEmits(['update:modelValue'])
</script>

<template>
  <div class="base-input-wrapper">
    <label v-if="label" class="input-label">{{ label }}</label>
    <div class="input-container" :class="{ 'has-error': error }">
      <input 
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
        class="base-input"
      />
      <span v-if="icon" class="material-symbols-outlined input-icon">{{ icon }}</span>
    </div>
    <span v-if="error" class="error-message">{{ error }}</span>
  </div>
</template>

<style scoped>
.base-input-wrapper {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  width: 100%;
}

.input-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-gray);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.base-input {
  width: 100%;
  padding: 0.85rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  font-family: var(--font-sans);
  font-size: 0.95rem;
  color: var(--text-primary);
  background-color: var(--color-white);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.base-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(184, 183, 255, 0.2);
}

.input-icon {
  position: absolute;
  right: 1rem;
  color: var(--text-gray);
  pointer-events: none;
}

.has-error .base-input {
  border-color: var(--status-expired);
}

.error-message {
  font-size: 0.8rem;
  color: var(--status-expired);
  margin-top: 2px;
}
</style>
