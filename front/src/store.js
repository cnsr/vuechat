import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    uid: '',
    admin: false,
    socket: {
      isConnected: false,
      message: '',
      reconnectError: false,
      usercount: 0,
    },
    messagesCache: [],
    error: '',
  },
  getters: {
    getUsercount: state => {
      return state.socket.usercount;
    },
    getMessages: state => {
      return state.messagesCache;
    },
    getAdmin: state => {
      return state.admin;
    },
    getUID: state => {
      return state.uid;
    }
  },
  mutations: {
    SOCKET_ONOPEN(state, event) {
      Vue.prototype.$socket = event.currentTarget;
      state.socket.isConnected = true;
    },
    SOCKET_ONCLOSE(state, event) {
      state.socket.isConnected = false;
    },
    SOCKET_ONMESSAGE(state, message) {
      console.log(message);
      switch (message.type) {
        case 'uid':
          state.uid = message.uid;
        case 'setadmin':
          state.admin = message.admin;
          if (message.admin)
            document.getElementById('adminfloater').remove();
          else {
            Vue.prototype.$snack.danger({
              text: 'Wrong password',
            });
          }
        case 'count':
          state.socket.usercount = message.usercount;
          break;
        case 'message':
          state.messagesCache.push(message);
          break;
        case 'cached':
          state.messagesCache = [...message.cache];
          break;
        case 'remove':
          state.messagesCache = state.messagesCache.filter(m => m.count != message.count);
          break;
        case 'error':
          Vue.prototype.$snack.danger({
            text: message.text,
          });
          break;
        default:
          console.log(message);
          break;
      };
      state.socket.message = message;
    },
    SOCKET_ONERROR(state, event) {
      console.error(state, event);
    },
    SOCKET_RECONNECT(state, count) {
      console.info(state, count);
    },
    SOCKET_RECONNECT_ERROR(state) {
      state.socket.reconnectError = true;
    }
  },
  actions: {
    sendMessage: function(context, message) {
      Vue.prototype.$socket.sendObj(message);
    }
  }
});
