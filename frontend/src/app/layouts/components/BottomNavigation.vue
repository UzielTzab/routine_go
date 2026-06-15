<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <nav class="bottom-navigation">
    <RouterLink to="/" class="nav-item" exact-active-class="active">
      <span class="material-symbols-outlined nav-icon">grid_view</span>
      <span class="nav-label">Dashboard</span>
    </RouterLink>
    <RouterLink to="/agenda" class="nav-item" exact-active-class="active">
      <span class="material-symbols-outlined nav-icon">calendar_today</span>
      <span class="nav-label">Agenda</span>
    </RouterLink>
    <RouterLink to="/active-routine" class="nav-item" exact-active-class="active">
      <span class="material-symbols-outlined nav-icon">play_circle</span>
      <span class="nav-label">Rutina</span>
    </RouterLink>
    <RouterLink to="/create-routine" class="nav-item" exact-active-class="active">
      <span class="material-symbols-outlined nav-icon">add_circle</span>
      <span class="nav-label">Crear</span>
    </RouterLink>
    <RouterLink to="/reports" class="nav-item" exact-active-class="active">
      <span class="material-symbols-outlined nav-icon">bar_chart</span>
      <span class="nav-label">Reportes</span>
    </RouterLink>
  </nav>
</template>

<style scoped>
.bottom-navigation {
  display: flex;
  justify-content: space-around;
  align-items: center;
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 70px;
  background-color: var(--color-white);
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.05);
  z-index: 100;
  padding-bottom: env(safe-area-inset-bottom);
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  color: var(--text-gray);
  text-decoration: none;
  flex: 1;
  height: 100%;
  transition: color 0.2s;
}

.nav-icon {
  font-size: 1.5rem;
}

.nav-label {
  font-size: 0.65rem;
  font-weight: 500;
}

.nav-item.active {
  color: var(--color-primary);
}

.nav-item.active .nav-icon {
  font-variation-settings: 'FILL' 1;
}

@media (min-width: 769px) {
  .bottom-navigation {
    display: none;
  }
}
</style>
