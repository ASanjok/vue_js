<template>
  <div id="app">
    <!-- Navbar is shown only when user is not on login or register pages -->
    <b-navbar type="dark" variant="info" v-if="showNavbar">
      <b-navbar-brand to="/map">Lidmašīnas Karte</b-navbar-brand>

      <!-- Search input with dropdown results -->
      <div class="position-relative">
        <b-form-input v-model="searchInput" placeholder="Search by callsign" @input="updateInput(searchInput)"
          class="mr-2" autocomplete="off"></b-form-input>

        <!-- Search results dropdown -->
        <b-list-group v-if="searchResults.length && searchInput" class="position-absolute w-100" style="z-index: 1000">
          <b-list-group-item v-for="(result, index) in searchResults" :key="index" @click="chooseCallSign(result)"
            button>
            {{ result }}
          </b-list-group-item>
        </b-list-group>
      </div>

      <!-- Navbar right side: Style chooser + Account dropdown -->
      <b-navbar-nav class="ml-auto">
        <!-- Style chooser dropdown -->
        <b-nav-item-dropdown text="Map Style" right>
          <b-dropdown-item v-for="style in mapStyles" :key="style.id" @click="changeMapStyle(style.id)">
            {{ style.name }}
          </b-dropdown-item>
        </b-nav-item-dropdown>

        <!-- Account dropdown menu -->
        <b-nav-item-dropdown text="Account" right>
          <b-dropdown-item to="/account">View account information</b-dropdown-item>
          <b-dropdown-item @click="logout">Log out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-navbar>

    <!-- Router outlet to render pages -->
    <router-view />
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchInput: '',  // User's input in the search bar
      mapStyles: [
        { id: 'liberty', name: 'Light' },
        { id: 'dark', name: 'Dark' },
      ]
    };
  },
  computed: {
    // Show navbar only on routes other than login and register
    showNavbar() {
      return !['/login', '/register'].includes(this.$route.path);
    },
    // Get callsign results from Vuex store getter
    searchResults() {
      return this.$store.getters.planesCallSigns;
    }
  },
  methods: {
    // Logout method clears auth token and navigates to login page
    logout() {
      console.log('Logging out...');
      localStorage.removeItem('authToken');
      this.$router.push('/login');
    },
    // Update search input in Vuex store to trigger search results update
    updateInput(newVal) {
      this.$store.commit('setSearchBarInput', newVal);
    },
    // When user selects a callsign from dropdown, clear input and save chosen callsign in store
    chooseCallSign(callsign) {
      this.searchInput = '';
      this.$store.commit('setChoosedCallSign', callsign);
    },
    changeMapStyle(style){
      this.$store.commit('setMapStyle', style)
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
