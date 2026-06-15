<script setup lang="ts">
import { ref, computed } from 'vue'
import BaseCard from '../../shared/components/BaseCard.vue'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { Line, Bar } from 'vue-chartjs'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

// Line Chart Data (Weekly Progress)
const lineData = {
  labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
  datasets: [
    {
      label: 'Minutos Productivos',
      backgroundColor: 'rgba(184, 183, 255, 0.2)', // Using primary color with opacity
      borderColor: '#B8B7FF', // var(--color-primary)
      data: [120, 210, 150, 300, 250, 400, 320],
      fill: true,
      tension: 0.4, // smooth curve
      pointRadius: 0,
      borderWidth: 3
    }
  ]
}

const lineOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: { mode: 'index', intersect: false } as any
  },
  scales: {
    y: { display: false, beginAtZero: true },
    x: {
      grid: { display: false, drawBorder: false },
      ticks: { color: '#717171', font: { family: 'Inter', size: 12 } } // var(--text-gray)
    }
  }
}

// Streak History (GitHub style contribution graph)
// 90 days = ~13 weeks
const streakDays = ref(Array.from({ length: 90 }, (_, i) => {
  // Randomly assign a level from 0 to 4 to simulate activity
  return Math.floor(Math.random() * 5);
}))

const getStreakColor = (level: number) => {
  const colors = ['#E9E9FB', '#C6C5FA', '#9C9BFA', '#7674FA', '#3A3B51'] 
  // From var(--bg-app) up to var(--sidebar-bg) for high intensity
  return colors[level] || colors[0];
}

// Hourly Compliance (Bar Chart)
const hourlyData = {
  labels: ['6a', '8a', '10a', '12p', '2p', '4p', '6p', '8p', '10p'],
  datasets: [
    {
      backgroundColor: '#C6C5FA',
      borderRadius: 4,
      data: [20, 40, 70, 85, 60, 45, 90, 50, 15],
      barPercentage: 0.6
    }
  ]
}

const hourlyOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    y: { display: false, beginAtZero: true },
    x: { display: false }
  }
}

// Sleep vs Focus (Stacked Bar Chart)
const stackedData = {
  labels: ['Hoy', 'Ayer', 'Jue', 'Mié'],
  datasets: [
    {
      label: 'Sueño',
      backgroundColor: '#6462EC', // var(--color-focus) wait, sleep is #6576A6 but the image shows purple for both?
      // Actually image legend: Sueño (Purple), Foco (Dark Blue). I will use #6462EC for sleep and #3A3B51 for Focus to match image style
      data: [8, 7, 6.5, 7.5],
      borderRadius: { topLeft: 10, bottomLeft: 10, topRight: 0, bottomRight: 0 },
      borderSkipped: false,
      barThickness: 12
    },
    {
      label: 'Foco',
      backgroundColor: '#3A3B51', // Dark sidebar color for contrast
      data: [4, 5, 3.5, 4.5],
      borderRadius: { topLeft: 0, bottomLeft: 0, topRight: 10, bottomRight: 10 },
      borderSkipped: false,
      barThickness: 12
    }
  ]
}

const stackedOptions = {
  responsive: true,
  maintainAspectRatio: false,
  indexAxis: 'y' as const, // Horizontal bar chart
  plugins: {
    legend: { display: false } // Custom legend in HTML
  },
  scales: {
    x: { display: false, stacked: true },
    y: { 
      stacked: true, 
      grid: { display: false, drawBorder: false },
      ticks: { color: '#717171', font: { family: 'Inter', size: 12 } }
    }
  }
}

</script>

<template>
  <div class="reports-page">
    <header class="page-header">
      <h1 class="greeting">Reportes de Rendimiento</h1>
      <p class="subtitle">Análisis detallado de tu tiempo y enfoque semanal.</p>
    </header>

    <!-- Main Chart -->
    <BaseCard class="main-chart-card" padding="2rem">
      <div class="chart-header">
        <div class="chart-title-group">
          <h3 class="card-title">Progreso Semanal</h3>
          <p class="card-subtitle">Minutos productivos registrados</p>
        </div>
        <div class="chart-metric">
          <span class="metric-value">2,450</span>
          <span class="metric-unit">min</span>
        </div>
      </div>
      <div class="chart-container-large">
        <Line :data="lineData" :options="lineOptions" />
      </div>
    </BaseCard>

    <!-- Streak History -->
    <BaseCard class="streak-card" padding="1.5rem 2rem">
      <div class="chart-header">
        <div class="chart-title-group">
          <h3 class="card-title">Historial de Rachas</h3>
          <p class="card-subtitle">Consistencia diaria últimos 90 días</p>
        </div>
        <span class="material-symbols-outlined icon-small">local_fire_department</span>
      </div>
      <div class="streak-grid">
        <div 
          v-for="(day, index) in streakDays" 
          :key="index"
          class="streak-day"
          :style="{ backgroundColor: getStreakColor(day) }"
          :title="`Nivel: ${day}`"
        ></div>
      </div>
    </BaseCard>

    <!-- Bottom Row (Two Columns) -->
    <div class="bottom-row">
      <!-- Hourly Compliance -->
      <BaseCard class="hourly-card" padding="1.5rem 2rem">
        <div class="chart-title-group mb-4">
          <h3 class="card-title">Cumplimiento por Hora</h3>
          <p class="card-subtitle">Intensidad de actividad promedio</p>
        </div>
        <div class="chart-container-small">
          <Bar :data="hourlyData" :options="hourlyOptions" />
        </div>
      </BaseCard>

      <!-- Sleep vs Focus -->
      <BaseCard class="stacked-card" padding="1.5rem 2rem">
        <div class="chart-header mb-4">
          <div class="chart-title-group">
            <h3 class="card-title">Sueño vs Foco</h3>
            <p class="card-subtitle">Correlación de rendimiento</p>
          </div>
          <div class="custom-legend">
            <span class="legend-item"><span class="dot" style="background-color: #6462EC"></span> Sueño</span>
            <span class="legend-item"><span class="dot" style="background-color: #3A3B51"></span> Foco</span>
          </div>
        </div>
        <div class="chart-container-small">
          <Bar :data="stackedData" :options="stackedOptions" />
        </div>
      </BaseCard>
    </div>
  </div>
</template>

<style scoped>
.reports-page {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
  padding-bottom: var(--space-8);
}

.page-header {
  margin-bottom: var(--space-2);
}

.greeting {
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 var(--space-1) 0;
  color: var(--text-primary);
}

.subtitle {
  color: var(--text-gray);
  font-size: 1rem;
  margin: 0;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.chart-title-group {
  display: flex;
  flex-direction: column;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 700;
  margin: 0 0 4px 0;
  color: var(--text-primary);
}

.card-subtitle {
  font-size: 0.85rem;
  color: var(--text-gray);
  margin: 0;
}

.chart-metric {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.metric-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-focus); /* Dark purple based on image */
}

.metric-unit {
  font-size: 0.9rem;
  color: var(--text-gray);
  font-weight: 600;
}

.chart-container-large {
  position: relative;
  height: 250px;
  width: 100%;
  margin-top: var(--space-4);
}

.streak-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(12px, 1fr));
  gap: 4px;
  margin-top: var(--space-6);
  padding-bottom: var(--space-2);
}

.streak-day {
  width: 100%;
  aspect-ratio: 1;
  border-radius: 2px;
}

.bottom-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-6);
}

.chart-container-small {
  position: relative;
  height: 150px;
  width: 100%;
}

.mb-4 {
  margin-bottom: var(--space-4);
}

.icon-small {
  color: var(--text-gray);
}

.custom-legend {
  display: flex;
  gap: var(--space-4);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
  color: var(--text-primary);
  font-weight: 600;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
</style>
