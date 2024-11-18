import Vue from 'vue'
import VueRouter from 'vue-router'
import FirstPageView from '../views/firstPage.vue'
import SecondPageView from '../views/secondPage.vue'
import MainPageView from '../views/mainPage.vue'
// import { component } from 'vue/types/umd'

Vue.use(VueRouter)

const routes = [
  {
    path: '/firstPage',
    component: FirstPageView
  },
  {
    path: '/secondPage',
    // component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
    component: SecondPageView
  },
  {
    path: '/',
    component: MainPageView
  }
]

const router = new VueRouter({
  routes
})

export default router
