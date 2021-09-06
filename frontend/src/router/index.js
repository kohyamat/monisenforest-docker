import Vue from "vue";
import VueRouter from "vue-router";
import Overview from "../views/Overview.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Overview",
    component: Overview,
  },
  {
    path: "/data",
    name: "Data",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "data" */ "../views/Data.vue"),
  },
  {
    path: "/species",
    name: "Species",
    component: () =>
      import(/* webpackChunkName: "data" */ "../views/Species.vue"),
  },
  {
    path: "/about",
    name: "About",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
  {
    path: "/treegbh",
    name: "TreeGBH",
    component: () =>
      import(/* webpackChunkName: "data" */ "../views/TreeGBH.vue"),
  },
  {
    path: "/litterfall",
    name: "Litterfall",
    component: () =>
      import(/* webpackChunkName: "data" */ "../views/Litterfall.vue"),
  },
  {
    path: "/seedfall",
    name: "Seedfall",
    component: () =>
      import(/* webpackChunkName: "data" */ "../views/Seedfall.vue"),
  },
];

const router = new VueRouter({
  routes,
});

export default router;
