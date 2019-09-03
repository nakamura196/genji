import Vue from "vue";
import Router from "vue-router";
import Index from "./pages/Index.vue";
import MainNavbar from "./layout/MainNavbar.vue";

Vue.use(Router);

export default new Router({
  linkExactActiveClass: "active",
  routes: [
    {
      path: "/",
      name: "index",
      components: { default: Index, header: MainNavbar }
    }
  ]
});
