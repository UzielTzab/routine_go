<script setup lang="ts">
defineProps({
  category: {
    type: String,
    required: true,
    validator: (value: string) => ['hygiene', 'exercise', 'focus', 'nutrition', 'sleep'].includes(value)
  },
  label: {
    type: String,
    required: true
  },
  progress: {
    type: Number,
    required: true,
    default: 0
  },
  icon: {
    type: String,
    required: false
  }
})

const getCategoryColor = (cat: string) => {
  const map: Record<string, string> = {
    hygiene: 'var(--color-hygiene)',
    exercise: 'var(--color-exercise)',
    focus: 'var(--color-focus)',
    nutrition: 'var(--color-nutrition)',
    sleep: 'var(--color-sleep)',
  }
  return map[cat] || 'var(--text-primary)'
}
</script>

<template>
  <div class="metric-item">
    <div class="circular-progress" :style="{ '--progress-color': getCategoryColor(category), '--progress': progress }">
      <div class="inner-circle">
        <img v-if="icon" :src="icon" :alt="label" class="icon-img" />
      </div>
    </div>
    <div class="metric-info">
      <span class="metric-label">{{ label }}</span>
      <span class="metric-value">{{ progress }}%</span>
    </div>
  </div>
</template>

<style scoped>
.metric-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2);
}

.circular-progress {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: conic-gradient(
    var(--progress-color) calc(var(--progress) * 1%), 
    var(--bg-app) 0
  );
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.inner-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: var(--color-white);
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-img {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.metric-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-1);
}

.metric-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-primary);
}

.metric-value {
  font-size: 0.8rem;
  color: var(--text-gray);
}
</style>
