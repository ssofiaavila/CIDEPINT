// Importa los estilos de Bootstrap y BootstrapVue
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'jquery'
import 'popper.js'
import 'bootstrap'

// import './assets/main.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import router from './router';
import axios from 'axios';


const app = createApp(App);

// Configuración de Axios

// Interceptor para manejar errores de red
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      // El servidor respondió con un código de estado que no está en el rango 2xx.
      console.error('Respuesta del servidor con error:', error.response.data);
    } else if (error.request) {
      // La solicitud se hizo pero no se recibió respuesta.
      console.error('No se recibió respuesta del servidor.');
    } else {
      // Algo sucedió en la configuración de la solicitud que desencadenó un error.
      console.error('Error al configurar la solicitud:', error.message);
    }
    return Promise.reject(error);
  }
);

app.use(createPinia());
app.use(router);
app.config.globalProperties.$axios = axios;

app.mount('#app');
