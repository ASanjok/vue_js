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

export default {
  methods: {
  }
}

Vue.config.productionTip = false;

// Axios interceptor to automatically add Authorization header with Bearer token on every request
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  console.error('Request error:', error);
  return Promise.reject(error);
});

// Function to clear token and redirect user to login page (logout)
function logout() {
  console.log('Logging out...');
  localStorage.removeItem('authToken');
  router.push('/login');
}

// Function to track JWT token expiration, show warning toast 30 seconds before expiry,
// and logout user once token is expired
function trackTokenExpiration() {
  const token = localStorage.getItem('authToken');
  console.log("in trackTokenExpiration");
  if (token) {
    try {
      // Decode JWT token payload (base64 decode and parse JSON)
      const decodedToken = JSON.parse(atob(token.split('.')[1]));
      const expirationTime = decodedToken.exp * 1000; // JWT exp is in seconds, convert to ms
      const timeUntilExpiration = expirationTime - Date.now();

      console.log('Token will expire in:', timeUntilExpiration, 'ms');

      // Show warning toast 30 seconds before token expires
      setTimeout(() => {
        // Only show if token hasn't changed in localStorage
        if (token == localStorage.getItem('authToken')) {
          Vue.prototype.$toast.warning('Your session is about to expire in 30 seconds.', {
            timeout: true, // Notification does not disappear automatically
          });
        } else {
          // Token was refreshed, restart tracking for new token
          trackTokenExpiration();
          return;
        }
      }, timeUntilExpiration - 30000);

      // Logout once token has expired
      setTimeout(() => {
        if (token == localStorage.getItem('authToken')) {
          logout();
          // After logout, start waiting for new token and track again
          waitForTokenAndTrack();
        } else {
          trackTokenExpiration();
          return;
        }
      }, timeUntilExpiration);

      // Immediate logout if token is already expired
      if (timeUntilExpiration <= 0) {
        logout();
      }
    } catch (err) {
      console.error('Failed to decode token:', err);
    }
  }
}

// Poll localStorage every second until token appears, then start expiration tracking
function waitForTokenAndTrack() {
  const checkTokenInterval = setInterval(() => {
    console.log('watching for token');
    const token = localStorage.getItem('authToken');
    if (token) {
      trackTokenExpiration();
      clearInterval(checkTokenInterval);
    }
  }, 1000);
}

// Uncomment and implement if you want to refresh token on each route change
// router.beforeEach(async (to, from, next) => {
//   const token = localStorage.getItem('authToken');
//   if (token) {
//     await refreshToken(); // Refresh token API call
//     trackTokenExpiration(); // Restart tracking
//   }
//   next();
// });

// Create and mount Vue app instance, start tracking token expiration once mounted
new Vue({
  router,
  store,
  render: h => h(App),
  mounted() {
    waitForTokenAndTrack();
  }
}).$mount('#App');

// Install toast plugin with configuration
Vue.use(Toast, {
  timeout: 30000,  // Notifications show for 30 seconds
  position: 'top-right'  // Position of toast notifications
});
