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

axios.interceptors.request.use(
  config => {
    let jwt = localStorage.getItem("jwt");
    if(jwt){
        config.headers.Authorization = jwt;
    }

    config.headers["X-CSRFToken"] = utils.getCookie("csrftoken")

    if(config.method === 'get') {
      config.paramsSerializer = function (params) {
        return qs.stringify(params, {arrayFormat: 'repeat'})
      }
    }

    return config
},
error => {
    return Promise.reject(error);
});


axios.interceptors.response.use(
  response => {
      return response;
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          router.replace({
            path: "/login/",
          })
      }
    }

    let title, message
    if (error.response && error.response.data && error.response.data.msg) {
      title = error.response.status
      message = error.response.data.msg + ", " + (error.response.data.detail || "")
    } else if (error.response && error.response.data) {
      title = error.response.status
      message = JSON.stringify(error.response.data)
    } else if (error.response) {
      title = error.response.status
      message = error.response.statusText
    } else {
      title = "Error"
      message = JSON.stringify(error)
    }

    if (error.response && error.response.config.url == "/api/auth/") {
      if (error.response.status == 400) {
        message = "请输入正确的用户名密码"
      }
    }

    app.$bvToast.toast(message, {
      title: title,
      variant: "danger",
      toaster: "b-toaster-top-center",
      solid: true
    })
    return Promise.reject(error);
  }
);

/* eslint-disable no-new */
const app = new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
