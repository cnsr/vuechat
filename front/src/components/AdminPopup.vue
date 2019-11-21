<template>
  <div class='adminfloater'>
    <md-field>
      <label>Your message</label>
      <md-field>
        <label>Admin password</label>
        <md-input v-model="password" type="password"></md-input>
      </md-field>
      <md-field class="md-layout-item">
        <md-button class="md-primary md-raised" :disabled="this.password == ''" @click="sendAdmin()">Submit</md-button>
      </md-field>
    </md-field>
  </div>
</template>

<script>
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
        this.$socket
      },
  }
}
</script>

<style scoped>
  .adminfloater {
    display: block;
    position: relative;
    top: -80%;
  }
</style>
