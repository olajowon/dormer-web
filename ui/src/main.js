// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import { BootstrapVue } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import qs from "qs"
import axios from "axios"
import merge from 'webpack-merge'
import '@ztree/ztree_v3/js/jquery.ztree.core.min.js'
import '@ztree/ztree_v3/js/jquery.ztree.excheck.min.js'
import '@ztree/ztree_v3/css/zTreeStyle/zTreeStyle.css'
import HighCharts from 'highcharts'
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import * as utils from "./utils/utils"

Vue.config.productionTip = false
Vue.use(BootstrapVue)
Vue.use(flatPickr)
HighCharts.setOptions({
  global: {useUTC: false},
  lang: {
    resetZoom: "重置",
  },
})
Vue.prototype.HighCharts = HighCharts
Vue.prototype.axios = axios
Vue.prototype.qs = qs
Vue.prototype.merge = merge
Vue.prototype.utils = utils

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
