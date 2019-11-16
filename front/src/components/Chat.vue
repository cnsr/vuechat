<template>
<div class="page-container">
    <md-app>
      <md-app-content>
        <md-content>
          <div class="messages md-scrollbar">
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
          <md-textarea maxlen="2000" v-model="body"></md-textarea>
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
    .md-textarea {
      height: 8vh;
    }
    .li {
      list-style-type: none;
    }
    .usercount {
      position: fixed;
      float: right;
    }
    .messages {
      overflow-y: scroll;
      height: 55vh;
    }
    html,body{margin:0;padding:0;}
</style>
