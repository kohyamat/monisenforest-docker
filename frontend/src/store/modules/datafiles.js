import axios from 'axios'

const state = {
  datafiles: [],
  empty: null,
  networkStatus: null,
}

const getters = {
  allDatafiles: (state) => state.datafiles,
  getEmpty: (state) => state.empty,
  getNetworkStatus: (state) => state.networkStatus,
}

const actions = {
  async getDatafiles({ commit }) {
    await axios
      .get('http://localhost:8000/api/datafiles/')
      .then((response) => {
        commit('setNetworkStatus', null)
        commit('setDatafiles', response.data)
        if (response.data.length > 0) {
          commit('setEmpty', false)
        } else {
          commit('setEmpty', true)
        }
      })
      .catch((e) => {
        console.log(e)
        commit('setNetworkStatus', 'error')
      })
  },
}

const mutations = {
  setDatafiles: (state, datafiles) => (state.datafiles = datafiles),
  setEmpty: (state, empty) => (state.empty = empty),
  setNetworkStatus: (state, status) => (state.networkStatus = status),
}

export default {
  state,
  getters,
  actions,
  mutations,
}
