<template>
  <div class='adminfloater' id='adminfloater'>
        <label>Admin password</label>
        <input v-model="password" type="password" />
        <md-button class="md-primary md-raised" :disabled="this.password == ''" @click="sendAdmin">Submit</md-button>
  </div>
</template>

<script>
import { store } from '../store';
export default {
  name: 'AdminPopup',
  data () {
    return {
      loc: location.hostname,
      password: '',
    };
  },
  props: {
  },
  methods: {
    sendAdmin() {
      store.dispatch('sendMessage', {
        'type': 'admin',
        'password': this.password,
      });
      this.password = '';
    },
  }
}
</script>

<style scoped>
  .adminfloater {
    background: white;
    display: block;
    position: relative;
    border: 2px solid;
    padding: 2px;
    -webkit-box-shadow: 0px 0px 93px -52px rgba(0,0,0,0.55);
    -moz-box-shadow: 0px 0px 93px -52px rgba(0,0,0,0.55);
    box-shadow: 0px 0px 93px -52px rgba(0,0,0,0.55);
  }
</style>
