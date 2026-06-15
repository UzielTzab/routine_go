import { ref } from 'vue'

export type ToastType = 'success' | 'error' | 'info'

export interface Toast {
  id: number
  message: string
  type: ToastType
}

const toasts = ref<Toast[]>([])
let nextId = 0

export const useToast = () => {
  const addToast = (message: string, type: ToastType = 'info', duration = 3000) => {
    const id = nextId++
    toasts.value.push({ id, message, type })
    setTimeout(() => {
      removeToast(id)
    }, duration)
  }

  const removeToast = (id: number) => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }

  return {
    toasts,
    addToast,
    removeToast
  }
}
