import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authApi } from '../../../shared/api/auth.api'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const loading = ref(false)
  const error = ref<string | null>(null)
  const user = ref<{ name: string; email: string } | null>(null)
  const router = useRouter()

  const login = async (credentials: { email: string; password: string }) => {
    loading.value = true
    error.value = null
    try {
      const response = await authApi.login(credentials)
      
      // Save user from response or fallback to email
      user.value = {
        name: response.data?.user?.name || credentials.email.split('@')[0],
        email: response.data?.user?.email || credentials.email
      }
      
      localStorage.setItem('isAuthenticated', 'true')
      router.push('/')
    } catch (err: any) {
      error.value = err.response?.data?.detail || err.message || 'Error al iniciar sesión'
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    try {
      await authApi.logout()
    } catch (e) {
      console.error(e)
    } finally {
      user.value = null
      localStorage.removeItem('isAuthenticated')
      router.push('/login')
    }
  }

  return {
    loading,
    error,
    user,
    login,
    logout
  }
})
