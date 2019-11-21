<template>
<div class="page-container">
  <div ref="container">
  </div>
    <md-app>
      <md-app-content>
        <md-content>
          <div class="messages md-scrollbar">
              <template v-for="msg in getMessages">
                <Message v-bind:msg="msg" v-bind:key="msg.count"></Message>
              </template>
          </div>
        </md-content>
        <progress max="100" :value.prop="uploadPercentage"></progress>
        <div class="md-layout">
          <md-field class="md-layout-item">
            <label>Username</label>
            <md-input v-model='username'></md-input>
          </md-field>
          <md-field class="md-layout-item">
            <label for='threadinput'>Thread</label>
            <md-input id='threadinput' v-model='thread'></md-input>
          </md-field>
        </div>
        <md-field>
          <label>Your message</label>
          <md-textarea md-clearable="true" maxlen="2000" v-model="body" md-counter="2000" v-on:keyup.enter="sendMessage()"></md-textarea>
        </md-field>
        <div class="md-layout">
          <div class="md-layout-item">
            <input type="file" id="file" ref="file" v-on:change="handleFileUpload"/>
          </div>
          <!--md-field class="md-layout-item">
            <label>File</label>
            <md-file accept="audio/*|video/*|image/*" v-on:change="handleFileUpload" type="file" id="file" ref="file" v-model='filename' placeholder="Only images and videos below 10MiB accepted."/>
          </md-field-->
          <md-field class="md-layout-item">
            <md-button class="md-primary md-raised" :disabled="this.body == ''" @click="sendMessage()">Submit</md-button>
          </md-field>
        </div>
      </md-app-content>
    </md-app>
  </div>
</template>

<script>
import Vue from 'vue';
import { mapState, mapGetters } from 'vuex';
import Message from './Message.vue';
import AdminPopup from './AdminPopup.vue';
import * as axios from 'axios';

export default {
  name: 'Chat_app',
  data () {
    return {
      textarea: '',
      body: '',
      username: '',
      thread: 'General',
      file: null,
      filelink: '',
      uploadPercentage: 0,
      filename: '',
    };
  },
  computed: {
    ...mapState(['usercount', 'messages',]),
    ...mapGetters(['getUsercount', 'getMessages',]),
  },
  methods: {
      sendMessage () {
        switch (true) {
          case (this.body.startsWith('/')):
            //console.log('slashfunc');
            this.performSlash();
            break;
          case (this.body.trim() != '' && !this.file):
            console.log('no file')
            this.$store.dispatch('sendMessage', {
              'type': 'message',
              'body': this.body,
              'username': this.username,
              'thread': this.thread,
              'filelink': this.filelink,
              'filename': this.filename,
            });
            this.body = '';
            this.file = null;
            this.filelink = '';
            this.filename = '';
            break;
          case (this.file != null):
            console.log('file is uploaded');
            this.sendFile();
            this.file = null;
            break;
          default:
            alert('Empty');
            break;
        }
      },
      handleFileUpload () {
        console.log(this.$refs.file.files[0]);
        //console.log(this.$refs.file.$refs.inputFile.files[0]);
        //this.file = this.$refs.file.$refs.inputFile.files[0];
        this.file = this.$refs.file.files[0];
        if (this.body == '') this.body = ' ';
        // TODO: check filesize, warn if too large and clear
      },
      sendFile () {
        let formData = new FormData();
        formData.append('file', this.file);
        formData.append('filename', this.file.name);
        axios.post('http://' + location.hostname + ':8000/upload',
          formData,
          {
            headers: {
                'Content-Type': 'multipart/form-data'
            },
            onUploadProgress: function( progressEvent ) {
              this.uploadPercentage = parseInt( Math.round( ( progressEvent.loaded * 100 ) / progressEvent.total ) );
            }.bind(this)
          })
          .then(function(response) {
            console.log(response.data);
            console.log(this);
            if (this.body == '') this.body = ' ';
            this.filelink = response.data.link;
            this.uploadPercentage = 0;
            this.file = null;
          }.bind(this))
          .catch(function() {
            console.log('err');
          })
      },
      performSlash () {
        console.log('slashery');
        console.log(this.body);
        switch (this.body.trim()) {
          case '/admin':
            var adminpop = Vue.extend(AdminPopup);
            var instance = new adminpop();
            instance.$mount();
            console.log(this.$refs);
            this.$refs.container.appendChild(instance.$el);
            break;
          case '/huj':
            break;
          default:
            break;
        }
      }
  },
  components: {
    'Message': Message,
    'AdminPopup': AdminPopup,
  },
};
</script>

<style scoped>
    .md-textarea {
      height: 8vh;
      resize: none !important;
    }
    .md-field {
      margin-top: 0px !important;
      margin-bottom: 12px !important;
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
