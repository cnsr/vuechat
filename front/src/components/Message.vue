<template>
  <div class='message-container'>
    <div class="message" v-bind:id='msg.count'>
        <div class='message-header'>
            <span v-if="this.$store.state.admin">
              <b-button squared size='sm' variant="dark" @click="sendDelete(msg.count)">rm</b-button>
              <b-button squared size='sm' variant="dark" class='adminbtn' @click="sendBan(msg.uid)">ban</b-button>
            </span>
            <span>{{msg.time}}</span>
            <span v-if="msg.username != ''">{{msg.username}} </span>
            <a v-bind:href="'#' + msg.count">#{{msg.count}}</a>
        </div>
        <div v-if="msg.filelink != '' && msg.filelink !== undefined" class='file'>
          <img v-bind:src="'http://' + loc + ':8000/' + msg.filelink" />
        </div>
        <pre class='message-text'>{{msg.body}}</pre>
        </div>
    </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex';
export default {
  name: 'Message',
  data () {
    return {
      loc: location.hostname,
    };
  },
  computed: {
  },
  props: {
    msg: {
        type: Object
    },
  },
  methods: {
    sendDelete(id) {
      console.log(id);
      this.$store.dispatch('sendMessage', {
        'type': 'remove',
        'admin': this.$store.state.admin,
        'count': id,
      });
    },
    sendBan(uid, id) {
      this.$store.dispatch('sendMessage', {
        'type': 'remove',
        'admin': this.$store.state.admin,
        'count': id,
        'uid': uid,
      });
    }
  }
};
</script>

<style scoped>
    .message-container {
      display: block;
      position: relative;
      min-height: 50px;
      overflow: auto;
    }
    .message {
      border: 1px dashed #ccc;
      margin-top: 15px;
      display: block;
      overflow: auto;
      padding: 6px;
    }
    .message-header {
      display: block;
      position: absolute;
      background-color: white;
      top: 10px;
      right: 10px;
      padding: 3px;
      border: 1px solid black;
      z-index: 1000;
    }
    .file {
      position: relative;
      float: left;
      width: 100px;
      height: 100px;
      border: 1px solid black;
      padding: 1px;
      padding-left: 2px;
    }
    .message-text {
      padding-top: 5px;
      display: inline-block;
      word-wrap: break-word;
      word-break: break-all;
      overflow-wrap: break-word;
      padding-left: 5px;
      white-space: normal;
    }
</style>