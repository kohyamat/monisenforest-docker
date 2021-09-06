import Vue from "vue";
import Vuex from "vuex";
import plots from "./modules/plots.js";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: { plots },
});
