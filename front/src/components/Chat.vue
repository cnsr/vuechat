<template>
<div class="page-container">
    <md-app>
      <md-app-content>
        <md-app-toolbar class="md-primary">
          <md-button class="md-icon-button" @click="menuVisible = !menuVisible">
            <md-icon>menu</md-icon>
            </md-button>
            <label id='usercount'>Users online: {{ getUsercount }}</label>
          </md-app-toolbar>
        <md-content>
          <div class="messages">
              <template v-for="msg in getMessages">
                <Message v-bind:msg="msg" v-bind:key="msg.count"></Message>
              </template>
          </div>
        </md-content>
        <md-field>
          <label>Username</label>
          <md-input v-model='username'></md-input>
        </md-field>
        <md-field>
          <label>Your message</label>
          <md-textarea v-model="body"></md-textarea>
        </md-field>
        <md-button class="md-primary md-raised" :disabled="this.body == ''" @click="sendMessage()">Submit</md-button>
      </md-app-content>
    </md-app>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex';
import Message from './Message.vue';

export default {
  name: 'Chat_app',
  data () {
    return {
      textarea: '',
      body: '',
      username: '',
    };
  },
  computed: {
    ...mapState(['usercount', 'messages']),
    ...mapGetters(['getUsercount', 'getMessages'])
  },
  methods: {
      sendMessage () {
        //this.$socket.sendObj({'message': this.message});
        this.$store.dispatch('sendMessage', {
          'type': 'message',
          'body': this.body,
          'username': this.username,
        });
        this.body = '';
      }
  },
  components: {
    'Message': Message,
  },
};
</script>

<style scoped>
    .md-app {
        min-height: 75%;
        /*height: 800px;*/
    }
    .md-textarea {
        height: 100px;;
    }
    .li {
      list-style-type: none;
    }
    .usercount {
      position: fixed;
      float: right;
    }
</style>
