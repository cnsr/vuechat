import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    socket: {
      isConnected: false,
      message: '',
      reconnectError: false,
      usercount: 0,
    },
    messagesCache: [],
  },
  getters: {
    getUsercount: state => {
      return state.socket.usercount;
    },
    getMessages: state => {
      return state.messagesCache;
    },
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
