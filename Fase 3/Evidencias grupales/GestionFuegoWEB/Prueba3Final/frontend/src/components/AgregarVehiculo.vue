<template>
  <div>
    <h1>Agregar Vehículo</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="patente">Patente:</label>
        <input type="text" v-model="patente" required />
      </div>
      <div class="form-group">
        <label for="marca">Marca:</label>
        <input type="text" v-model="marca" required />
      </div>
      <div class="form-group">
        <label for="fechaLlegada">Fecha de Llegada:</label>
        <input type="date" v-model="fechaLlegada" required />
      </div>
      <div class="form-group">
        <label for="tipoVehiculo">Tipo de Vehículo:</label>
        <select v-model="tipoVehiculo" required>
          <option disabled value="">Seleccione un tipo</option>
          <option>Carro Bomba</option>
          <option>Carro Escala</option>
          <option>Carro Aljibe</option>
          <option>Carro de Rescate</option>
          <option>Carro Forestal</option>
          <option>Carro HazMat</option>
          <option>Unidad de Rescate</option>
          <option>Ambulancia de Bomberos</option>
          <option>Carro QR</option>
        </select>
      </div>
      <div class="form-group">
        <label for="reparacion">Reparación:</label>
        <input type="text" v-model="reparacion" required />
      </div>
      <div class="form-group">
        <label for="montoTotal">Costo Reparacion:</label>
        <input type="number" v-model="montoTotal" required />
      </div>
      <div class="form-group">
        <label for="mecanico">Mecánico:</label>
        <select v-model="mecanico" @change="updateMontoMecanico" required>
          <option disabled value="">Seleccione un mecánico</option>
          <option v-for="mecanico in mecanicos" :key="mecanico.id" :value="mecanico.id">
            {{ mecanico.nombre }} {{ mecanico.apellido }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="montoMecanico">Costo del Mecánico:</label>
        <input type="number" v-model="montoMecanico" readonly />
      </div>
      <div class="button-group">
        <button type="submit">Guardar Vehículo</button>
        <button type="button" @click="goBack" class="back-button">ATRÁS</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AgregarVehiculo',
  data() {
    return {
      patente: '',
      marca: '',
      fechaLlegada: '',
      tipoVehiculo: '',
      reparacion: '',
      montoTotal: '',
      mecanico: '',
      montoMecanico: '',
      mecanicos: [],
    };
  },
  created() {
    this.fetchMecanicos();
  },
  methods: {
    // Obtener los mecánicos desde el backend
    async fetchMecanicos() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/v1/Mecanico/');
        console.log('Datos de mecánicos:', response.data); // Verificación de datos
        this.mecanicos = response.data;
      } catch (error) {
        console.error('Error al cargar los mecánicos:', error);
      }
    },

    // Actualizar el monto del mecánico seleccionado
    updateMontoMecanico() {
      const selectedMecanico = this.mecanicos.find(m => m.id === this.mecanico);
      if (selectedMecanico) {
        this.montoMecanico = selectedMecanico.monto_mecanico;
        console.log("Monto del Mecánico seleccionado:", this.montoMecanico);
      }
    },

    // Enviar los datos al backend
    async submitForm() {
      const fechaLlegadaFormateada = this.fechaLlegada;
      const vehicleData = {
        patente: this.patente,
        marca: this.marca,
        fecha_llegada: fechaLlegadaFormateada, // Aquí la fecha se mantiene tal cual si el formato es correcto
        tipo_vehiculo: this.tipoVehiculo,
        Reparación: this.reparacion, // Aquí cambio el nombre de "reparacion" a "Reparación" para coincidir con el modelo
        monto_total: this.montoTotal,
        mecanico: this.mecanico,
        monto_mecanico: this.montoMecanico,
      };

      try {
        await axios.post('http://127.0.0.1:8000/api/v1/vehiculos-en-espera/', vehicleData);
        this.$router.push({ name: 'vehiculosEspera' }); // Redirigir después de guardar
      } catch (error) {
        console.error('Error al guardar el vehículo:', error);
        if (error.response) {
          console.log('Respuesta del servidor:', error.response.data); // Ver detalles del error
        }
      }
    },

    // Volver atrás a la página destino
    goBack() {
      this.$router.push({ name: 'paginaDestino' }); // Redirige a la página destino
    },
  },
};
</script>

<style scoped>
/* Estilo general */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  height: 100vh;
  background: linear-gradient(135deg, #6e7bff, #a0b0ff); /* Gradiente suave */
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Contenedor del formulario */
form {
  max-width: 600px;
  margin: 2rem auto;
  padding: 1.5rem;
  background-color: rgba(255, 255, 255, 0.9); /* Fondo blanco semitransparente */
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 2px solid red; /* Bordes rojos */
}

/* Título */
h1 {
  text-align: center;
  color: #333;
  margin-bottom: 1.5rem;
}

/* Grupos de formulario */
.form-group {
  margin-bottom: 1.2rem;
}

/* Etiquetas */
label {
  display: block;
  font-weight: bold;
  color: #555;
  margin-bottom: 0.5rem;
}

/* Campos de entrada */
input[type="text"],
input[type="date"],
input[type="number"],
select {
  width: 100%;
  padding: 0.8rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

/* Botones */
.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 1.5rem;
}

button {
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button[type="submit"] {
  background-color: #28a745;
  color: #fff;
}

button[type="submit"]:hover {
  background-color: #218838;
}

.back-button {
  background-color: #dc3545;
  color: #fff;
}

.back-button:hover {
  background-color: #c82333;
}

/* Espaciado para campos seleccionados */
select {
  appearance: none;
}

/* Espaciado para campos de texto */
input[readonly] {
  background-color: #f1f1f1;
}

/* Efectos responsivos */
@media (max-width: 768px) {
  form {
    padding: 1rem;
  }
  button {
    width: 48%;
  }
}
</style>
