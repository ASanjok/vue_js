<template>
  <div id="app">
    <b-navbar type="dark" variant="info" v-if="showNavbar">
      <b-navbar-brand to="/map">Lidmašīnas Karte</b-navbar-brand>

      <div class="position-relative">
        <b-form-input v-model="searchInput" placeholder="Search by callsign" @input="updateInput(searchInput)"
          class="mr-2" autocomplete="off"></b-form-input>

        <b-list-group v-if="searchResults.length && searchInput" class="position-absolute w-100" style="z-index: 1000">
          <b-list-group-item v-for="(result, index) in searchResults" :key="index" @click="chooseCallSign(result)" button>
            {{ result }}
          </b-list-group-item>
        </b-list-group>
      </div>

      <b-navbar-nav class="ml-auto">
        <b-nav-item-dropdown text="Account" right>
          <b-dropdown-item to="/account">View account information</b-dropdown-item>
          <b-dropdown-item @click="logout">Log out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-navbar>

    <router-view />
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchInput: '',
    }
  },
  computed: {
    // Check which page the user is on
    showNavbar() {
      // Hide the navbar on the login and registration pages
      return !['/login', '/register'].includes(this.$route.path);
    },
    searchResults() {
      return this.$store.getters.planesCallSigns
    }
  },
  methods: {
    logout() {
      console.log('Logging out...');
      localStorage.removeItem('authToken');
      this.$router.push('/login');
    },
    updateInput(newVal) {
      this.$store.commit('setSearchBarInput', newVal)
    },
    chooseCallSign(callsign) {
      this.searchInput = '';
      this.$store.commit('setChoosedCallSign', callsign);
    }
  }
};
</script>

<style>
.search-input {
  margin: 1rem;
  padding: 0.5rem;
  font-size: 1rem;
}

.position-relative {
  position: relative;
}

.position-absolute {
  position: absolute;
}
</style>