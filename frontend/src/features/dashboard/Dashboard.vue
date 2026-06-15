<script setup lang="ts">
import BaseCard from '../../shared/components/BaseCard.vue'
import BaseButton from '../../shared/components/BaseButton.vue'
import MetricCard from '../../shared/components/MetricCard.vue'

// Data based on the image using local icon paths
const metrics = [
  { category: 'hygiene', label: 'Hygiene', progress: 100, icon: '/images/icons/hygiene.png' },
  { category: 'exercise', label: 'Exercise', progress: 0, icon: '/images/icons/excersice.png' },
  { category: 'focus', label: 'Focus', progress: 60, icon: '/images/icons/focus.png' },
  { category: 'nutrition', label: 'Nutrition', progress: 30, icon: '/images/icons/nutrition.png' },
  { category: 'sleep', label: 'Sleep', progress: 85, icon: '/images/icons/sleep.png' },
]
</script>

<template>
  <div class="dashboard-page">
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
              <span class="number">5</span>
              <span class="text">Days</span>
            </div>
            <div class="streak-bars">
              <div class="bar active"></div>
              <div class="bar active"></div>
              <div class="bar active"></div>
              <div class="bar active"></div>
              <div class="bar active"></div>
              <div class="bar inactive"></div>
              <div class="bar inactive"></div>
            </div>
          </div>
        </BaseCard>

        <!-- Active Routine -->
        <BaseCard class="active-routine-card" padding="0">
          <div class="active-routine-content">
            <div class="routine-info">
              <span class="badge">ACTIVE ROUTINE</span>
              <h2 class="routine-title">Deep Work Session</h2>
              <span class="routine-category">
                 <img src="/images/icons/focus.png" class="inline-icon" alt="Focus"/> Focus
              </span>
              
              <div class="routine-actions">
                <BaseButton variant="primary" class="pause-btn">
                  <span class="material-symbols-outlined">pause</span> Pause
                </BaseButton>
              </div>
            </div>
            <div class="routine-timer">
              <div class="timer-circle">
                <span class="time-left">25m</span>
              </div>
              <img src="/images/icons/clock.png" alt="Clock" class="clock-illustration" />
            </div>
          </div>
        </BaseCard>
      </div>

      <!-- Middle Row -->
      <BaseCard title="DAILY PROGRESS" class="metrics-card">
        <div class="metrics-container">
          <MetricCard 
            v-for="metric in metrics" 
            :key="metric.category"
            :category="metric.category"
            :label="metric.label"
            :progress="metric.progress"
            :icon="metric.icon"
          />
        </div>
      </BaseCard>

      <!-- Bottom Row -->
      <div class="bottom-row">
        <!-- Up Next -->
        <BaseCard title="UP NEXT" class="up-next-card">
          <div class="next-item">
            <div class="item-icon-wrapper">
              <img src="/images/icons/nutrition.png" alt="Nutrition" class="item-img-icon" />
            </div>
            <div class="item-details">
              <h4 class="item-title">Healthy Lunch</h4>
              <span class="item-time">13:30 - Nutrition</span>
            </div>
          </div>
        </BaseCard>

        <!-- Weekly Compliance -->
        <BaseCard class="compliance-card">
          <div class="compliance-header">
            <span class="card-label">WEEKLY COMPLIANCE</span>
            <span class="avg-label">76% AVG</span>
          </div>
          <div class="chart-placeholder">
            <div class="chart-bars">
              <div class="chart-bar" style="height: 30%"><span>M</span></div>
              <div class="chart-bar" style="height: 40%"><span>T</span></div>
              <div class="chart-bar" style="height: 20%"><span>W</span></div>
              <div class="chart-bar" style="height: 45%"><span>T</span></div>
              <div class="chart-bar active" style="height: 85%"><span>F</span></div>
              <div class="chart-bar" style="height: 10%"><span>S</span></div>
              <div class="chart-bar" style="height: 5%"><span>S</span></div>
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
