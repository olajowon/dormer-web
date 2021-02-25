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
    padding-bottom: calc(0.175rem + 1px) !important;
    color: #343a40 !important;
  }

  small, .small {
    font-size: 85% !important;
  }

  .btn-group-xs>.btn, .btn-xs {
    padding: 0.15rem 0.4rem;
    font-size: 0.79rem;
    line-height: 1.5;
    border-radius: 0.2rem;
    vertical-align: middle !important;
  }

  .btn-mini, .btn-group-mini > .btn {
    padding: 0.12rem 0.3rem;
    font-size: 0.7rem;
    line-height: 1.25;
    border-radius: 0.2rem;
  }

  .card-sm .card-header {
    font-size: 0.875rem;
    padding: 0.4rem 0.8rem;
  }

  .card-sm .card-body {
    padding: 0.4rem 0.45rem;
  }

  .card-sm button.dropdown-toggle {
    position: fixed;
    right: 8px;
    top: 7px;
    padding: 0px 5px;
  }

  .card-sm .dropdown-menu {
    font-size: 0.815rem;
  }

  .card-sm .dropdown-menu {
    min-width: inherit;
  }

  .metric-card {
    margin-bottom: 0.875rem;
  }

  .metric-card .card-body {
    height: 220px;
  }

  .btn-warning, .btn-warning:focus, .btn-warning.focus, .btn-warning:hover, .btn-warning.disabled, .btn-warning:disabled {
    color: #fff;
  }

  .alert {
    font-size: 0.875rem;
  }

  @-webkit-keyframes spin {
    from {
        -webkit-transform: rotate(0deg);
    }
    to {
        -webkit-transform: rotate(360deg);
    }
  }

  @keyframes spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
  }
</style>
