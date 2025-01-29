import Vue from 'vue';
import VueRouter from 'vue-router';
import testVuePageView from '../views/testVuePage.vue';
import djangoAnimePageView from '../views/djangoAnimePage.vue';
import startMapPageView from '../views/startMapPage.vue';
import testMapPageView from '../views/testMapPage.vue';
import LoginForm from '@/views/loginFormPage.vue';
import RegisterForm from '@/views/registerFormPage.vue';
import AccountPageView from '@/views/accountPage.vue';

Vue.use(VueRouter);

const isAuthenticated = () => !!localStorage.getItem('authToken');

const routes = [
  {
    path: '/',
    component: startMapPageView,
    meta: { requiresAuth: true }
  },
  {
    path: '/firstPage',
    component: testVuePageView,
    meta: { requiresAuth: true }
  },
  {
    path: '/secondPage',
    component: djangoAnimePageView,
    meta: { requiresAuth: true }
  },
  {
    path: '/1',
    component: testMapPageView,
    meta: { requiresAuth: true }
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
    meta: {requiresAuth: true}
  }
];

const router = new VueRouter({
  routes
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated()) {
    next('/login');
  } else {
    next();
  }
});

export default router;
