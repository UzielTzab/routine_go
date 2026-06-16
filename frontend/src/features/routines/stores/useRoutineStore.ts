import { defineStore } from 'pinia'
import { ref } from 'vue'
import { routinesApi } from '../../../shared/api/routines.api'

export const useRoutineStore = defineStore('routine', () => {
  const categories = ref<any[]>([])
  const loadingCategories = ref(false)
  const errorCategories = ref<string | null>(null)

  const loadingCreate = ref(false)
  const errorCreate = ref<string | null>(null)
  const createSuccess = ref(false)

  const fetchCategories = async () => {
    loadingCategories.value = true
    errorCategories.value = null
    try {
      const response = await routinesApi.getCategories()
      categories.value = response.data
    } catch (err: any) {
      errorCategories.value = err.message || 'Error fetching categories'
    } finally {
      loadingCategories.value = false
    }
  }

  const createRoutine = async (routineData: any) => {
    loadingCreate.value = true
    errorCreate.value = null
    createSuccess.value = false
    try {
      await routinesApi.createTemplate(routineData)
      createSuccess.value = true
    } catch (err: any) {
      errorCreate.value = err.message || 'Error creating routine'
      throw err
    } finally {
      loadingCreate.value = false
    }
  }

  const deleteRoutine = async (id: string) => {
    try {
      await routinesApi.deleteTemplate(id)
    } catch (err: any) {
      throw err
    }
  }

  const updateRoutine = async (id: string, routineData: any) => {
    try {
      await routinesApi.updateTemplate(id, routineData)
    } catch (err: any) {
      throw err
    }
  }

  return {
    categories,
    loadingCategories,
    errorCategories,
    loadingCreate,
    errorCreate,
    createSuccess,
    fetchCategories,
    createRoutine,
    deleteRoutine,
    updateRoutine
  }
})
