import { defineStore } from 'pinia'
import { ref } from 'vue'
import { analyticsApi } from '../../../shared/api/analytics.api'

export const useAnalyticsStore = defineStore('analytics', () => {
  const reportsData = ref<any>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchReports = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await analyticsApi.getReports()
      reportsData.value = response.data
    } catch (err: any) {
      error.value = err.message || 'Error fetching reports'
    } finally {
      loading.value = false
    }
  }

  return {
    reportsData,
    loading,
    error,
    fetchReports
  }
})
