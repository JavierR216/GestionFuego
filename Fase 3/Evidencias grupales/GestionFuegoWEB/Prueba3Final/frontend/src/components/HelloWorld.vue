<template>
  <div class="login-container">
    <h1 class="main-title">Gestión Fuego</h1>
    <h2 class="login-title">Iniciar Sesión</h2>
    <form @submit.prevent="login" class="login-form">
      <input
        type="text"
        v-model="username"
        placeholder="Usuario"
        class="login-input"
      />
      <input
        type="password"
        v-model="password"
        placeholder="Contraseña"
        class="login-input"
      />
      <button type="submit" class="login-button">Ingresar</button>
    </form>
    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      error: null,
    };
  },
  methods: {
  login() {
    console.log('Usuario ingresado:', this.username);
    console.log('Contraseña ingresada:', this.password);

    // Validar credenciales de admin
    if (this.username === 'admin' && this.password === 'admin123') {
      this.$router.push({ name: 'paginaDestino' }); // Redirigir al administrador
    } 
    // Validar credenciales de bombero
    else if (this.username === 'bombero' && this.password === 'bombero123') {
      this.$router.push({ name: 'paginaBombero' }); // Redirigir al bombero
    } 
    // Validar credenciales de mecánico
    else if (this.username === 'mecanico' && this.password === 'mecanico123') {
      this.$router.push({ name: 'paginaMecanico' }); // Redirigir al mecánico
    } 
    // Credenciales inválidas
    else {
      this.error = 'Credenciales incorrectas';
    }
  },
},

};
</script>

<style scoped>
/* Contenedor principal con la imagen de fondo */
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-image: url('https://img.freepik.com/fotos-premium/primer-plano-retrato-dos-bomberos-profesionales-parados-junto-vehiculo-todo-terreno-utilizando_396607-43085.jpg?w=826');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.login-container::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  filter: blur(30px);
  z-index: -1;
}

.main-title {
  color: #dc3545;
  margin-bottom: 10px;
  font-size: 48px;
  font-weight: bold;
  text-align: center;
}

.login-title {
  color: #dc3545;
  margin-bottom: 20px;
}

.login-form {
  display: flex;
  flex-direction: column;
  width: 300px;
}

.login-input {
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #dc3545;
  border-radius: 5px;
  font-size: 16px;
}

.login-button {
  padding: 10px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-button:hover {
  background-color: #c82333;
}

.error-message {
  color: red;
  margin-top: 10px;
}
</style>
