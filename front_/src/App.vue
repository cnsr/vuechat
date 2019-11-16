<template>
  <div id="app">
    <div id="nav">
          <router-link to="/">Chatroom</router-link>
          <router-link to="/settings">Settings</router-link> 
    </div>
    <router-view/>
  </div>
</template>

<script>
import Chat from './components/Chat.vue';
import Settings from './components/Settings.vue';
import Message from './components/Message.vue';

export default {
  name: 'App',
  components: {
    'Chat': Chat,
    'Settings': Settings,
    'Message': Message,
  },
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
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
</style>
