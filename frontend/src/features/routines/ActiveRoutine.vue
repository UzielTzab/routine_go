<script setup lang="ts">
import BaseCard from '../../shared/components/BaseCard.vue'
import BaseButton from '../../shared/components/BaseButton.vue'
</script>

<template>
  <div class="active-routine-page">
    <div class="bg-plants"></div>
    
    <div class="routine-content">
      <header class="routine-header">
        <div class="category-badge">
          <img src="/images/icons/focus.png" class="category-icon" alt="Focus"/>
          <span class="category-text">Foco</span>
        </div>
        <h1 class="routine-title">Trabajo Profundo</h1>
        <p class="routine-subtitle">Proyecto Alpha</p>
      </header>

      <div class="timer-container">
        <div class="timer-circle-large">
          <div class="timer-text-container">
            <span class="time-display">24:15</span>
            <span class="time-label">RESTANTE</span>
          </div>
        </div>
      </div>

      <div class="bottom-actions-container">
        <BaseCard class="info-card" padding="2rem">
          <div class="info-content">
            <div class="minus-icon-wrapper">
              <span class="material-symbols-outlined icon-minus">remove</span>
            </div>
            <p class="info-text">
              Elimina distracciones, activa modo no molestar y concéntrate en una sola tarea.
            </p>
          </div>
        </BaseCard>

        <div class="action-buttons">
          <BaseButton variant="ghost" class="side-btn">
            <span class="material-symbols-outlined">pause</span> Pausar
          </BaseButton>
          
          <BaseButton variant="primary" class="main-btn">
            <span class="material-symbols-outlined">check_circle</span> Start Routine
          </BaseButton>

          <BaseButton variant="ghost" class="side-btn">
            Omitir <span class="material-symbols-outlined">skip_next</span>
          </BaseButton>
        </div>
      </div>
    </div>
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
</style>
