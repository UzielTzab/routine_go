<script setup lang="ts">
defineProps({
  title: {
    type: String,
    required: false,
    default: ''
  },
  padding: {
    type: String,
    required: false,
    default: '1.5rem'
  }
})
</script>

<template>
  <div class="base-card" :style="{ padding }">
    <div v-if="title || $slots.header" class="card-header">
      <h3 v-if="title" class="card-title">{{ title }}</h3>
      <slot name="header"></slot>
    </div>
    <div class="card-content">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
.base-card {
  background-color: var(--surface-card);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-card);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  color: var(--text-gray);
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.card-content {
  flex-grow: 1;
}
</style>
