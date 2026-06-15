import { defineStore } from 'pinia'
import { ref } from 'vue'
import { scheduleApi } from '../../../shared/api/schedule.api'
import { executionsApi } from '../../../shared/api/executions.api'
import { useToast } from '../../../shared/composables/useToast'

export const useScheduleStore = defineStore('schedule', () => {
  const todaySchedule = ref<any[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const { addToast } = useToast()

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

  const extractError = (err: any) => {
    if (err.response?.data) {
      if (Array.isArray(err.response.data) && err.response.data[0]) {
        return err.response.data[0]
      }
      if (err.response.data.detail) return err.response.data.detail
      if (typeof err.response.data === 'string') return err.response.data
    }
    return err.message
  }

  const startExecution = async (uuid: string) => {
    try {
      await executionsApi.start(uuid)
      addToast('Rutina iniciada', 'success')
      await fetchToday()
    } catch (err: any) {
      addToast(extractError(err) || 'Error al iniciar', 'error')
    }
  }

  const completeExecution = async (uuid: string) => {
    try {
      await executionsApi.complete(uuid)
      addToast('Rutina completada con éxito', 'success')
      await fetchToday()
    } catch (err: any) {
      addToast(extractError(err) || 'Error al completar', 'error')
    }
  }
  
  const skipExecution = async (uuid: string) => {
    try {
      await executionsApi.omit(uuid)
      addToast('Rutina omitida', 'info')
      await fetchToday()
    } catch (err: any) {
      addToast(extractError(err) || 'Error al omitir', 'error')
    }
  }

  const snoozeExecution = async (uuid: string) => {
    try {
      await executionsApi.snooze(uuid)
      addToast('Rutina pospuesta 15 minutos', 'info')
      await fetchToday()
    } catch (err: any) {
      addToast(extractError(err) || 'Error al posponer', 'error')
    }
  }

  return {
    todaySchedule,
    loading,
    error,
    fetchToday,
    startExecution,
    completeExecution,
    skipExecution,
    snoozeExecution
  }
})
