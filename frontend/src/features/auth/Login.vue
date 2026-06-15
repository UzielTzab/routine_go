<script setup lang="ts">
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import BaseInput from '../../shared/components/BaseInput.vue'
import BaseButton from '../../shared/components/BaseButton.vue'
import BaseSwitch from '../../shared/components/BaseSwitch.vue'
import { useAuthStore } from './stores/useAuthStore'

const authStore = useAuthStore()
const { loading, error } = storeToRefs(authStore)

const email = ref('')
const password = ref('')
const rememberMe = ref(false)

const handleLogin = async () => {
  if (!email.value || !password.value) return
  await authStore.login({ email: email.value, password: password.value })
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
          Focus on what<br/>moves you forward.
        </h2>
        <p class="overlay-subtitle">
          Build better routines, track your progress, and<br/>perform at your best every day.
        </p>
      </div>

      <img src="/images/login_left_background.png" alt="Welcome Back Background" class="auth-bg-image" />
    </div>

    <!-- Right Panel: Form -->
    <div class="auth-right-panel">
      <div class="form-container">
        <div class="form-header">
          <div class="icon-circle">
            <span class="material-symbols-outlined">lock</span>
          </div>
          <h1 class="auth-title">Welcome Back</h1>
          <p class="auth-subtitle">Sign in to continue your journey.</p>
        </div>

        <form @submit.prevent="handleLogin" class="auth-form">
          <div v-if="error" class="error-banner">
            {{ error }}
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

          <div class="form-options">
            <BaseSwitch v-model="rememberMe" label="Remember me" />
            <a href="#" class="forgot-password">Forgot password?</a>
          </div>

          <BaseButton 
            type="submit" 
            variant="primary" 
            class="submit-btn"
            :disabled="loading"
          >
            <span v-if="loading" class="material-symbols-outlined spin icon-small">sync</span>
            <span v-else class="material-symbols-outlined icon-small">check_circle</span>
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </BaseButton>

          <div class="divider">
            <span>or</span>
          </div>

          <p class="auth-footer">
            Don't have an account? <router-link to="/signup" class="auth-link">Sign up</router-link>
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
  background-color: var(--color-white); /* Right panel background */
  overflow: hidden;
}

.auth-left-panel {
  flex: 1;
  position: relative;
  background-color: #E2DEFB; /* A soft purple if image doesn't cover entirely */
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
  top: 25%;
  left: 0;
  width: 100%;
  text-align: center;
  z-index: 10;
  padding: 0 2rem;
}

.overlay-title {
  font-size: 3rem;
  font-weight: 800;
  color: #2D3748; /* Dark gray/black matching design */
  line-height: 1.1;
  margin: 0 0 1rem 0;
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
  background-color: #F8F9FD; /* Match the slightly grayish background from the right panel in figma */
}

.form-container {
  width: 100%;
  max-width: 480px;
  background-color: var(--color-white);
  padding: 3rem;
  border-radius: var(--radius-xl);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.05);
}

.form-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2.5rem;
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
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.error-banner {
  padding: 1rem;
  background-color: var(--bg-status-danger);
  color: var(--status-expired);
  border-radius: var(--radius-md);
  font-size: 0.9rem;
  font-weight: 600;
  text-align: center;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: -0.5rem;
}

.forgot-password {
  color: var(--color-primary);
  font-size: 0.85rem;
  font-weight: 600;
  text-decoration: none;
}

.submit-btn {
  width: 100%;
  justify-content: center;
  padding: 0.85rem;
  font-size: 1rem;
  border-radius: var(--radius-md);
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

/* Responsive adjustments */
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
