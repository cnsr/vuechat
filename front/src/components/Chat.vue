<template>
<div class="page-container">
  <div ref="container" class='popup-container'>
  </div>
  <div>
  </div>
    <md-app>
      <md-app-content>
        <b-progress v-if="this.uploadPercentage > 0"
            :type="'is-darkgrey'"
            :size="'is-small'"
            :value="this.uploadPercentage ? undefined : 0"
            :show-value="false"
            :format="'raw'"
            :keep-trailing-zeroes="false"></b-progress>
        <md-content>
          <div class="messages md-scrollbar" v-chat-scroll="{always: false, smooth: true}">
              <template v-for="msg in getMessages">
                <Message v-bind:msg="msg" v-bind:key="msg.count"></Message>
              </template>
          </div>
        </md-content>
        <!--progress max="100" :value.prop="uploadPercentage"></progress-->
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
            <input accept="audio/*|video/*|image/*" type="file" id="file" ref="file" v-on:change="handleFileUpload"/>
          </div>
          <!--md-field class="md-layout-item">
            <label>File</label>
            <md-file accept="audio/*|video/*|image/*" v-on:change="handleFileUpload" type="file" id="file" ref="file" v-model='filename' placeholder="Only images and videos below 10MiB accepted."/>
          </md-field-->
          <div class="md-layout-item">
            <md-button class="md-primary md-raised" :disabled="this.body == '' || this.disableButton" @click="sendMessage()">Submit</md-button>
          </div>
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
      disableButton: false,
    };
  },
  computed: {
    ...mapState(['usercount', 'messages',]),
    ...mapGetters(['getUsercount', 'getMessages',]),
  },
  methods: {
      sendMessage () {
        if (this.disableButton) {return;};
        switch (true) {
          case (this.body.startsWith('/')):
            this.performSlash();
            break;
          case (this.body.trim() != '' && !this.file):
            console.log('no file')
            this.$store.dispatch('sendMessage', {
              'type': 'message',
              'body': this.body.trim(),
              'username': this.username,
              'thread': this.thread,
              'filelink': this.filelink,
              'filename': this.filename,
            });
            this.body = '';
            this.file = null;
            this.filelink = '';
            this.filename = '';
            this.disableButton = true;
            setTimeout(() => this.disableButton=false, 3000);
            break;
          case (this.file != null):
            this.sendFile();
            this.file = null;
            break;
          case (this.body == '' && this.file == null):
            Vue.prototype.$snack.danger({
              text: 'Empty post!',
            });
            break;
          default:
            alert('Empty');
            break;
        }
      },
      handleFileUpload () {
        //console.log(this.$refs.file.files[0]);
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
            //console.log(this.$refs);
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
    .popup-container {
      position: fixed;
      z-index: 10000000;
      width: auto;
      left: 50%;
      top: 50%;
    }
    .md-layout-item {
      max-height: 36px !important;
    }
    .progress {
      position: relative;
      top:-15px;
      height: 3px;
      margin-top: 0px;
    }
    @media only screen and (max-width: 768px) {
      .md-button {
        margin: 0px;
      }
      #file {

      }
      .md-textarea {
        min-height: 50px !important;
      }
      .progress {
        margin-top: 0px;
      }
    }
    html,body{margin:0;padding:0;}
</style>
