import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '../../features/dashboard/Dashboard.vue';

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Dashboard,
    },
  ],
});
