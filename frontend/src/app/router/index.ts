import { createRouter, createWebHistory } from 'vue-router';
import DashboardLayout from '../layouts/DashboardLayout.vue';
import Dashboard from '../../features/dashboard/Dashboard.vue';
import Agenda from '../../features/schedule/Agenda.vue';
import ActiveRoutine from '../../features/routines/ActiveRoutine.vue';
import CreateRoutine from '../../features/routines/CreateRoutine.vue';
import Reports from '../../features/analytics/Reports.vue';
import Login from '../../features/auth/Login.vue';
import SignUp from '../../features/auth/SignUp.vue';

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUp
    },
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

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true'
  const isAuthRoute = to.path === '/login' || to.path === '/signup'

  if (!isAuthenticated && !isAuthRoute) {
    next('/login')
  } else if (isAuthenticated && isAuthRoute) {
    next('/')
  } else {
    next()
  }
})
