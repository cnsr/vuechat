import Vue from 'vue';
import VueRouter from 'vue-router';
import Chat from '../components/Chat.vue';
import Settings from '../components/Settings.vue';
Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Chat',
    component: Chat,
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
