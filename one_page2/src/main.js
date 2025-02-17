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
    // Function to refresh token by making an API call

  }
}



Vue.config.productionTip = false;

// Axios interceptor for adding Authorization header
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

// Logout logic
function logout() {
  console.log('Logging out...');
  localStorage.removeItem('authToken');
  router.push('/login');
}

// Track token expiration and refresh if necessary
function trackTokenExpiration() {
  const token = localStorage.getItem('authToken');
  console.log("in tracktokenexpiration")
  if (token) {
    try {
      const decodedToken = JSON.parse(atob(token.split('.')[1]));
      const expirationTime = decodedToken.exp * 1000;
      const timeUntilExpiration = expirationTime - Date.now();

      console.log('Token will expire in:', timeUntilExpiration, 'ms');

      // Show toast 30 seconds before token expires

      setTimeout(() => {
        if (token == localStorage.getItem('authToken')) {
          Vue.prototype.$toast.warning('Your session is about to expire in 30 seconds.', {
            timeout: true, // Notification does not disappear automatically
          });
        } else {
          trackTokenExpiration();
          return;
        }
      }, timeUntilExpiration - 30000); // 30 seconds before expiration
      setTimeout(() => {
        if (token == localStorage.getItem('authToken')) {
          logout();

          waitForTokenAndTrack();
        } else {
          trackTokenExpiration();
          return;
        }
      }, timeUntilExpiration);


      // Logout if token is expired
      if (timeUntilExpiration <= 0) {
        logout();
      }
    } catch (err) {
      console.error('Failed to decode token:', err);
    }
  }
}

// Wait for the token and start tracking
function waitForTokenAndTrack() {
  const checkTokenInterval = setInterval(() => {
    console.log('whatching for token');
    const token = localStorage.getItem('authToken');
    if (token) {
      trackTokenExpiration();
      clearInterval(checkTokenInterval);
    }
  }, 1000); // Check every second
}

// Before each route, refresh token if necessary
// router.beforeEach(async (to, from, next) => {
//   const token = localStorage.getItem('authToken');

//   if (token) {
//     // Обновить токен и перезапустить отслеживание
//     await refreshToken(); // Функция обновления токена
//     trackTokenExpiration(); // Перезапустить отслеживание истечения
//   }

//   // next(); // Proceed with route change
// });

new Vue({
  router,
  store,
  render: h => h(App),
  mounted() {
    waitForTokenAndTrack(); // Start checking for token when app is mounted
  }
}).$mount('#App');

Vue.use(Toast, {
  timeout: 30000, // Notification display time (50 seconds)
  position: 'top-right' // Notification position
});
