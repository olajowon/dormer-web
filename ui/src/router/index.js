import Vue from 'vue'
import Router from 'vue-router'
import Basic from '@/components/Basic'
import Login from '@/components/Login'
import Metric from './metric'
import Organization from './organization'
import User from './user'


Vue.use(Router)

export default new Router({
  routes: [{
      path: '/login/',
      name: 'Login',
      component: Login,
    },
    {
      path: '/',
      name: 'Basic',
      component: Basic,
      children: [
        Metric,
        Organization,
        User
      ]
    }
  ]
})
