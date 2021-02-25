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
    padding: 0.15rem 0.4rem !important;
    font-size: 0.79rem !important;
    line-height: 1.5 !important;
    border-radius: 0.2rem !important;
    vertical-align: middle !important;
  }

  .btn-mini, .btn-group-mini > .btn {
    padding: 0.12rem 0.3rem !important;
    font-size: 0.7rem !important;
    line-height: 1.25 !important;
    border-radius: 0.2rem !important;
  }

  .card-sm .card-header {
    font-size: 0.875rem !important;
    padding: 0.4rem 0.8rem !important;
  }

  .card-sm .card-body {
    padding: 0.4rem 0.45rem !important;
  }

  .card-sm button.dropdown-toggle {
    position: fixed !important;
    right: 8px !important;
    top: 7px !important;
    padding: 0px 5px !important;
  }

  .card-sm .dropdown-menu {
    font-size: 0.815rem !important;
  }

  .card-sm .dropdown-menu {
    min-width: inherit !important;
  }

  .metric-card {
    margin-bottom: 0.875rem !important;
  }

  .metric-card .card-body {
    height: 220px !important;
  }

  .btn-warning, .btn-warning:focus, .btn-warning.focus, .btn-warning:hover, .btn-warning.disabled, .btn-warning:disabled {
    color: #fff !important;
  }

  .alert {
    font-size: 0.875rem !important;
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
