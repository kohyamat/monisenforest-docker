import Vue from "vue";
import Vuex from "vuex";
import datafiles from "./modules/datafiles.js";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: { datafiles },
});
