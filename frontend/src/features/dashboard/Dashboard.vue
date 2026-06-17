<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import BaseCard from '../../shared/components/BaseCard.vue'
import BaseButton from '../../shared/components/BaseButton.vue'
import MetricCard from '../../shared/components/MetricCard.vue'
import { useDashboardStore } from './stores/useDashboardStore'

const router = useRouter()
const dashboardStore = useDashboardStore()
const { dashboardData, loading } = storeToRefs(dashboardStore)

onMounted(async () => {
  await dashboardStore.fetchDashboard()
})

const getCategoryIcon = (categoryCode: string) => {
  const code = (categoryCode || '').toLowerCase()
  if (code.includes('hygiene') || code.includes('higiene')) return '/images/icons/hygiene.png'
  if (code.includes('exercise') || code.includes('ejercicio')) return '/images/icons/excersice.png'
  if (code.includes('focus') || code.includes('work') || code.includes('foco') || code.includes('trabajo')) return '/images/icons/focus.png'
  if (code.includes('nutrition') || code.includes('health') || code.includes('nutrición') || code.includes('nutricion') || code.includes('alimentación') || code.includes('alimentacion')) return '/images/icons/nutrition.png'
  if (code.includes('sleep') || code.includes('sueño') || code.includes('descanso')) return '/images/icons/sleep.png'
  return '/images/icons/focus.png'
}

const formatTime = (isoString: string) => {
  if (!isoString) return ''
  const d = new Date(isoString)
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const displayMetrics = computed(() => {
  const backendMetrics = dashboardData.value?.daily_progress || []
  
  if (backendMetrics.length === 0) {
    return [
      { category_code: 'hygiene', category_name: 'Higiene', percentage: 0 },
      { category_code: 'exercise', category_name: 'Ejercicio', percentage: 0 },
      { category_code: 'focus', category_name: 'Foco', percentage: 0 },
      { category_code: 'nutrition', category_name: 'Alimentación', percentage: 0 },
      { category_code: 'sleep', category_name: 'Descanso', percentage: 0 }
    ]
  }

  return backendMetrics.map((m: any) => ({
    category_code: m.category_code || 'unknown',
    category_name: m.category_name || 'Desconocido',
    percentage: m.percentage || 0
  }))
})


</script>

<template>
  <div class="dashboard-page" v-if="loading">
    <p>Cargando panel...</p>
  </div>
  <div class="dashboard-page" v-else-if="dashboardData">
    <header class="page-header">
      <h1 class="greeting">Buenos días</h1>
      <p class="subtitle">Ready for peak performance today.</p>
    </header>

    <div class="dashboard-grid">
      <!-- Top Row -->
      <div class="top-row">
        <!-- Current Streak -->
        <BaseCard class="streak-card">
          <div class="streak-header">
            <span class="card-label">CURRENT STREAK</span>
            <img src="/images/icons/Fire.png" alt="Streak" class="flame-icon" />
          </div>
          <div class="streak-body">
            <div class="streak-count">
              <span class="number">{{ dashboardData.current_streak }}</span>
              <span class="text">Days</span>
            </div>
            <div class="streak-bars">
              <div v-for="i in 7" :key="i" class="bar" :class="{ 'active': i <= (dashboardData.current_streak % 7 || 7) && dashboardData.current_streak > 0, 'inactive': i > (dashboardData.current_streak % 7 || 7) || dashboardData.current_streak === 0 }"></div>
            </div>
          </div>
        </BaseCard>

        <!-- Active Routine -->
        <BaseCard 
          class="active-routine-card" 
          :class="{ 'is-active-snake': dashboardData.active_routine }"
          padding="0"
        >
          <div class="active-routine-content" v-if="dashboardData.active_routine">
            <div class="routine-info">
              <span class="badge">ACTIVE ROUTINE</span>
              <h2 class="routine-title">{{ dashboardData.active_routine.title }}</h2>
              <span class="routine-category">
                 <img :src="getCategoryIcon(dashboardData.active_routine.category_name)" class="inline-icon" alt="Category"/> {{ dashboardData.active_routine.category_name }}
              </span>
              
              <div class="routine-actions">
                <BaseButton variant="primary" class="pause-btn" @click="router.push('/active-routine')">
                  <span class="material-symbols-outlined">timer</span> Ver Temporizador
                </BaseButton>
              </div>
            </div>
            <div class="routine-timer">
              <div class="timer-circle">
                <span class="time-left">{{ dashboardData.active_routine.duration_minutes }}m</span>
              </div>
              <img src="/images/icons/clock.png" alt="Clock" class="clock-illustration" />
            </div>
          </div>
          <div class="active-routine-content empty-active" v-else>
             <div class="routine-info">
               <h2 class="routine-title">Sin Rutina Activa</h2>
               <p class="routine-category">Dirígete a tu agenda para comenzar tu día.</p>
               <BaseButton variant="primary" class="pause-btn" @click="router.push('/agenda')">Ver Agenda</BaseButton>
             </div>
             <div class="routine-timer empty-timer">
               <img src="/images/icons/clock.png" alt="Clock" class="clock-illustration" style="opacity: 0.5;" />
             </div>
          </div>
        </BaseCard>
      </div>

      <!-- Metrics Row -->
      <BaseCard title="DAILY PROGRESS" class="metrics-card">
        <div class="metrics-container" v-if="displayMetrics && displayMetrics.length > 0">
          <MetricCard 
            v-for="metric in displayMetrics" 
            :key="metric.category_code"
            :category="metric.category_code"
            :label="metric.category_name"
            :progress="metric.percentage"
            :icon="getCategoryIcon(metric.category_name)"
          />
        </div>
        <div v-else class="metrics-container">
          <p style="color: var(--text-gray); font-size: 0.9rem;">No hay progreso aún. ¡Inicia una rutina!</p>
        </div>
      </BaseCard>

      <!-- Bottom Row -->
      <div class="bottom-row">
        <!-- Up Next -->
        <BaseCard title="UP NEXT" class="up-next-card">
          <div class="next-item" v-if="dashboardData.up_next">
            <div class="item-icon-wrapper" :style="{ backgroundColor: dashboardData.up_next.category_color }">
              <img :src="getCategoryIcon(dashboardData.up_next.category_color)" alt="Category" class="item-img-icon" />
            </div>
            <div class="item-details">
              <h4 class="item-title">{{ dashboardData.up_next.title }}</h4>
              <span class="item-time">{{ formatTime(dashboardData.up_next.scheduled_start) }}</span>
            </div>
          </div>
          <div v-else class="next-item">
            <p style="color: var(--text-gray);">No hay más rutinas programadas para hoy.</p>
          </div>
        </BaseCard>

        <!-- Weekly Compliance -->
        <BaseCard class="compliance-card">
          <div class="compliance-header">
            <span class="card-label">WEEKLY COMPLIANCE</span>
            <span class="avg-label">{{ dashboardData.weekly_compliance.average }}% AVG</span>
          </div>
          <div class="chart-placeholder">
            <div class="chart-bars">
              <div class="chart-bar" 
                   v-for="(day, index) in dashboardData.weekly_compliance.days" 
                   :key="index"
                   :class="{ 'active': day.is_today }"
                   :style="{ height: Math.max(day.progress, 5) + '%' }">
                <span>{{ day.day }}</span>
              </div>
            </div>
          </div>
        </BaseCard>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-page {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.page-header {
  margin-bottom: var(--space-2);
}

.greeting {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: var(--space-1);
}

.subtitle {
  color: var(--text-gray);
  font-size: 1rem;
}

.dashboard-grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.top-row {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: var(--space-6);
}

/* Streak Card */
.streak-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-gray);
  letter-spacing: 0.05em;
}

.flame-icon {
  width: 32px;
  height: 32px;
  object-fit: contain;
}

.streak-body {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  margin-top: var(--space-2);
}

.streak-count {
  display: flex;
  align-items: baseline;
  gap: var(--space-2);
}

.number {
  font-size: 3rem;
  font-weight: 700;
  line-height: 1;
}

.text {
  color: var(--text-gray);
  font-weight: 600;
}

.streak-bars {
  display: flex;
  gap: 4px;
}

.bar {
  height: 4px;
  flex-grow: 1;
  border-radius: 2px;
}

.bar.active {
  background-color: #D97706; /* Placeholder for orange */
}

.bar.inactive {
  background-color: var(--border-color);
}

/* Active Routine Card */
.active-routine-card {
  background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);
  border: none;
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

.active-routine-content {
  display: flex;
  justify-content: space-between;
  padding: var(--space-6);
  height: 100%;
}

.routine-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--space-2);
}

.badge {
  background-color: rgba(184, 183, 255, 0.3);
  color: var(--color-focus);
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 700;
}

.routine-title {
  font-size: 1.5rem;
  margin: 0;
}

.inline-icon {
  width: 14px;
  height: 14px;
  vertical-align: middle;
  margin-right: 4px;
}

.routine-category {
  color: var(--text-gray);
  font-size: 0.9rem;
  margin-bottom: var(--space-4);
  display: flex;
  align-items: center;
}

.pause-btn {
  background-color: #C4B5FD;
  color: var(--sidebar-bg);
  min-width: 150px;
}

.routine-timer {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
}

.timer-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: 4px solid var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-focus);
  font-weight: 700;
  font-size: 0.85rem;
}

.clock-illustration {
  width: 80px;
  height: 80px;
  margin-top: -10px;
  object-fit: contain;
}

/* Metrics Card */
.metrics-container {
  display: flex;
  justify-content: space-between;
  padding: var(--space-4) 0;
}

/* Bottom Row */
.bottom-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-6);
}

.next-item {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  margin-top: var(--space-4);
}

.item-icon-wrapper {
  width: 48px;
  height: 48px;
  background-color: var(--bg-status-danger);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-img-icon {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.item-title {
  margin: 0 0 var(--space-1) 0;
  font-size: 1.1rem;
}

.item-time {
  color: var(--text-gray);
  font-size: 0.85rem;
}

.compliance-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
}

.avg-label {
  color: var(--color-hygiene);
  font-weight: 700;
  font-size: 0.85rem;
}

.chart-placeholder {
  flex-grow: 1;
  display: flex;
  align-items: flex-end;
  height: 150px;
}

.chart-bars {
  display: flex;
  justify-content: space-between;
  width: 100%;
  height: 100%;
  align-items: flex-end;
  gap: var(--space-2);
}

.chart-bar {
  flex-grow: 1;
  background-color: var(--border-color);
  border-radius: 4px 4px 0 0;
  position: relative;
  display: flex;
  justify-content: center;
}

.chart-bar.active {
  background-color: #1D4ED8; /* Darker blue */
}

.chart-bar:nth-child(4) {
  background-color: var(--status-in-progress);
}

.chart-bar span {
  position: absolute;
  bottom: -25px;
  font-size: 0.75rem;
  color: var(--text-gray);
}

@media (max-width: 768px) {
  .top-row {
    grid-template-columns: 1fr;
  }

  .bottom-row {
    grid-template-columns: 1fr;
  }

  .metrics-container {
    overflow-x: auto;
    justify-content: flex-start;
    gap: var(--space-6);
    padding-bottom: var(--space-4);
  }
}
</style>
