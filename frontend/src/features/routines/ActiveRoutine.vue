<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import BaseCard from '../../shared/components/BaseCard.vue'
import BaseButton from '../../shared/components/BaseButton.vue'
import BaseModal from '../../shared/components/BaseModal.vue'
import { useScheduleStore } from '../../features/schedule/stores/useScheduleStore'
import { useRoutineStore } from '../../features/routines/stores/useRoutineStore'

const router = useRouter()
const scheduleStore = useScheduleStore()
const routineStore = useRoutineStore()
const { todaySchedule } = storeToRefs(scheduleStore)
const { categories } = storeToRefs(routineStore)

const activeItem = ref<any>(null)
const timerInterval = ref<any>(null)
const remainingMs = ref(0)

const getCategoryName = (categoryId: number | string) => {
  const cat = categories.value.find((c: any) => c.id === categoryId)
  return cat ? cat.name : 'General'
}

const getCategoryAppearance = (name: string) => {
  const lowerName = (name || '').toLowerCase()
  if (lowerName.includes('higiene') || lowerName.includes('hygiene')) return { icon: '/images/icons/hygiene.png', color: 'var(--color-hygiene)' }
  if (lowerName.includes('ejercicio') || lowerName.includes('exercise')) return { icon: '/images/icons/excersice.png', color: 'var(--color-exercise)' }
  if (lowerName.includes('foco') || lowerName.includes('focus') || lowerName.includes('trabajo')) return { icon: '/images/icons/focus.png', color: 'var(--color-focus)' }
  if (lowerName.includes('nutrición') || lowerName.includes('nutricion') || lowerName.includes('nutrition') || lowerName.includes('alimentación') || lowerName.includes('alimentacion')) return { icon: '/images/icons/nutrition.png', color: 'var(--color-nutrition)' }
  if (lowerName.includes('sueño') || lowerName.includes('sleep')) return { icon: '/images/icons/sleep.png', color: 'var(--color-sleep)' }
  
  return { icon: '/images/icons/focus.png', color: 'var(--color-focus)' }
}

onMounted(async () => {
  if (categories.value.length === 0) {
    await routineStore.fetchCategories()
  }
  await scheduleStore.fetchToday()
  
  activeItem.value = todaySchedule.value.find((item: any) => 
    item.status?.toLowerCase() === 'in-progress' || item.status?.toLowerCase() === 'in_progress'
  )

  if (activeItem.value) {
    const durationMins = activeItem.value.duration_minutes || activeItem.value.routine?.default_duration_minutes || 60
    const totalDurationMs = durationMins * 60 * 1000
    
    let elapsedMs = 0
    if (activeItem.value.actual_start) {
      const startTime = new Date(activeItem.value.actual_start).getTime()
      elapsedMs = Date.now() - startTime
    }
    
    remainingMs.value = Math.max(0, totalDurationMs - elapsedMs)
    
    timerInterval.value = setInterval(() => {
      if (remainingMs.value > 0) {
        remainingMs.value -= 1000
      } else {
        clearInterval(timerInterval.value)
      }
    }, 1000)
  }
})

onUnmounted(() => {
  if (timerInterval.value) clearInterval(timerInterval.value)
})

const displayTime = computed(() => {
  if (remainingMs.value <= 0) return '00:00'
  const totalSeconds = Math.floor(remainingMs.value / 1000)
  const hours = Math.floor(totalSeconds / 3600)
  const minutes = Math.floor((totalSeconds % 3600) / 60)
  const seconds = totalSeconds % 60
  
  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
  }
  return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
})

const formatTime = (isoString: string) => {
  if (!isoString) return ''
  const d = new Date(isoString)
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const upcomingRoutines = computed(() => {
  return todaySchedule.value.filter((item: any) => {
    const s = item.status?.toLowerCase() || ''
    if (s === 'completed' || s === 'omitted' || s === 'in-progress' || s === 'in_progress') return false
    
    if (item.scheduled_end) {
      const end = new Date(item.scheduled_end).getTime()
      if (Date.now() > end) return false // hide expired
    }
    return true
  }).sort((a: any, b: any) => {
    const timeA = new Date(a.scheduled_start || 0).getTime()
    const timeB = new Date(b.scheduled_start || 0).getTime()
    return timeA - timeB
  })
})

const handleStartClick = (item: any) => {
  if (activeItem.value) {
    alert('Ya tienes una rutina en progreso.')
    return
  }
  
  if (item.scheduled_start) {
    const startTime = new Date(item.scheduled_start).getTime()
    if (Date.now() < startTime - (5 * 60 * 1000)) {
      selectedItem.value = item
      openModal('startEarly')
      return
    }
  }
  
  startExecution(item)
}

const startExecution = async (item: any) => {
  await scheduleStore.startExecution(item.id)
  // Al iniciar, tenemos que refrescar la vista.
  // ActiveRoutine hace fetchToday en onMounted, pero podemos recargar manualmente:
  window.location.reload()
}

const isModalOpen = ref(false)
const selectedAction = ref<string>('')
const selectedItem = ref<any>(null)

const actionTitleMap: Record<string, string> = {
  complete: 'Completar Rutina',
  skip: 'Omitir Rutina',
  startEarly: 'Iniciar Anticipadamente'
}

const openModal = (action: string) => {
  selectedAction.value = action
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
  selectedAction.value = ''
  selectedItem.value = null
}

const confirmAction = async () => {
  if (selectedAction.value === 'startEarly' && selectedItem.value) {
    await startExecution(selectedItem.value)
  } else if (activeItem.value) {
    if (selectedAction.value === 'complete') {
      await scheduleStore.completeExecution(activeItem.value.id)
      router.push('/')
    } else if (selectedAction.value === 'skip') {
      await scheduleStore.skipExecution(activeItem.value.id)
      router.push('/')
    }
  }
  
  closeModal()
}
</script>

<template>
  <div class="active-routine-page">
    <div class="bg-plants"></div>
    
    <div class="routine-content" v-if="activeItem">
      <header class="routine-header">
        <div class="category-badge">
          <img :src="getCategoryAppearance(getCategoryName(activeItem.routine?.category)).icon" class="category-icon" alt="Focus"/>
          <span class="category-text" :style="{ color: getCategoryAppearance(getCategoryName(activeItem.routine?.category)).color }">
            {{ getCategoryName(activeItem.routine?.category) }}
          </span>
        </div>
        <h1 class="routine-title">{{ activeItem.routine?.title || 'Rutina Activa' }}</h1>
        <p class="routine-subtitle">{{ activeItem.routine?.instructions || 'Mantén el foco y logra tu objetivo' }}</p>
      </header>

      <div class="timer-container">
        <div class="timer-circle-large" :style="{ borderColor: getCategoryAppearance(getCategoryName(activeItem.routine?.category)).color }">
          <div class="timer-text-container">
            <span class="time-display">{{ displayTime }}</span>
            <span class="time-label">RESTANTE</span>
          </div>
        </div>
      </div>

      <div class="bottom-actions-container">
        <BaseCard class="info-card" padding="2rem">
          <div class="info-content">
            <div class="minus-icon-wrapper" :style="{ backgroundColor: getCategoryAppearance(getCategoryName(activeItem.routine?.category)).color }">
              <span class="material-symbols-outlined icon-minus">remove</span>
            </div>
            <p class="info-text">
              Elimina distracciones, activa modo no molestar y concéntrate en una sola tarea.
            </p>
          </div>
        </BaseCard>

        <div class="action-buttons">
          <BaseButton variant="primary" class="main-btn" @click="openModal('complete')">
            <span class="material-symbols-outlined">check_circle</span> Completar
          </BaseButton>

          <BaseButton variant="ghost" class="side-btn" @click="openModal('skip')">
            Omitir <span class="material-symbols-outlined">skip_next</span>
          </BaseButton>
        </div>
      </div>
    </div>
    <div v-else class="routine-content empty-content">
      <span class="material-symbols-outlined empty-icon">timer_off</span>
      <h1 class="routine-title">Ninguna Rutina Activa</h1>
      <p class="routine-subtitle">¡Pero puedes activarla desde tu agenda!</p>
      
      <div v-if="upcomingRoutines.length > 0" class="upcoming-list-container">
        <h3 class="upcoming-title">Próximas rutinas:</h3>
        <div class="upcoming-scroll">
          <BaseCard 
            v-for="item in upcomingRoutines" 
            :key="item.id" 
            class="upcoming-card"
            padding="1rem"
            @click="handleStartClick(item)"
          >
            <div class="upcoming-item-content">
              <div class="upcoming-left">
                 <img :src="getCategoryAppearance(getCategoryName(item.routine?.category)).icon" class="upcoming-icon" />
                 <div class="upcoming-text">
                   <span class="upcoming-item-title">{{ item.routine?.title }}</span>
                   <span class="upcoming-item-time">{{ formatTime(item.scheduled_start) }}</span>
                 </div>
              </div>
              <span class="material-symbols-outlined play-icon">play_circle</span>
            </div>
          </BaseCard>
        </div>
      </div>
      
      <BaseButton v-else variant="primary" class="main-btn mt-6" @click="router.push('/agenda')">
        Ir a Agenda
      </BaseButton>
    </div>

    <BaseModal 
      v-model="isModalOpen" 
      :title="actionTitleMap[selectedAction] || 'Confirmar Acción'"
    >
      <p v-if="selectedAction === 'complete'">
        ¿Seguro que deseas marcar '{{ activeItem?.routine?.title }}' como completada? ¡Gran trabajo!
      </p>
      <p v-else-if="selectedAction === 'skip'">
        ¿Seguro que deseas omitir el resto de la rutina '{{ activeItem?.routine?.title }}'?
      </p>
      <p v-else-if="selectedAction === 'startEarly'">
        Todavía falta para tu rutina '{{ selectedItem?.routine?.title }}'. ¿Seguro que deseas iniciarla anticipadamente?
      </p>
      <p v-else>
        ¿Confirmar esta acción?
      </p>

      <template #footer>
        <BaseButton variant="ghost" @click="closeModal">Cancelar</BaseButton>
        <BaseButton variant="primary" @click="confirmAction">Confirmar</BaseButton>
      </template>
    </BaseModal>
  </div>
</template>

<style scoped>
.active-routine-page {
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.bg-plants {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('/images/plants.png');
  background-size: cover;
  background-position: center;
  opacity: 0.8;
  z-index: 0;
  pointer-events: none;
}

.routine-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 800px;
  height: 100%;
  justify-content: space-between;
  padding: var(--space-4) 0 var(--space-12) 0;
}

.routine-header {
  text-align: center;
  margin-top: var(--space-8);
}

.category-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  margin-bottom: var(--space-2);
}

.category-icon {
  width: 16px;
  height: 16px;
  object-fit: contain;
}

.category-text {
  color: var(--color-focus);
  font-weight: 700;
  font-size: 0.9rem;
}

.routine-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 var(--space-1) 0;
  color: var(--text-primary);
}

.routine-subtitle {
  color: var(--text-gray);
  font-size: 1.1rem;
  margin: 0;
}

.timer-container {
  flex-grow: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.timer-circle-large {
  width: 350px;
  height: 350px;
  border-radius: 50%;
  border: 12px solid var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
}

.timer-text-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.time-display {
  font-size: 5.5rem;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1;
  letter-spacing: -0.02em;
}

.time-label {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--text-gray);
  letter-spacing: 0.1em;
  margin-top: var(--space-2);
}

.bottom-actions-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-6);
}

.info-card {
  width: 100%;
  max-width: 600px;
}

.info-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--space-3);
}

.minus-icon-wrapper {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-white);
}

.icon-minus {
  font-size: 1.2rem;
}

.info-text {
  color: var(--text-primary);
  font-size: 1rem;
  font-weight: 500;
  line-height: 1.5;
  margin: 0;
}

.action-buttons {
  display: flex;
  align-items: center;
  gap: var(--space-8);
  margin-top: var(--space-4);
}

.main-btn {
  padding: 1rem 3rem !important;
  font-size: 1.1rem !important;
  border-radius: var(--radius-xl) !important;
}

.side-btn {
  color: var(--text-gray) !important;
  font-weight: 600 !important;
}

.side-btn:hover {
  background-color: transparent !important;
  color: var(--text-primary) !important;
}

@media (max-width: 768px) {
  .timer-circle-large {
    width: 280px;
    height: 280px;
  }

  .time-display {
    font-size: 4rem;
  }

  .action-buttons {
    flex-direction: column;
    gap: var(--space-3);
  }

  .main-btn {
    width: 100%;
    order: -1; /* Make complete button appear first on mobile */
  }

  .side-btn {
    width: 100%;
    text-align: center;
    justify-content: center;
  }
}

.empty-content {
  justify-content: center;
  text-align: center;
  gap: var(--space-4);
}

.empty-icon {
  font-size: 6rem;
  color: var(--text-gray);
  opacity: 0.5;
  margin-bottom: var(--space-2);
}

.upcoming-list-container {
  width: 100%;
  max-width: 400px;
  margin-top: var(--space-6);
  text-align: left;
}

.upcoming-title {
  color: var(--text-gray);
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: var(--space-3);
  font-weight: 700;
}

.upcoming-scroll {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  max-height: 250px;
  overflow-y: auto;
  padding-right: var(--space-2);
}

.upcoming-card {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  background-color: var(--bg-card);
}

.upcoming-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--color-primary-light);
}

.upcoming-item-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.upcoming-left {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.upcoming-icon {
  width: 24px;
  height: 24px;
}

.upcoming-text {
  display: flex;
  flex-direction: column;
}

.upcoming-item-title {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 1rem;
}

.upcoming-item-time {
  font-size: 0.85rem;
  color: var(--text-gray);
}

.play-icon {
  color: var(--color-primary);
  font-size: 2rem;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.upcoming-card:hover .play-icon {
  opacity: 1;
}

.mt-6 {
  margin-top: var(--space-6);
}
</style>
