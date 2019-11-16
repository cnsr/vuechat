<template>
    <div class="message" v-bind:id='msg.count'>
        <div class='message-header'>
            <span v-if="msg.username != ''">{{msg.username}} </span>
            <a v-bind:href="'#' + msg.count">#{{msg.count}}</a>
        </div>
        <pre>{{msg.body}}</pre>
        </div>
</template>

<script>
export default {
  name: 'Message',
  data () {
    return {
    };
  },
  props: {
    msg: {
        type: Object
    },
  },
  methods: {
  }
};
</script>

<style scoped>
    .message {
        border: 1px dashed #ccc;
        position: relative;
        margin-top: 15px;
    }
    .message-header {
        position: absolute;
        background-color: white;
        top: -10px;
        right: 10px;
        padding: 3px;
        border: 1px solid black;
    }
</style>