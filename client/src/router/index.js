import { createRouter, createWebHistory } from 'vue-router'
import { authGuard } from "@auth0/auth0-vue";

import AppView from '@/views/AppView.vue'
import App from '@/App.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
        path: '/app',
        name: 'app',
        component: AppView,
        beforeEnter: authGuard
    }
  ],
})

export default router