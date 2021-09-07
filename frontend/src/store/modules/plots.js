import axios from "axios";

const state = {
  plots: [],
  empty: null,
  networkStatus: null,
};

const getters = {
  allPlots: (state) => state.plots,
  getEmpty: (state) => state.empty,
  getNetworkStatus: (state) => state.networkStatus,
};

const actions = {
  async getPlots({ commit }) {
    await axios
      .get("http://localhost:8000/api/plots/")
      .then((response) => {
        commit("setNetworkStatus", null);
        commit("setPlots", response.data);
        if (response.data.length > 0) {
          commit("setEmpty", false);
        } else {
          commit("setEmpty", true);
        }
      })
      .catch((e) => {
        console.log(e);
        commit("setNetworkStatus", "error");
      });
  },
};

const mutations = {
  setPlots: (state, plots) => (state.plots = plots),
  setEmpty: (state, empty) => (state.empty = empty),
  setNetworkStatus: (state, status) => (state.networkStatus = status),
};

export default {
  state,
  getters,
  actions,
  mutations,
};
