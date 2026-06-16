<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import BaseInput from '../../shared/components/BaseInput.vue'
import BaseButton from '../../shared/components/BaseButton.vue'

import { authApi } from '../../shared/api/auth.api'

const router = useRouter()
const loading = ref(false)

const nombre = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const agreeTerms = ref(false)

const handleSignUp = async () => {
  if (password.value !== confirmPassword.value) {
    alert("Las contraseñas no coinciden")
    return
  }
  if (!agreeTerms.value) {
    alert("Debes aceptar los términos")
    return
  }
  
  loading.value = true
  try {
    await authApi.register({
      name: nombre.value,
      email: email.value,
      password: password.value
    })
    alert('Cuenta creada exitosamente. Por favor, inicia sesión.')
    router.push('/login')
  } catch (error: any) {
    alert(error.response?.data?.detail || 'Error al registrar')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-layout">
    <!-- Left Panel: Background Image and Logo -->
    <div class="auth-left-panel">
      <div class="logo-container">
        <img src="/images/routine_go_logo.png" alt="Routine GO Logo" class="auth-logo" />
      </div>
      
      <div class="auth-text-overlay">
        <h2 class="overlay-title">
          Build a better routine.<br/>
          <span class="text-primary">Become your best self.</span>
        </h2>
        <p class="overlay-subtitle">
          Join Routine GO and take control of your habits,<br/>focus, and daily progress.
        </p>
      </div>

      <img src="/images/sign_up_left_background.png" alt="Create Account Background" class="auth-bg-image" />
    </div>

    <!-- Right Panel: Form -->
    <div class="auth-right-panel">
      <div class="form-container">
        <div class="form-header">
          <div class="icon-circle">
            <span class="material-symbols-outlined">person_add</span>
          </div>
          <h1 class="auth-title">Create Account</h1>
          <p class="auth-subtitle">Start your journey to a better every day.</p>
        </div>

        <form @submit.prevent="handleSignUp" class="auth-form">
          <div class="form-group">
            <BaseInput 
              v-model="nombre"
              type="text"
              label="Nombre"
              placeholder="Your name"
            />
          </div>

          <div class="form-group">
            <BaseInput 
              v-model="email"
              type="email"
              label="Email address"
              placeholder="you@example.com"
              icon="mail"
            />
          </div>

          <div class="form-group">
            <BaseInput 
              v-model="password"
              type="password"
              label="Password"
              placeholder="••••••••••••"
              icon="visibility_off"
            />
          </div>

          <div class="form-group">
            <BaseInput 
              v-model="confirmPassword"
              type="password"
              label="Confirm Password"
              placeholder="••••••••••••"
              icon="visibility_off"
            />
          </div>

          <div class="form-options">
            <label class="checkbox-label">
              <input type="checkbox" v-model="agreeTerms" class="custom-checkbox" />
              <span>I agree to the <a href="#" class="auth-link">Terms</a> & <a href="#" class="auth-link">Privacy Policy</a></span>
            </label>
          </div>

          <BaseButton 
            type="submit" 
            variant="primary" 
            class="submit-btn"
            :disabled="loading"
          >
            <span v-if="loading" class="material-symbols-outlined spin icon-small">sync</span>
            <span v-else class="material-symbols-outlined icon-small">check_circle</span>
            {{ loading ? 'Creating...' : 'Sign Up' }}
          </BaseButton>

          <div class="divider">
            <span>or</span>
          </div>

          <p class="auth-footer">
            Already have an account? <router-link to="/login" class="auth-link">Sign in</router-link>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  background-color: var(--color-white);
  overflow: hidden;
}

.auth-left-panel {
  flex: 1;
  position: relative;
  background-color: #E2DEFB;
  display: flex;
  flex-direction: column;
}

.logo-container {
  position: absolute;
  top: 2rem;
  left: 2rem;
  z-index: 10;
}

.auth-logo {
  height: 48px;
  object-fit: contain;
}

.auth-bg-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1;
}

.auth-text-overlay {
  position: absolute;
  top: 15%;
  left: 0;
  width: 100%;
  z-index: 10;
  padding: 0 4rem;
  text-align: left;
}

.overlay-title {
  font-size: 2.8rem;
  font-weight: 800;
  color: #2D3748;
  line-height: 1.1;
  margin: 0 0 1rem 0;
}

.text-primary {
  color: var(--color-primary);
}

.overlay-subtitle {
  font-size: 1.1rem;
  color: #4A5568;
  line-height: 1.5;
  margin: 0;
}

.auth-right-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #F8F9FD;
}

.form-container {
  width: 100%;
  max-width: 480px;
  background-color: var(--color-white);
  padding: 3rem;
  border-radius: var(--radius-xl);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.05);
  max-height: 95vh;
  overflow-y: auto;
}

.form-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
  text-align: center;
}

.icon-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: #F0F0FA;
  color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.auth-title {
  font-size: 2rem;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.02em;
}

.auth-subtitle {
  color: var(--text-gray);
  font-size: 0.95rem;
  margin: 0;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-options {
  display: flex;
  margin-top: 0.25rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: var(--text-gray);
  cursor: pointer;
}

.custom-checkbox {
  width: 16px;
  height: 16px;
  accent-color: var(--color-primary);
  cursor: pointer;
}

.submit-btn {
  width: 100%;
  justify-content: center;
  padding: 0.85rem;
  font-size: 1rem;
  border-radius: var(--radius-md);
  margin-top: 0.5rem;
}

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: 1rem 0;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid var(--border-color);
}

.divider span {
  padding: 0 1rem;
  color: var(--text-gray);
  font-size: 0.85rem;
}

.auth-footer {
  text-align: center;
  font-size: 0.9rem;
  color: var(--text-gray);
  margin: 0;
}

.auth-link {
  color: var(--color-primary);
  font-weight: 600;
  text-decoration: none;
}

.spin {
  animation: spin 1s linear infinite;
}
@keyframes spin { 100% { transform: rotate(360deg); } }

@media (max-width: 900px) {
  .auth-left-panel {
    display: none;
  }
  .form-container {
    box-shadow: none;
    background-color: transparent;
  }
}
</style>
