<script setup lang="ts">
import { RouterView } from 'vue-router'
import ToastContainer from './shared/components/ToastContainer.vue'
</script>

<template>
  <main class="app-container">
    <RouterView />
    <ToastContainer />
  </main>
</template>
