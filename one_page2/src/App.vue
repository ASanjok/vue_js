<template>
  <div id="app">
    <div>
      <!-- Conditional rendering of the navbar, it will only show if not on the login or registration page -->
      <b-navbar type="dark" variant="info" v-if="showNavbar">
        <b-navbar-brand to="/map">Lidmasinas Karte</b-navbar-brand>


        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown text="Account" right>
            <b-dropdown-item to="/account">View account information</b-dropdown-item>
            <b-dropdown-item @click="logout">Log out</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-navbar>
    </div>

    <router-view />
  </div>
</template>

<script>
export default {
  computed: {
    // Check which page the user is on
    showNavbar() {
      // Hide the navbar on the login and registration pages
      return !['/login', '/register'].includes(this.$route.path);
    }
  },
  methods: {
    logout() {
      console.log('Logging out...');
      localStorage.removeItem('authToken');
      this.$router.push('/login');
    }
  }
};
</script>
