<template>
  <div class="page-container">
    <md-app>
      <md-app-content>
        <md-content>
        </md-content>
        <md-button class="md-primary md-raised" v-on:click="saveSettings()">Save</md-button>
      </md-app-content>
    </md-app>
  </div>
</template>

<script>
export default {
  name: 'Settings',
  data () {
    return {
    };
  },
  methods: {
      saveSettings () {
        this.$store.dispatch('sendMessage', {
            'type': 'settings',
        });
        this.message = '';
      }
  }
};
</script>

<style scoped>
    .md-app {
        min-height: 75%;
        /*height: 800px;*/
    }
    .md-textarea {
        height: 200px;;
    }
    .messageClass {
      border: 1px solid black;
    }
</style>
