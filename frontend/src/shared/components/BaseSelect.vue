<script setup lang="ts">


defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  label: {
    type: String,
    required: false
  },
  options: {
    type: Array as () => Array<{ value: string | number, label: string }>,
    required: true
  }
})

defineEmits(['update:modelValue'])
</script>

<template>
  <div class="base-select-wrapper">
    <label v-if="label" class="select-label">{{ label }}</label>
    <div class="select-container">
      <select 
        :value="modelValue"
        @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
        class="base-select"
      >
        <option v-for="option in options" :key="option.value" :value="option.value">
          {{ option.label }}
        </option>
      </select>
      <span class="material-symbols-outlined select-icon">expand_more</span>
    </div>
  </div>
</template>

<style scoped>
.base-select-wrapper {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  width: 100%;
}

.select-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-gray);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.select-container {
  position: relative;
  display: flex;
  align-items: center;
}

.base-select {
  width: 100%;
  padding: 0.85rem 2.5rem 0.85rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  font-family: var(--font-sans);
  font-size: 0.95rem;
  color: var(--text-primary);
  background-color: var(--color-white);
  appearance: none;
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.base-select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(184, 183, 255, 0.2);
}

.select-icon {
  position: absolute;
  right: 1rem;
  color: var(--text-gray);
  pointer-events: none;
}
</style>
