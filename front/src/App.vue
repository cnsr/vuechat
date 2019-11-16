<template>
  <div id="app">
    <div id="nav">
      <md-app>
        <md-app-toolbar class="md-primary">
          <md-tabs class="md-primary" md-alignment="right" md-sync-route>
            <md-tab id="tab-home" md-label="Home" to='/'>
            </md-tab>
            <md-tab id="tab-settings" md-label="Settings" to='/settings'>
            </md-tab>
          </md-tabs>
        </md-app-toolbar>
      </md-app>
      <label id='usercount'>Users online: {{ getUsercount }}</label>
      <router-view/>
    </div>
  </div>
</template>

<script>
import Chat from './components/Chat.vue';
import Settings from './components/Settings.vue';
import Message from './components/Message.vue';
import { mapState, mapGetters } from 'vuex';

export default {
  name: 'App',
  data () {
    return {
      menuVisible: false
    }
  },
  computed: {
    ...mapState(['usercount']),
    ...mapGetters(['getUsercount'])
  },
  components: {
    'Chat': Chat,
    'Settings': Settings,
    'Message': Message,
  },
  methods: {
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

#nav a {
  font-weight: bold;
  color: #2c3e50;
  padding-right: 5px;
  padding-left: 50px;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
.md-app {
  display: block;
}
</style>
