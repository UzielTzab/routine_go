<script setup lang="ts">


defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  label: {
    type: String,
    required: true
  }
})

defineEmits(['update:modelValue'])
</script>

<template>
  <label class="base-switch-wrapper">
    <span class="switch-label">{{ label }}</span>
    <div class="switch-container">
      <input 
        type="checkbox"
        :checked="modelValue"
        @change="$emit('update:modelValue', ($event.target as HTMLInputElement).checked)"
        class="switch-input"
      />
      <div class="switch-track">
        <div class="switch-thumb"></div>
      </div>
    </div>
  </label>
</template>

<style scoped>
.base-switch-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  width: 100%;
}

.switch-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
}

.switch-container {
  position: relative;
  display: flex;
  align-items: center;
}

.switch-input {
  opacity: 0;
  position: absolute;
  width: 0;
  height: 0;
}

.switch-track {
  width: 44px;
  height: 24px;
  background-color: var(--color-disable);
  border-radius: 12px;
  position: relative;
  transition: background-color 0.2s;
}

.switch-thumb {
  width: 20px;
  height: 20px;
  background-color: var(--color-white);
  border-radius: 50%;
  position: absolute;
  top: 2px;
  left: 2px;
  transition: transform 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.switch-input:checked + .switch-track {
  background-color: var(--color-primary);
}

.switch-input:checked + .switch-track .switch-thumb {
  transform: translateX(20px);
}
</style>
