// store/index.js
import { createStore } from 'vuex';

export default createStore({
  state: {
    isAuthenticated: false,
    // Puedes agregar más estados según tus necesidades
  },
  mutations: {
    setAuthenticated(state, value) {
      state.isAuthenticated = value;
    },
    // Puedes agregar más mutaciones según tus necesidades
  },
  actions: {
    // Puedes agregar acciones si es necesario
  },
  getters: {
    // Puedes agregar getters si es necesario
  },
  // Puedes agregar más opciones según tus necesidades
});
