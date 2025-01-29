import '@babel/polyfill';
import 'mutationobserver-shim';
import Vue from 'vue';
import './plugins/bootstrap-vue';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from 'axios';
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';

Vue.config.productionTip = false;

// Axios interceptor for adding Authorization header
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken');
  console.log('Intercepted request, adding token:', token); // Logging the token to the console
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  console.error('Request error:', error); // Logging the request error
  return Promise.reject(error);
});

// Function to track token expiration
function trackTokenExpiration() {
  const token = localStorage.getItem('authToken');
  console.log('Tracking token expiration, token:', token); // Logging the token being tracked

  if (token) {
    try {
      const decodedToken = JSON.parse(atob(token.split('.')[1])); // Decoding the JWT payload
      console.log('Decoded token:', decodedToken); // Logging the decoded token

      const expirationTime = decodedToken.exp * 1000; // Token expiration time (in milliseconds)
      const timeUntilExpiration = expirationTime - Date.now();
      console.log('Token will expire in:', timeUntilExpiration, 'ms'); // Logging the time until token expiration

      if (timeUntilExpiration > 0) {
        // Notification 1 minute before expiration
        setTimeout(() => {
          console.log('Session is about to expire, showing toast notification'); // Logging before showing the notification
          Vue.prototype.$toast.warning('Your session is about to expire soon.', {
            timeout: false, // Notification does not disappear automatically
          });
        }, timeUntilExpiration - 60000); // 1 minute before expiration
      } else {
        console.log('Token has expired, logging out'); // Token has expired
        logout();
      }
    } catch (err) {
      console.error('Failed to decode token:', err); // Error decoding the token
    }
  } else {
    console.log('No token found'); // No token present
  }
}

// Logout logic
function logout() {
  console.log('Logging out...'); // Logging the logout message
  localStorage.removeItem('authToken');
  router.push('/login');
}

// Wait for the token to exist before calling trackTokenExpiration
function waitForTokenAndTrack() {
  const checkTokenInterval = setInterval(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      console.log('Token found, starting to track expiration...');
      trackTokenExpiration();
      clearInterval(checkTokenInterval); // Stop checking once the token is found
    } else {
      console.log('No token found, waiting...');
    }
  }, 1000); // Check every 1000 ms (1 second)
}

new Vue({
  router,
  store,
  render: h => h(App),
  mounted() {
    console.log('App mounted, waiting for token...');
    waitForTokenAndTrack(); // Start waiting for the token
  }
}).$mount('#App');

Vue.use(Toast, {
  // Notification settings
  timeout: 50000, // Notification display time (50 seconds)
  position: 'top-right' // Notification position
});
