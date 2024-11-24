<template>
  <div id="app">
    <div style="height: 10vh;">
      <b-navbar type="dark" variant="info">
        <b-navbar-brand to="/">A. Sloka</b-navbar-brand>
        <b-navbar-nav class="d-flex mx-auto justify-content-center">
          <b-nav-item to="/firstPage">First Page</b-nav-item>
          <b-nav-item to="/secondPage">Second Page</b-nav-item>
        </b-navbar-nav>
      </b-navbar>
    </div>

    <router-view /> <!-- here show what route return -->
  </div>
</template>
