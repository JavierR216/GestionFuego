import { createApp } from 'vue';
import App from './App.vue';
import axios from 'axios';
import router from './router'; // Importa el router

// Importaciones de FontAwesome
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faTrash } from '@fortawesome/free-solid-svg-icons'; // Importa el ícono de basura

// Agregar íconos a la biblioteca de FontAwesome
library.add(faTrash);

const app = createApp(App);

// Configuración de la URL base para todas las solicitudes de axios
axios.defaults.baseURL = 'http://127.0.0.1:8000/api/v1/';

// Interceptores de Axios para manejar errores y autenticación si es necesario
axios.interceptors.response.use(
  (response) => response, // Devuelve la respuesta si es exitosa
  (error) => {
    console.error('Error de Axios:', error);
    alert('Ocurrió un error con la solicitud.');
    return Promise.reject(error);
  }
);

// Configura axios como una propiedad global para usarlo en los componentes
app.config.globalProperties.$axios = axios;

// Usa el router en tu aplicación
app.use(router);

// Registra el componente global de FontAwesome
app.component('font-awesome-icon', FontAwesomeIcon);

app.mount('#app');
