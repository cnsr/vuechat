<template>
    <md-snackbar :md-position="bottom" :md-duration="5000" :md-active.sync="showSnackbar" md-persistent>
      <span>{{pop.text}}</span>
      <md-button class="md-primary" @click="showSnackbar = false">X</md-button>
    </md-snackbar>
</template>

<script>
export default {
    name: 'Snack',
    data() {
        return {
            showSnackbar: false,
        }
    },
    props: {
        pop: {
            type: Object,
        },
    },
}
</script>