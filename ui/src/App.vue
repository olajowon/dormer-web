<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
  #app {
    #font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
    #font-family: Verdana, Arial, Helvetica, AppleGothic, sans-serif, "Microsoft YaHei", "微软雅黑";
    -webkit-font-smoothing: antialiased;
  }

  .col-form-label {
    font-size: 0.875rem !important;
  }

  .navbar-dark .navbar-nav .nav-link {
    color: #fff;
  }
</style>
