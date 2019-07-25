import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import SearchByPage from './views/SearchByPage.vue'
import SearchByWork from './views/SearchByWork.vue'
import About from './views/About.vue'

Vue.use(Router)

export default new Router({
  //mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/searchByPage',
      name: 'searchByPage',
      component: SearchByPage
    },
    {
      path: '/searchByWork',
      name: 'searchByWork',
      component: SearchByWork
    },
    {
      path: '/about',
      name: 'about',
      component: About
    }
  ]
})
