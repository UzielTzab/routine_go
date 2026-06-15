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

  const startExecution = async (uuid: string) => {
    try {
      await executionsApi.start(uuid)
      addToast('Rutina iniciada', 'success')
      await fetchToday()
    } catch (err: any) {
      addToast(err.message || 'Error al iniciar', 'error')
    }
  }

  const completeExecution = async (uuid: string) => {
    try {
      await executionsApi.complete(uuid)
      addToast('Rutina completada con éxito', 'success')
      await fetchToday()
    } catch (err: any) {
      addToast(err.message || 'Error al completar', 'error')
    }
  }
  
  const skipExecution = async (uuid: string) => {
    try {
      await executionsApi.omit(uuid)
      addToast('Rutina omitida', 'info')
      await fetchToday()
    } catch (err: any) {
      addToast(err.message || 'Error al omitir', 'error')
    }
  }

  const snoozeExecution = async (uuid: string) => {
    try {
      await executionsApi.snooze(uuid)
      addToast('Rutina pospuesta 15 minutos', 'info')
      await fetchToday()
    } catch (err: any) {
      addToast(err.message || 'Error al posponer', 'error')
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
