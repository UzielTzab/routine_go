<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { storeToRefs } from 'pinia'
import BaseCard from '../../shared/components/BaseCard.vue'
import BaseButton from '../../shared/components/BaseButton.vue'
import { useScheduleStore } from './stores/useScheduleStore'

const scheduleStore = useScheduleStore()
const { todaySchedule, loading, error } = storeToRefs(scheduleStore)

// Map backend status to our dot colors
const getDotColor = (status: string) => {
  switch(status?.toLowerCase()) {
    case 'expired': 
    case 'overdue': return 'var(--status-expired)';
    case 'in_progress': 
    case 'in-progress': return 'var(--status-in-progress)';
    default: return 'var(--text-gray)';
  }
}

// Local icon map based on category name
const getCategoryAppearance = (name: string) => {
  const map: Record<string, { icon: string, color: string }> = {
    'hygiene': { icon: '/images/icons/hygiene.png', color: 'var(--color-hygiene)' },
    'exercise': { icon: '/images/icons/excersice.png', color: 'var(--color-exercise)' },
    'focus': { icon: '/images/icons/focus.png', color: 'var(--color-focus)' },
    'nutrition': { icon: '/images/icons/nutrition.png', color: 'var(--color-nutrition)' },
    'sleep': { icon: '/images/icons/sleep.png', color: 'var(--color-sleep)' },
  }
  const lowerName = (name || '').toLowerCase()
  return map[lowerName] || { icon: '/images/icons/focus.png', color: 'var(--text-primary)' }
}

onMounted(() => {
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
      <p class="subtitle">Wednesday, October 25</p>
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
          <span class="time-text" :style="{ color: item.status === 'expired' ? 'var(--status-expired)' : item.status === 'in-progress' ? 'var(--status-in-progress)' : 'var(--text-primary)' }">
            {{ item.start_time || '00:00' }}
          </span>
          <span class="time-dot" :style="{ backgroundColor: getDotColor(item.status) }"></span>
        </div>
        
        <BaseCard class="task-card" padding="1rem 1.5rem">
          <div class="task-content">
            <div class="task-info">
              <div class="task-meta">
                <img :src="getCategoryAppearance(item.category?.name).icon" class="meta-icon" />
                <span class="meta-category" :style="{ color: getCategoryAppearance(item.category?.name).color }">
                  {{ item.category?.name || 'General' }}
                </span>
                
                <span v-if="item.status === 'completed'" class="status-badge badge-completed">
                  <span class="material-symbols-outlined icon-small">check_circle</span> Completada
                </span>
                <span v-else-if="item.status === 'expired' || item.status === 'overdue'" class="status-badge badge-expired">
                  <span class="material-symbols-outlined icon-small">warning</span> Vencida
                </span>
                <span v-else-if="item.status === 'in-progress' || item.status === 'in_progress'" class="status-badge badge-in-progress">
                  <span class="material-symbols-outlined icon-small">sync</span> En progreso
                </span>
              </div>
              <h3 class="task-title">{{ item.title || item.template?.name || 'Rutina' }}</h3>
            </div>
            
            <div class="task-actions" v-if="item.status !== 'completed'">
              <BaseButton variant="ghost" class="action-btn" v-if="item.status !== 'in-progress' && item.status !== 'in_progress'">
                Omitir
              </BaseButton>
              <BaseButton variant="secondary" class="action-btn">
                Posponer{{ (item.status === 'in-progress' || item.status === 'in_progress') ? ' +15' : '' }}
              </BaseButton>
              <BaseButton variant="primary" class="action-btn" v-if="item.status === 'in-progress' || item.status === 'in_progress'">
                Completar
              </BaseButton>
              <BaseButton variant="primary" class="action-btn" v-else>
                Iniciar
              </BaseButton>
            </div>
            <div class="task-actions" v-else>
               <span class="status-text-completed">
                  <span class="material-symbols-outlined icon-small">check_circle</span> Completada
               </span>
            </div>
          </div>
        </BaseCard>
      </div>
    </div>
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

.time-text {
  font-size: 0.9rem;
  font-weight: 600;
}

.time-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.task-card {
  flex-grow: 1;
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

.status-text-completed {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  color: var(--text-gray);
  font-size: 0.9rem;
  font-weight: 500;
}
</style>
