import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authApi } from '../../../shared/api/auth.api'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const loading = ref(false)
  const error = ref<string | null>(null)
  const storedUser = localStorage.getItem('user')
  const user = ref<{ name: string; email: string } | null>(storedUser ? JSON.parse(storedUser) : null)
  const router = useRouter()

  const login = async (credentials: { email: string; password: string }) => {
    loading.value = true
    error.value = null
    try {
      const response = await authApi.login(credentials)
      
      // Save user from response or fallback to email
      const userData = {
        name: response.data?.user?.name || credentials.email.split('@')[0],
        email: response.data?.user?.email || credentials.email
      }
      user.value = userData
      
      localStorage.setItem('isAuthenticated', 'true')
      localStorage.setItem('user', JSON.stringify(userData))
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
      localStorage.removeItem('user')
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
