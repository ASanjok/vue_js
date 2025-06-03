import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    searchBarInput: '',
    planesCallSigns: {},
    choosedCallSign: '',
  },
  getters: {
    planesCallSigns: state => {
      const input = state.searchBarInput.toLowerCase();
      return Object.keys(state.planesCallSigns).filter(callsign =>
        callsign.toLowerCase().includes(input)
      );
    },
    searchBarInput: state => state.searchBarInput,
  },
  mutations: {
    setPlanesCallSigns(state, newValue) {
      state.planesCallSigns = { ...newValue };
    },
    setSearchBarInput(state, newValue) {
      state.searchBarInput = newValue
    },
    setChoosedCallSign(state, newValue){
      state.choosedCallSign = newValue
    }
  },
  actions: {
  },
  modules: {
  }
})
