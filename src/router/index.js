import Vue from 'vue'
import VueRouter from 'vue-router'
import FirstPageView from '../views/firstPage.vue'
import SecondPageView from '../views/secondPage.vue'
// import { component } from 'vue/types/umd'

Vue.use(VueRouter)

const routes = [
  {
    path: '/firstPage',
    name: 'home',
    component: FirstPageView
  },
  {
    path: '/secondPage',
    name: 'about',
    // component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
    component: SecondPageView
  }
]

const router = new VueRouter({
  routes
})

export default router
