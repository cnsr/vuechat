import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import Vuex from 'vuex';
import VueMaterial from 'vue-material';
import 'vue-material/dist/vue-material.css';
import 'vue-material/dist/theme/black-green-light.css';
import VueNativeSock from 'vue-native-websocket';

import App from './App.vue';
import router from './router';

// module imports
import { store } from './store';

import Chat from './components/Chat.vue';
import Settings from './components/Settings.vue';
import Message from './components/Message.vue';
import AdminPopup from './components/AdminPopup.vue';

import VueSnackbar from 'vue-snack' 
import 'vue-snack/dist/vue-snack.min.css'
import VueChatScroll from 'vue-chat-scroll';
//import Buefy from 'buefy';
//import 'buefy/dist/buefy.css'

Vue.use(BootstrapVue);
Vue.use(Vuex);
Vue.use(VueMaterial)
Vue.use(VueSnackbar, { position: 'top-right', time: 3000 })
Vue.use(VueChatScroll);
//Vue.use(Buefy);

Vue.config.productionTip = false;

Vue.use(VueNativeSock, 'ws://' + location.hostname + ':8000/websocket', {
  format: 'json',
  store: store,
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 3000,
});

new Vue({
  router,
  data: {
    newMessage: null,
    messages: [],
    username: null,
  },
  store,
  components: {
    'Chat': Chat,
    'Settings': Settings,
    'Message': Message,
    'AdminPopup': AdminPopup,
  },
  render: h => h(App),
}).$mount('#app');
