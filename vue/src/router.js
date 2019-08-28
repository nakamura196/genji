import Vue from 'vue';
import Router from 'vue-router';
import Index from './pages/Index.vue';
import MainFooter from './layout/MainFooter.vue';

Vue.use(Router);

export default new Router({
  linkExactActiveClass: 'active',
  routes: [
    {
      path: '/',
      name: 'index',
      components: { default: Index, footer: MainFooter },
      props: {
        footer: { backgroundColor: 'black' }
      }
    }
  ]
});
