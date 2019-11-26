<template>
  <div id="app">
    <div id="nav">
      <md-app>
        <md-app-toolbar class="md-primary md-dense">
          <md-tabs class="md-primary" md-alignment="right" md-sync-route>
            <md-tab id="tab-home" md-label="Home" to='/'>
            </md-tab>
            <md-tab id="tab-settings" md-label="Settings" to='/settings'>
            </md-tab>
          </md-tabs>
          <div class='md-toolbar-section-end'>
            <md-button v-on:click="toggleUserlist" class='md-small'>{{ getUsercount }}</md-button>
          </div>
        </md-app-toolbar>
      </md-app>
      <router-view/>
    </div>
    <md-card class='userlist' v-show="active">
      <md-card-header>
          <div class="md-title">List of users online</div>
      </md-card-header>
      <md-card-content>
        <p>Nothing to see here</p>
      </md-card-content>
    </md-card>
  </div>
</template>

<script>
import Chat from './components/Chat.vue';
import Settings from './components/Settings.vue';
import Message from './components/Message.vue';
import Snack from './components/Snack.vue';
import { mapState, mapGetters } from 'vuex';

export default {
  name: 'App',
  data () {
    return {
      active: false,
    }
  },
  computed: {
    ...mapState(['usercount', 'userlist']),
    ...mapGetters(['getUsercount', 'getUserlist'])
  },
  components: {
    'Chat': Chat,
    'Settings': Settings,
    'Message': Message,
    'Snack': Snack,
  },
  methods: {
    isMobile() {
      if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        return true
      } else {
        return false
      }
    },
    toggleUserlist() {
      this.active = !this.active;
    },
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100vh;
  min-height: 100vh;
  max-height: 100vh;
}

.userlist {
  display: block;
  position: fixed;
  right: 0;
  top: 5%;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
  padding-right: 5px;
  padding-left: 5px;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
.md-app {
  display: block;
}
.snackbar {
  display: block;
  position: relative;
}
</style>
