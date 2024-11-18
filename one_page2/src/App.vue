<template>
  <div id="app">

    <div>
      <b-navbar toggleable="lg" type="dark" variant="info">

        <b-navbar-brand to="/" >A. Sloka</b-navbar-brand>

          <b-navbar-nav class="mx-auto">
            <b-nav-item to="/firstPage">first page</b-nav-item>
            <b-nav-item to="/secondPage">second page</b-nav-item>
          </b-navbar-nav>  
      </b-navbar>
    </div>

    <router-view />  <!-- here show what route return -->
  
  </div>
</template>