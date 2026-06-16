<script setup lang="ts">
import { ref, watch } from 'vue'
import BaseModal from '../../shared/components/BaseModal.vue'
import BaseInput from '../../shared/components/BaseInput.vue'
import BaseButton from '../../shared/components/BaseButton.vue'
import { useRoutineStore } from './stores/useRoutineStore'
import { useToast } from '../../shared/composables/useToast'

const props = defineProps<{
  isOpen: boolean
  routine: any
}>()

const emit = defineEmits(['close', 'saved'])

const routineStore = useRoutineStore()
const { addToast } = useToast()

const title = ref('')
const selectedDays = ref<string[]>([])
const loading = ref(false)

const weekDays = [
  { id: 'L', value: '0' },
  { id: 'M', value: '1' },
  { id: 'X', value: '2' },
  { id: 'J', value: '3' },
  { id: 'V', value: '4' },
  { id: 'S', value: '5' },
  { id: 'D', value: '6' }
]

watch(() => props.isOpen, (newVal) => {
  if (newVal && props.routine) {
    title.value = props.routine.title || ''
    
    // Parse existing days from the first schedule rule
    if (props.routine.schedule_rules && props.routine.schedule_rules.length > 0) {
      const rule = props.routine.schedule_rules[0]
      const days = (rule.days_of_week || '').split(',')
      
      // Map '0' to 'L', '1' to 'M', etc.
      selectedDays.value = days.map((d: string) => {
        const match = weekDays.find(w => w.value === d.trim())
        return match ? match.id : ''
      }).filter(Boolean)
    } else {
      selectedDays.value = []
    }
  }
})

const toggleDay = (dayId: string) => {
  if (selectedDays.value.includes(dayId)) {
    selectedDays.value = selectedDays.value.filter(d => d !== dayId)
  } else {
    selectedDays.value.push(dayId)
  }
}

const handleSave = async () => {
  if (!title.value.trim()) {
    addToast('El nombre de la rutina es requerido', 'error')
    return
  }
  if (selectedDays.value.length === 0) {
    addToast('Selecciona al menos un día', 'error')
    return
  }

  loading.value = true
  try {
    const dayMap: Record<string, string> = { 'L': '0', 'M': '1', 'X': '2', 'J': '3', 'V': '4', 'S': '5', 'D': '6' }
    
    // Preserve other rule settings (hours, category, etc.)
    const currentRule = props.routine.schedule_rules && props.routine.schedule_rules.length > 0 
      ? props.routine.schedule_rules[0] 
      : {}
      
    // Exclude 'id' from currentRule to avoid passing it during PATCH if needed, 
    // but the backend update_routine_with_rules will recreate it or update it.
    const ruleData = { ...currentRule }
    delete ruleData.id
      
    const payload = {
      title: title.value,
      schedule_rules: [{
        ...ruleData,
        days_of_week: selectedDays.value.map(d => dayMap[d]).join(',')
      }]
    }

    await routineStore.updateRoutine(props.routine.id, payload)
    addToast('Rutina actualizada exitosamente', 'success')
    emit('saved')
    emit('close')
  } catch (err: any) {
    addToast('Error al actualizar rutina', 'error')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <BaseModal :is-open="isOpen" title="Editar Rutina" @close="$emit('close')">
    <div class="edit-form">
      <div class="form-group">
        <label>Nombre de la rutina</label>
        <BaseInput v-model="title" placeholder="Ej: Leer 10 páginas" />
      </div>

      <div class="form-group">
        <label>Días de la semana</label>
        <div class="days-selector">
          <button 
            v-for="day in weekDays" 
            :key="day.id"
            class="day-btn"
            :class="{ 'active': selectedDays.includes(day.id) }"
            @click="toggleDay(day.id)"
          >
            {{ day.id }}
          </button>
        </div>
      </div>
    </div>
    
    <template #footer>
      <BaseButton variant="ghost" @click="$emit('close')" :disabled="loading">Cancelar</BaseButton>
      <BaseButton variant="primary" @click="handleSave" :disabled="loading">Guardar Cambios</BaseButton>
    </template>
  </BaseModal>
</template>

<style scoped>
.edit-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  margin-bottom: var(--space-4);
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: var(--space-2);
  color: var(--text-primary);
  font-size: 0.95rem;
}

.days-selector {
  display: flex;
  gap: var(--space-2);
  justify-content: flex-start;
  flex-wrap: wrap;
}

.day-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid var(--border-color);
  background-color: var(--bg-card);
  color: var(--text-primary);
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.day-btn.active {
  background-color: var(--color-primary);
  color: var(--color-white);
  border-color: var(--color-primary);
}
</style>
