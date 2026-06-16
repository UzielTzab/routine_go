<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { storeToRefs } from 'pinia'
import BaseCard from '../../shared/components/BaseCard.vue'
import BaseButton from '../../shared/components/BaseButton.vue'
import BaseModal from '../../shared/components/BaseModal.vue'
import { useScheduleStore } from './stores/useScheduleStore'
import { useRoutineStore } from '../routines/stores/useRoutineStore'
import { useToast } from '../../shared/composables/useToast'

const scheduleStore = useScheduleStore()
const routineStore = useRoutineStore()
const { addToast } = useToast()
const { todaySchedule, loading, error } = storeToRefs(scheduleStore)
const { categories } = storeToRefs(routineStore)

const isModalOpen = ref(false)
const selectedItem = ref<any>(null)
const selectedAction = ref<string>('')

const actionTitleMap: Record<string, string> = {
  complete: 'Completar Rutina',
  snooze: 'Posponer Rutina',
  skip: 'Omitir Rutina',
  startEarly: 'Iniciar Anticipadamente',
  delete: 'Eliminar Rutina'
}

const openModal = (item: any, action: string) => {
  selectedItem.value = item
  selectedAction.value = action
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
  selectedItem.value = null
  selectedAction.value = ''
}

const confirmAction = async () => {
  if (!selectedItem.value) return
  
  const id = selectedItem.value.id
  if (selectedAction.value === 'complete') {
    scheduleStore.completeExecution(id)
  } else if (selectedAction.value === 'snooze') {
    scheduleStore.snoozeExecution(id)
  } else if (selectedAction.value === 'skip') {
    scheduleStore.skipExecution(id)
  } else if (selectedAction.value === 'startEarly') {
    scheduleStore.startExecution(id)
  } else if (selectedAction.value === 'delete') {
    if (selectedItem.value.routine?.id) {
      await routineStore.deleteRoutine(selectedItem.value.routine.id)
      scheduleStore.fetchToday()
    }
  }
  
  closeModal()
}

const getComputedStatus = (item: any) => {
  const s = item.status?.toLowerCase() || '';
  if (s === 'completed' || s === 'in-progress' || s === 'in_progress' || s === 'omitted') return s;
  
  if (item.scheduled_end) {
    const end = new Date(item.scheduled_end).getTime();
    if (Date.now() > end) return 'expired';
  }
  return s;
}

const handleStartClick = (item: any) => {
  // 1. Validar que no haya otra rutina corriendo
  const hasActiveRoutine = todaySchedule.value.some(r => {
    const s = getComputedStatus(r)
    return s === 'in-progress' || s === 'in_progress'
  })
  
  if (hasActiveRoutine) {
    addToast('Ya tienes una rutina en progreso. Complétala o páusala primero.', 'error')
    return
  }
  
  // 2. Validar si es muy temprano (más de 5 minutos antes)
  if (item.scheduled_start) {
    const startTime = new Date(item.scheduled_start).getTime();
    // Si faltan más de 5 minutos para que inicie
    if (Date.now() < startTime - (5 * 60 * 1000)) {
      openModal(item, 'startEarly');
      return;
    }
  }
  
  // 3. Iniciar normal
  scheduleStore.startExecution(item.id);
}

const canSnooze = (item: any) => {
  const status = getComputedStatus(item);
  // Ocultar si ya se completó, se omitió o está en progreso
  if (status === 'completed' || status === 'omitted' || status === 'in-progress' || status === 'in_progress') return false;
  
  if (!item.scheduled_start) return true;
  
  const startTime = new Date(item.scheduled_start).getTime();
  const now = Date.now();
  const thirtyMinsInMs = 30 * 60 * 1000;
  
  // Mostrar solo si faltan 30 minutos o menos para que inicie (o si ya pasó la hora)
  return now >= (startTime - thirtyMinsInMs);
}

const getDotColor = (item: any) => {
  const status = getComputedStatus(item);
  switch(status) {
    case 'expired': 
    case 'overdue': return 'var(--status-expired)';
    case 'in_progress': 
    case 'in-progress': return 'var(--status-in-progress)';
    default: return 'var(--text-gray)';
  }
}

// Local icon map based on category name
const getCategoryAppearance = (name: string) => {
  const lowerName = (name || '').toLowerCase()
  if (lowerName.includes('higiene') || lowerName.includes('hygiene')) return { icon: '/images/icons/hygiene.png', color: 'var(--color-hygiene)' }
  if (lowerName.includes('ejercicio') || lowerName.includes('exercise')) return { icon: '/images/icons/excersice.png', color: 'var(--color-exercise)' }
  if (lowerName.includes('foco') || lowerName.includes('focus') || lowerName.includes('trabajo')) return { icon: '/images/icons/focus.png', color: 'var(--color-focus)' }
  if (lowerName.includes('nutrición') || lowerName.includes('nutricion') || lowerName.includes('nutrition') || lowerName.includes('alimentación') || lowerName.includes('alimentacion')) return { icon: '/images/icons/nutrition.png', color: 'var(--color-nutrition)' }
  if (lowerName.includes('sueño') || lowerName.includes('sleep')) return { icon: '/images/icons/sleep.png', color: 'var(--color-sleep)' }
  
  return { icon: '/images/icons/focus.png', color: 'var(--text-primary)' }
}

const formatTime = (isoString: string) => {
  if (!isoString) return '00:00';
  const d = new Date(isoString);
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

const todayDateString = computed(() => {
  return new Date().toLocaleDateString('es-ES', { weekday: 'long', month: 'long', day: 'numeric' })
})

const getCategoryName = (categoryId: number | string) => {
  const cat = categories.value.find((c: any) => c.id === categoryId)
  return cat ? cat.name : 'General'
}

onMounted(async () => {
  if (categories.value.length === 0) {
    await routineStore.fetchCategories()
  }
  scheduleStore.fetchToday()
})
</script>

<template>
  <div class="agenda-page">
    <header class="page-header">
      <div class="header-title-container">
        <h1 class="greeting">Agenda de hoy</h1>
        <img src="/images/icons/scheduler.png" alt="Agenda" class="header-icon" />
      </div>
      <p class="subtitle">{{ todayDateString }}</p>
    </header>

    <div v-if="loading" class="loading-state">
      <span class="material-symbols-outlined spin">sync</span> Cargando agenda...
    </div>

    <div v-else-if="error" class="error-state">
      {{ error }}
    </div>

    <div v-else-if="todaySchedule.length === 0" class="empty-state">
      No tienes rutinas agendadas para hoy.
    </div>

    <div v-else class="schedule-list">
      <div v-for="item in todaySchedule" :key="item.id" class="schedule-item">
        <div class="time-column">
          <div class="time-block" :style="{ color: getComputedStatus(item) === 'expired' ? 'var(--status-expired)' : getComputedStatus(item) === 'in-progress' || getComputedStatus(item) === 'in_progress' ? 'var(--status-in-progress)' : 'var(--text-primary)' }">
            <span class="time-text">{{ formatTime(item.scheduled_start) }}</span>
            <span class="duration-text">{{ item.duration_minutes }} min</span>
            <span v-if="item.actual_start" class="duration-text">Iniciado: {{ formatTime(item.actual_start) }}</span>
          </div>
          <span class="time-dot" :style="{ backgroundColor: getDotColor(item) }"></span>
        </div>
        
        <BaseCard 
          class="task-card" 
          :class="{ 
            'is-active-snake': getComputedStatus(item) === 'in-progress' || getComputedStatus(item) === 'in_progress',
            'is-completed': getComputedStatus(item) === 'completed',
            'is-omitted': getComputedStatus(item) === 'omitted'
          }"
          padding="1rem 1.5rem"
        >
          <div class="task-content">
            <div class="task-info">
              <div class="task-meta">
                <img :src="getCategoryAppearance(getCategoryName(item.routine?.category)).icon" class="meta-icon" />
                <span class="meta-category" :style="{ color: getCategoryAppearance(getCategoryName(item.routine?.category)).color }">
                  {{ getCategoryName(item.routine?.category) }}
                </span>
                
                <span v-if="getComputedStatus(item) === 'completed'" class="status-badge badge-completed">
                  <span class="material-symbols-outlined icon-small">check_circle</span> Completada
                </span>
                <span v-else-if="getComputedStatus(item) === 'expired' || getComputedStatus(item) === 'overdue'" class="status-badge badge-expired">
                  <span class="material-symbols-outlined icon-small">warning</span> Vencida
                </span>
                <span v-else-if="getComputedStatus(item) === 'omitted'" class="status-badge badge-omitted">
                  <span class="material-symbols-outlined icon-small">cancel</span> Omitida
                </span>
                <span v-else-if="getComputedStatus(item) === 'in-progress' || getComputedStatus(item) === 'in_progress'" class="status-badge badge-in-progress">
                  <span class="material-symbols-outlined icon-small">sync</span> En progreso
                </span>
              </div>
              <h3 class="task-title" :class="{ 'text-strikethrough': getComputedStatus(item) === 'completed' || getComputedStatus(item) === 'omitted' }">
                {{ item.routine?.title || 'Rutina' }}
              </h3>
            </div>
            
            <div class="task-actions" v-if="getComputedStatus(item) !== 'completed' && getComputedStatus(item) !== 'omitted'">
              <BaseButton 
                variant="ghost" class="action-btn" 
                v-if="getComputedStatus(item) !== 'in-progress' && getComputedStatus(item) !== 'in_progress'"
                @click="openModal(item, 'skip')"
              >
                Omitir
              </BaseButton>
              <BaseButton 
                variant="secondary" class="action-btn" 
                v-if="canSnooze(item)"
                @click="openModal(item, 'snooze')"
              >
                Posponer +15 min
              </BaseButton>
              <BaseButton 
                variant="primary" class="action-btn" 
                v-if="getComputedStatus(item) === 'in-progress' || getComputedStatus(item) === 'in_progress'"
                @click="openModal(item, 'complete')"
              >
                Completar
              </BaseButton>
              <BaseButton 
                variant="primary" class="action-btn" v-else
                @click="handleStartClick(item)"
              >
                Iniciar
              </BaseButton>
              <button class="icon-btn delete-btn" @click.stop="openModal(item, 'delete')">
                <span class="material-symbols-outlined">delete</span>
              </button>
            </div>
            <div class="task-actions" v-else>
               <span class="status-text-completed" v-if="getComputedStatus(item) === 'completed'">
                  <span class="material-symbols-outlined icon-small">check_circle</span> Completada
               </span>
               <span class="status-text-omitted" v-else-if="getComputedStatus(item) === 'omitted'">
                  <span class="material-symbols-outlined icon-small">cancel</span> Omitida
               </span>
               <button class="icon-btn delete-btn" @click.stop="openModal(item, 'delete')">
                 <span class="material-symbols-outlined">delete</span>
               </button>
            </div>
          </div>
        </BaseCard>
      </div>
    </div>

    <BaseModal 
      v-model="isModalOpen" 
      :title="actionTitleMap[selectedAction] || 'Confirmar Acción'"
    >
      <p v-if="selectedAction === 'complete'">
      <div class="modal-content-inner">
        <div v-if="selectedAction === 'delete'" class="delete-warning">
          <span class="material-symbols-outlined warning-icon">warning</span>
          <p>¿Estás seguro que deseas eliminar permanentemente la rutina <strong>{{ selectedItem?.routine?.title }}</strong>?</p>
          <p class="warning-text">Esto también eliminará todas sus ejecuciones programadas y no se puede deshacer.</p>
        </div>
        <p v-else-if="selectedAction === 'complete'">
          ¿Seguro que deseas marcar '{{ selectedItem?.routine?.title }}' como completada?
        </p>
        <p v-else-if="selectedAction === 'snooze'">
          ¿Seguro que deseas posponer la rutina '{{ selectedItem?.routine?.title }}' por 15 minutos extras?
        </p>
        <p v-else-if="selectedAction === 'startEarly'">
          Todavía falta para tu rutina '{{ selectedItem?.routine?.title }}'. ¿Seguro que deseas iniciarla anticipadamente?
        </p>
        <p v-else-if="selectedAction === 'skip'">
          ¿Seguro que deseas omitir la rutina '{{ selectedItem?.routine?.title }}'?
        </p>
        <p v-else>
          ¿Confirmar esta acción?
        </p>
      </div>

      <template #footer>
        <BaseButton variant="ghost" @click="closeModal">Cancelar</BaseButton>
        <BaseButton variant="primary" @click="confirmAction">Confirmar</BaseButton>
      </template>
    </BaseModal>
  </div>
</template>

<style scoped>
.agenda-page {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
  max-width: 900px;
}

.page-header {
  margin-bottom: var(--space-2);
}

.header-title-container {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-1);
}

.greeting {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
}

.header-icon {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.subtitle {
  color: var(--text-gray);
  font-size: 1rem;
  margin: 0;
}

.loading-state, .error-state, .empty-state {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-6);
  color: var(--text-gray);
  font-weight: 500;
}

.error-state {
  color: var(--status-expired);
}

.spin {
  animation: spin 1s linear infinite;
}
@keyframes spin { 100% { transform: rotate(360deg); } }

.schedule-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.schedule-item {
  display: flex;
  align-items: stretch;
  gap: var(--space-4);
}

.time-column {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  min-width: 100px;
}

.time-block {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.time-text {
  font-size: 0.9rem;
  font-weight: 600;
}

.duration-text {
  font-size: 0.75rem;
  font-weight: 500;
  opacity: 0.7;
}

.time-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.task-card {
  flex-grow: 1;
  transition: all 0.3s ease;
}

.is-completed {
  opacity: 0.5;
}

.text-strikethrough {
  text-decoration: line-through;
  color: var(--text-gray) !important;
}

@property --angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}

.is-active-snake {
  position: relative;
  background-clip: padding-box;
  border: 2px solid transparent;
}

.is-active-snake::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: inherit;
  padding: 2px;
  background: conic-gradient(from var(--angle), transparent 70%, var(--color-primary) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  animation: snake-spin 2s linear infinite;
  pointer-events: none;
}

@keyframes snake-spin {
  to { --angle: 360deg; }
}

.task-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.task-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.task-meta {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.modal-content-inner {
  text-align: center;
  margin: var(--space-4) 0;
}

.delete-warning {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
}

.warning-icon {
  font-size: 3rem;
  color: var(--status-expired);
}

.warning-text {
  font-size: 0.85rem;
  color: var(--status-expired);
}

.meta-icon {
  width: 16px;
  height: 16px;
  object-fit: contain;
}

.meta-category {
  font-size: 0.85rem;
  font-weight: 600;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  margin-left: var(--space-2);
}

.icon-small {
  font-size: 1rem;
}

.badge-expired {
  background-color: var(--bg-status-danger);
  color: var(--status-expired);
}

.badge-in-progress {
  background-color: var(--bg-status-in-progress);
  color: var(--status-in-progress);
}

.badge-omitted {
  background-color: #f1f5f9;
  color: var(--text-gray);
}

.badge-completed {
  display: none; 
}

.task-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.task-actions {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.action-btn {
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
}

@media (max-width: 768px) {
  .agenda-timeline {
    padding-left: 0;
  }
  
  .time-marker {
    display: none;
  }
  
  .task-card {
    width: 100%;
  }

  .task-content {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-4);
  }

  .task-actions {
    width: 100%;
    justify-content: flex-end;
    flex-wrap: wrap;
  }
  
  .action-btn {
    flex: 1 1 40%;
    text-align: center;
    justify-content: center;
  }
}

.status-text-completed, .status-text-omitted {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  color: var(--text-gray);
  font-size: 0.9rem;
  font-weight: 500;
}

.icon-btn.delete-btn {
  background: none;
  border: none;
  color: var(--status-expired);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: var(--space-2);
  border-radius: 50%;
  transition: background-color 0.2s ease;
}

.icon-btn.delete-btn:hover {
  background-color: #fee2e2;
}
</style>
