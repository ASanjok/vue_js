import Vue from 'vue'
import VueRouter from 'vue-router'
import testVuePageView from '../views/testVuePage.vue'
import djangoAnimePageView from '../views/djangoAnimePage.vue'
import MapPageView from '../views/mainMapPage.vue'
// import { component } from 'vue/types/umd'

Vue.use(VueRouter)

const routes = [
  {
    path: '/firstPage',
    component: testVuePageView
  },
  {
    path: '/secondPage',
    // component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
    component: djangoAnimePageView
  },
  {
    path: '/',
    component: MapPageView
  }
]

const router = new VueRouter({
  routes
})

export default router
