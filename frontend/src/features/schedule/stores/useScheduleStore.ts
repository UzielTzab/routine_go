import { defineStore } from 'pinia'
import { ref } from 'vue'
import { scheduleApi } from '../../../shared/api/schedule.api'

export const useScheduleStore = defineStore('schedule', () => {
  const todaySchedule = ref<any[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchToday = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await scheduleApi.getToday()
      todaySchedule.value = response.data
    } catch (err: any) {
      error.value = err.message || 'Error fetching today schedule'
    } finally {
      loading.value = false
    }
  }

  return {
    todaySchedule,
    loading,
    error,
    fetchToday
  }
})
