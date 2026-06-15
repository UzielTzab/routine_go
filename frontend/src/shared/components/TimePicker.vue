<script setup lang="ts">
import { defineProps, defineEmits, ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

// We maintain a local ref mapped from the prop to the input, 
// ensuring we can handle 24hr format natively.
const localValue = ref(props.modelValue)

// Watch for external changes
watch(() => props.modelValue, (newVal) => {
  // If external value is "08:00 AM", we need to convert it to "08:00" for the input type="time"
  let parsed = newVal
  if (newVal && newVal.includes(' ')) {
    const [time, modifier] = newVal.split(' ')
    let [hours, minutes] = time.split(':')
    if (modifier === 'PM' && hours !== '12') hours = String(parseInt(hours) + 12)
    if (modifier === 'AM' && hours === '12') hours = '00'
    parsed = `${hours.padStart(2, '0')}:${minutes}`
  }
  localValue.value = parsed
}, { immediate: true })

const handleInput = (e: Event) => {
  const target = e.target as HTMLInputElement
  localValue.value = target.value
  
  // Format for the parent component (e.g. "08:00 AM") so we don't break existing payload
  let [hours, minutes] = target.value.split(':')
  if (!hours) return
  let hr = parseInt(hours)
  const modifier = hr >= 12 ? 'PM' : 'AM'
  if (hr === 0) hr = 12
  if (hr > 12) hr -= 12
  const formattedStr = `${String(hr).padStart(2, '0')}:${minutes} ${modifier}`
  
  emit('update:modelValue', formattedStr)
}
</script>

<template>
  <div class="time-picker-wrapper">
    <label v-if="label" class="time-label">{{ label }}</label>
    <div class="input-container">
      <span class="material-symbols-outlined input-icon">schedule</span>
      <input 
        type="time" 
        :value="localValue" 
        @input="handleInput"
        class="time-input" 
        required 
      />
    </div>
  </div>
</template>

<style scoped>
.time-picker-wrapper {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  width: 100%;
}

.time-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-gray);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.input-container {
  display: flex;
  align-items: center;
  background-color: #F8F9FD;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 0 var(--space-4);
  height: 48px;
  transition: all 0.2s;
  position: relative;
}

.input-container:focus-within {
  border-color: var(--color-primary);
  background-color: var(--color-white);
  box-shadow: 0 0 0 4px rgba(100, 98, 236, 0.1);
}

.input-icon {
  color: var(--text-gray);
  margin-right: var(--space-2);
  font-size: 1.25rem;
}

.time-input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 0.95rem;
  color: var(--text-primary);
  font-family: inherit;
  outline: none;
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
  width: 100%;
  padding-right: 10px; /* Space for the native clock icon if browser shows one */
}

/* Hide webkit clear button to keep it clean */
.time-input::-webkit-clear-button {
  display: none;
}

/* En desktop podemos dejar el reloj de webkit nativo porque el usuario puede hacerle click,
   pero le damos el mismo color que nuestro icono. */
.time-input::-webkit-calendar-picker-indicator {
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.time-input::-webkit-calendar-picker-indicator:hover {
  opacity: 1;
}
</style>
