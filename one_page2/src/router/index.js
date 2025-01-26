import Vue from 'vue'
import VueRouter from 'vue-router'
import testVuePageView from '../views/testVuePage.vue'
import djangoAnimePageView from '../views/djangoAnimePage.vue'
import startMapPageView from '../views/startMapPage.vue'
import testMapPageView from '../views/testMapPage.vue'
// import { component } from 'vue/types/umd'

Vue.use(VueRouter)

const routes = [
  {
    path: '/firstPage',
    component: testVuePageView
  },
  {
    path: '/secondPage',
    component: djangoAnimePageView
  },
  {
    path: '/',
    component: startMapPageView
  },
  {
    path: '/1',
    component: testMapPageView
  }
]

const router = new VueRouter({
  routes
})

export default router
