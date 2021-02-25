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


router.beforeEach((to, from, next) => {
  let token = localStorage.getItem("token")
  let username = localStorage.getItem("username")

  if (to.name === "Login")
  {
    next()
  }
  else if (token == null || username == null)
  {
    localStorage.setItem("nextRoute", JSON.stringify({path: to.path, query: to.query}))
    next({path: "/login/"})
  }
  else if (to.name == "Basic") {
    next({path: "/user/" + username + "/"})
  }
  else if (to.name == "Metric" || to.name == "User" || to.name == "Organization")
  {
    let lsFrom = localStorage.getItem("from")
    let lsUntil = localStorage.getItem("until")
    let lsRefresh = localStorage.getItem("refresh")

    let lsQuery = localStorage.getItem(to.path + ".query") || "{}"
    if (from.path == to.path) {
      let q = JSON.parse(JSON.stringify(to.query))
      delete q["from"]
      delete q["until"]
      delete q["refresh"]
      localStorage.setItem(to.path + ".query", JSON.stringify(q));
    } else {
      if (JSON.stringify(to.query) == "{}" && lsQuery != "{}") {
        next({path: to.path, query: JSON.parse(lsQuery)})
        return
      }
    }

    if (JSON.stringify(to.query) != "{}") {
      if (to.query.from != lsFrom || to.query.until != lsUntil) {
        localStorage.setItem("from", to.query.from || "");
        localStorage.setItem("until", to.query.until || "");
      }
      if (to.query.refresh != lsRefresh) {
        localStorage.setItem("refresh", to.query.refresh || "0");
      }

      let q = to.query
      if ((to.query.from || to.query.until) && to.query.refresh) {
        next()
      } else {
        if (!to.query.from && !to.query.until) {
          q = merge(q, lsFrom || lsUntil ? {from: lsFrom || "", until: lsUntil || ""} : {from: "-1h", until: "now"})
        }

        if (!to.query.refresh) {
          q = merge(q, {refresh: lsRefresh || "0"})
        }
      }

      next({path: to.path, query: q})
    } else {
      next()
    }
  }
  else if (!from.name)
  {
     axios.post("/api/isauth/", {token: token}).then(response=>{
       next()
     })
     .catch(error=>{
       if (error.response.status == 400) {
         localStorage.setItem("nextRoute", JSON.stringify({path: to.path, query: to.query}))
         next({path: "/login/"})
       }
       next()
     })
  }
  else
  {
    next()
  };
})


/* eslint-disable no-new */
const app = new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
