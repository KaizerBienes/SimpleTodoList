<template>
  <div id="app">
    <link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,700" rel="stylesheet">
    <link href="https://unpkg.com/ionicons@4.4.2/dist/css/ionicons.min.css" rel="stylesheet">
    <img src="./assets/logo.png">
    <router-view/>
  </div>
</template>

<script>
import Vue from 'vue'

Vue.prototype.$hostname = 'http://localhost:5000/api/'
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
