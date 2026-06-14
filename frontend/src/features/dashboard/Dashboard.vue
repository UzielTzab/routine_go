<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiClient } from '../../shared/api/client'

const healthStatus = ref<string>('Loading...')

onMounted(async () => {
  try {
    const response = await apiClient.get('/health/')
    healthStatus.value = JSON.stringify(response.data, null, 2)
  } catch (error: any) {
    healthStatus.value = `Error connecting to API: ${error.message}`
  }
})
</script>

<template>
  <div>
    <h1>API Health Status</h1>
    <pre>{{ healthStatus }}</pre>
  </div>
</template>
