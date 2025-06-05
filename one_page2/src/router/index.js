import Vue from 'vue';
import VueRouter from 'vue-router';

import MapPageView from '@/views/mapPage.vue';
import LoginForm from '@/views/loginFormPage.vue';
import RegisterForm from '@/views/registerFormPage.vue';
import AccountPageView from '@/views/accountPage.vue';

Vue.use(VueRouter);

// Simple helper to check if user is authenticated (checks localStorage token)
const isAuthenticated = () => !!localStorage.getItem('authToken');

const routes = [
  {
    path: '/map',
    component: MapPageView,
    meta: { requiresAuth: true }  // Requires authentication
  },
  {
    path: '/login',
    component: LoginForm
  },
  {
    path: '/register',
    component: RegisterForm
  },
  {
    path: '/account',
    component: AccountPageView,
    meta: { requiresAuth: true }  // Requires authentication
  },
];

const router = new VueRouter({
  routes
});

// Navigation guard to redirect unauthenticated users to login page if route requires auth
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated()) {
    next('/login');
  } else {
    next();
  }
});

export default router;
