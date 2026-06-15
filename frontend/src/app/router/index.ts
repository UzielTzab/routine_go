import { createRouter, createWebHistory } from 'vue-router';
import DashboardLayout from '../layouts/DashboardLayout.vue';
import Dashboard from '../../features/dashboard/Dashboard.vue';
import Agenda from '../../features/schedule/Agenda.vue';
import ActiveRoutine from '../../features/routines/ActiveRoutine.vue';
import CreateRoutine from '../../features/routines/CreateRoutine.vue';
import Reports from '../../features/analytics/Reports.vue';

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: DashboardLayout,
      children: [
        {
          path: '',
          name: 'home',
          component: Dashboard,
        },
        {
          path: 'agenda',
          name: 'agenda',
          component: Agenda,
        },
        {
          path: 'active-routine',
          name: 'activeRoutine',
          component: ActiveRoutine,
        },
        {
          path: 'create-routine',
          name: 'createRoutine',
          component: CreateRoutine,
        },
        {
          path: 'reports',
          name: 'reports',
          component: Reports,
        }
      ]
    },
  ],
});
