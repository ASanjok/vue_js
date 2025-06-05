// store.js
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    searchBarInput: '',          // User input from search bar
    planesCallSigns: {},         // Object storing all planes
    choosedCallSign: '',         // Currently selected call sign
    mapStyle: 'liberty',
  },
  getters: {
    // Filter planesCallSigns by search input (case-insensitive)
    planesCallSigns: state => {
      const input = state.searchBarInput.toLowerCase();
      return Object.keys(state.planesCallSigns).filter(callsign =>
        callsign.toLowerCase().includes(input)
      );
    },
    // Getter for current search bar input
    searchBarInput: state => state.searchBarInput,
    mapStyle: state =>state.mapStyle,
  },
  mutations: {
    // Update planesCallSigns object in state
    setPlanesCallSigns(state, newValue) {
      state.planesCallSigns = { ...newValue };
    },
    // Update searchBarInput state value
    setSearchBarInput(state, newValue) {
      state.searchBarInput = newValue
    },
    // Update the selected call sign
    setChoosedCallSign(state, newValue){
      state.choosedCallSign = newValue
    },
    setMapStyle(state, newValue){
      state.mapStyle = newValue
    }
  },
  actions: {
  },
  modules: {
  }
})
