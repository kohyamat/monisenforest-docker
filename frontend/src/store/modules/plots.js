import axios from "axios";

const state = {
  plots: [],
};

const getters = {
  allPlots: (state) => state.plots,
};

const actions = {
  async getPlots({ commit }) {
    await axios
      .get("http://localhost:8000/api/plots/")
      .then((response) => commit("setPlots", response.data));
  },
};

const mutations = {
  setPlots: (state, plots) => (state.plots = plots),
};

export default {
  state,
  getters,
  actions,
  mutations,
};
