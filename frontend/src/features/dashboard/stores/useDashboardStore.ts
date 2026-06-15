import { defineStore } from 'pinia'
import { ref } from 'vue'
import { analyticsApi } from '../../../shared/api/analytics.api'

export const useDashboardStore = defineStore('dashboard', () => {
  const dashboardData = ref<any>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchDashboard = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await analyticsApi.getDashboard()
      dashboardData.value = response.data
    } catch (err: any) {
      error.value = err.message || 'Error fetching dashboard data'
    } finally {
      loading.value = false
    }
  }

  return {
    dashboardData,
    loading,
    error,
    fetchDashboard
  }
})
