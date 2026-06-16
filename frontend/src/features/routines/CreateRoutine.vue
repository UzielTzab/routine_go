<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import BaseCard from '../../shared/components/BaseCard.vue'
import BaseInput from '../../shared/components/BaseInput.vue'
import BaseSelect from '../../shared/components/BaseSelect.vue'
import BaseSwitch from '../../shared/components/BaseSwitch.vue'
import BaseButton from '../../shared/components/BaseButton.vue'
import TimePicker from '../../shared/components/TimePicker.vue'
import { useRoutineStore } from './stores/useRoutineStore'

const routineStore = useRoutineStore()
const { categories, loadingCategories, errorCategories, loadingCreate, createSuccess, errorCreate } = storeToRefs(routineStore)

// Form State
const routineName = ref('')
const selectedCategoryId = ref<number | string | null>(null)
const startTime = ref('08:00 AM')
const endTime = ref('10:00 AM')
const selectedDays = ref(['J'])
const reminder = ref('5 minutos antes')
const autoComplete = ref(true)

const reminderOptions = [
  { value: '5 minutos antes', label: '5 minutos antes' },
  { value: '10 minutos antes', label: '10 minutos antes' },
  { value: '15 minutos antes', label: '15 minutos antes' },
]

const weekDays = [
  { id: 'L', label: 'L' },
  { id: 'M', label: 'M' },
  { id: 'X', label: 'X' },
  { id: 'J', label: 'J' },
  { id: 'V', label: 'V' },
  { id: 'S', label: 'S' },
  { id: 'D', label: 'D' }
]

// Local icon map based on category name
const getCategoryAppearance = (name: string) => {
  const lowerName = (name || '').toLowerCase()
  if (lowerName.includes('higiene') || lowerName.includes('hygiene')) return { icon: '/images/icons/hygiene.png', color: 'var(--color-hygiene)' }
  if (lowerName.includes('ejercicio') || lowerName.includes('exercise')) return { icon: '/images/icons/excersice.png', color: 'var(--color-exercise)' }
  if (lowerName.includes('foco') || lowerName.includes('focus') || lowerName.includes('trabajo')) return { icon: '/images/icons/focus.png', color: 'var(--color-focus)' }
  if (lowerName.includes('nutrición') || lowerName.includes('nutricion') || lowerName.includes('nutrition') || lowerName.includes('alimentación') || lowerName.includes('alimentacion')) return { icon: '/images/icons/nutrition.png', color: 'var(--color-nutrition)' }
  if (lowerName.includes('sueño') || lowerName.includes('sleep')) return { icon: '/images/icons/sleep.png', color: 'var(--color-sleep)' }
  
  return { icon: '/images/icons/focus.png', color: 'var(--color-primary)' }
}

const toggleDay = (dayId: string) => {
  if (selectedDays.value.includes(dayId)) {
    selectedDays.value = selectedDays.value.filter(d => d !== dayId)
  } else {
    selectedDays.value.push(dayId)
  }
}

const handleSave = async () => {
  if (!routineName.value || !selectedCategoryId.value) {
    alert('Por favor ingresa un nombre y selecciona una categoría.')
    return
  }
  
  // Helper to parse "08:00 AM" to "HH:MM"
  const parseTime = (timeStr: string) => {
    const [time, modifier] = timeStr.split(' ')
    if (!modifier) return time
    let [hours, minutes] = time.split(':')
    if (hours === '12') hours = '00'
    if (modifier === 'PM') hours = String(parseInt(hours, 10) + 12)
    if (hours.length === 1) hours = '0' + hours
    return `${hours}:${minutes}`
  }

  // Calculate duration in minutes
  const calculateDuration = () => {
    const startStr = parseTime(startTime.value)
    const endStr = parseTime(endTime.value)
    const [startH, startM] = startStr.split(':').map(Number)
    const [endH, endM] = endStr.split(':').map(Number)
    
    let diff = (endH * 60 + endM) - (startH * 60 + startM)
    if (diff <= 0) diff += 24 * 60 // cross midnight
    return diff
  }

  // Helper to map days to integers if needed by backend, 
  // but for now we send the array as requested:
  const dayMap: Record<string, string> = { 'L': '0', 'M': '1', 'X': '2', 'J': '3', 'V': '4', 'S': '5', 'D': '6' }
  const payload = {
    title: routineName.value,
    category: selectedCategoryId.value,
    default_duration_minutes: calculateDuration(),
    schedule_rules: [{
      days_of_week: selectedDays.value.map(d => dayMap[d]).join(','),
      start_time: parseTime(startTime.value),
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      reminder_minutes: parseInt(reminder.value.split(' ')[0]) || 10,
      auto_complete: autoComplete.value
    }]
  }

  try {
    await routineStore.createRoutine(payload)
    if (createSuccess.value) {
      alert('¡Rutina creada con éxito!')
      // Optional: reset form
      routineName.value = ''
    }
  } catch (e) {
    console.error(e)
  }
}

onMounted(async () => {
  await routineStore.fetchCategories()
  if (categories.value.length > 0) {
    selectedCategoryId.value = categories.value[0].id
  }
})
</script>

<template>
  <div class="create-routine-page">
    <header class="page-header">
      <h1 class="greeting">Crear Rutina</h1>
      <p class="subtitle">Diseña un nuevo bloque de alto rendimiento.</p>
    </header>

    <div class="form-container">
      <form @submit.prevent="handleSave">
        <BaseCard padding="2rem">
          <div class="form-card">
            
            <div v-if="errorCreate" class="error-banner">
              {{ errorCreate }}
            </div>

            <!-- Nombre -->
            <div class="form-group">
              <BaseInput 
                v-model="routineName"
                label="NOMBRE DE LA RUTINA"
                placeholder="Ej. Bloque de Foco Profundo"
              />
            </div>

            <!-- Categoría -->
            <div class="form-group">
              <label class="group-label">CATEGORÍA</label>
              <div v-if="loadingCategories" class="loading-text">Cargando categorías...</div>
              <div v-else-if="errorCategories" class="error-text">{{ errorCategories }}</div>
              <div v-else class="categories-row">
                <button 
                  type="button"
                  v-for="cat in categories" 
                  :key="cat.id"
                  class="category-btn"
                  :class="{ 'is-selected': selectedCategoryId === cat.id }"
                  :style="{ backgroundColor: getCategoryAppearance(cat.name || '').color }"
                  @click="selectedCategoryId = cat.id"
                  :title="cat.name"
                >
                  <img :src="getCategoryAppearance(cat.name || '').icon" class="category-icon" />
                </button>
              </div>
            </div>

            <!-- Hora y Duración -->
            <div class="form-row">
              <TimePicker 
                v-model="startTime"
                label="HORA DE INICIO"
              />
              <TimePicker 
                v-model="endTime"
                label="HORA DE FIN"
              />
            </div>

            <!-- Días de la semana -->
            <div class="form-group">
              <label class="group-label">DÍAS DE LA SEMANA</label>
              <div class="days-row">
                <button
                  type="button"
                  v-for="day in weekDays"
                  :key="day.id"
                  class="day-btn"
                  :class="{ 'is-active': selectedDays.includes(day.id) }"
                  @click="toggleDay(day.id)"
                >
                  {{ day.label }}
                </button>
              </div>
            </div>

            <!-- Aviso Previo -->
            <div class="form-group half-width">
              <BaseSelect 
                v-model="reminder"
                label="AVISO PREVIO"
                :options="reminderOptions"
              />
            </div>

            <!-- Auto-completar -->
            <div class="form-group auto-complete-group">
              <BaseSwitch 
                v-model="autoComplete"
                label="Auto-completar al Iniciar"
              />
            </div>

            <!-- Submit -->
            <div class="submit-wrapper">
              <BaseButton 
                type="submit"
                variant="primary" 
                class="save-btn" 
                :disabled="loadingCreate"
              >
                <span v-if="loadingCreate" class="material-symbols-outlined icon-small spin">sync</span>
                <span v-else class="material-symbols-outlined icon-small">check_circle</span> 
                {{ loadingCreate ? 'Guardando...' : 'Guardar Rutina' }}
              </BaseButton>
            </div>
          </div>
        </BaseCard>
      </form>
    </div>
  </div>
</template>

<style scoped>
.create-routine-page {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
  max-width: 800px;
}

.page-header {
  margin-bottom: var(--space-2);
}

.greeting {
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 var(--space-1) 0;
}

.subtitle {
  color: var(--text-gray);
  font-size: 1rem;
  margin: 0;
}

.form-container {
  display: flex;
  flex-direction: column;
}

.form-card {
  display: flex;
  flex-direction: column;
  gap: 1.5rem; /* Reduced gap between blocks to balance spacing */
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem; /* Tighter gap between label and input */
}

.half-width {
  max-width: 50%;
}

.group-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-gray);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0; /* Let form-group gap handle it */
}

.loading-text {
  font-size: 0.85rem;
  color: var(--text-gray);
}

.error-text {
  font-size: 0.85rem;
  color: var(--status-expired);
}

.error-banner {
  padding: 1rem;
  background-color: var(--bg-status-danger);
  color: var(--status-expired);
  border-radius: var(--radius-md);
  font-size: 0.9rem;
  font-weight: 600;
}

.categories-row {
  display: flex;
  gap: var(--space-4);
  overflow-x: auto;
  padding-bottom: 4px;
}

.category-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  position: relative;
  flex-shrink: 0;
}

.category-btn::after {
  content: '';
  position: absolute;
  top: -4px;
  left: -4px;
  right: -4px;
  bottom: -4px;
  border: 2px solid var(--color-primary);
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.2s;
}

.category-btn.is-selected::after {
  opacity: 1;
}

.category-icon {
  width: 24px;
  height: 24px;
  object-fit: contain;
  filter: brightness(0) invert(1);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-6);
}

.days-row {
  display: flex;
  gap: var(--space-3);
  overflow-x: auto;
  padding-bottom: 4px;
}

.day-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid var(--border-color);
  background-color: var(--color-white);
  color: var(--text-gray);
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.day-btn.is-active {
  background-color: var(--color-primary);
  color: var(--color-white);
  border-color: var(--color-primary);
}

.divider {
  height: 1px;
  background-color: var(--border-color);
  opacity: 0.5;
  margin: var(--space-2) 0;
}

.auto-complete-group {
  margin-top: var(--space-2);
  max-width: 50%;
}

.submit-btn {
  width: 100%;
  justify-content: center;
  padding: 1rem;
  font-size: 1rem;
  border-radius: var(--radius-md);
  margin-top: var(--space-4);
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
    gap: var(--space-4);
  }

  .days-selector {
    flex-wrap: wrap;
    justify-content: center;
  }

  .day-btn {
    width: 36px;
    height: 36px;
  }
}

.submit-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: var(--space-4);
}

.save-btn {
  min-width: 200px;
}

.icon-small {
  font-size: 1.1rem;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin { 100% { transform: rotate(360deg); } }
</style>
