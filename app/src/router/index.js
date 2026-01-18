import { createRouter, createWebHistory } from 'vue-router'
import Debug from '../pages/Debug.vue'

const routes = [
  {
    path: '/debug',
    name: 'Debug',
    component: Debug
  },
  {
    path: '/',
    redirect: '/debug'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
