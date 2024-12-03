<template>
  <div class="bombero-container">
    <!-- Banner rojo -->
    <div class="banner">
      <h2>Control de Vehículos</h2>
      <div class="button-group">
        <button class="mechanic-button" @click="toggleModal">Mecánico Disponible</button>
        <button class="complete-vehicles-button" @click="goToVehiculosCompletos">Vehículos Disponibles</button>
        <button class="logout-button" @click="logout">Cerrar Sesión</button>
      </div>
    </div>

    <!-- Contenido principal -->
    <h1>Bienvenido, BOMBERO</h1>

    <!-- Tabla de vehículos -->
    <div class="vehicles-table-container">
      <h3>Lista de Vehículos</h3>
      <table>
        <thead>
          <tr>
            <th>Tipo de Vehículo</th>
            <th>Patente</th>
            <th>Fecha de Salida</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="vehiculo in vehiculos" :key="vehiculo.id">
            <td>{{ vehiculo.tipo_vehiculo }}</td>
            <td>{{ vehiculo.patente }}</td>
            <td>{{ formatCurrentDate() }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal de mecánicos -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h3>Mecánicos Disponibles</h3>
        <div class="mecanicos-table-container">
          <table>
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Apellido</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="mecanico in mecanicos" :key="mecanico.id">
                <td>{{ mecanico.nombre }}</td>
                <td>{{ mecanico.apellido }}</td>
                <td>{{ mecanico.estado }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <button class="close-button" @click="toggleModal">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PaginaBombero',
  data() {
    return {
      showModal: false,
      mecanicos: [],
      vehiculos: [],
    };
  },
  methods: {
    toggleModal() {
      this.showModal = !this.showModal;
      if (this.showModal) {
        this.fetchMecanicos();
      }
    },
    async fetchMecanicos() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/v1/Mecanico/');
        this.mecanicos = response.data.map((mecanico) => ({
          ...mecanico,
          estado: 'DISPONIBLE',
        }));
      } catch (error) {
        console.error('Error al obtener los mecánicos:', error);
      }
    },
    async fetchVehiculos() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/v1/Vehiculo-Completo/');
        this.vehiculos = response.data;
      } catch (error) {
        console.error('Error al obtener los vehículos:', error);
      }
    },
    goToVehiculosCompletos() {
      this.$router.push({ name: 'vehiculosDisponibles' });
    },
    logout() {
      this.$router.push({ name: 'Home' });
    },
    formatCurrentDate() {
      const currentDate = new Date();
      const year = currentDate.getFullYear();
      const month = String(currentDate.getMonth() + 1).padStart(2, '0');
      const day = String(currentDate.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },
  },
  mounted() {
    this.fetchVehiculos();
  },
};
</script>

<style scoped>
.bombero-container {
  text-align: center;
  margin: 20px;
  font-family: Arial, sans-serif;
}

.banner {
  background-color: #dc3545;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.banner h2 {
  margin: 0;
  font-size: 24px;
  text-align: left; /* Alinea el título a la izquierda */
  flex-grow: 1; /* Asegura que el título ocupe todo el espacio disponible */
}

.button-group {
  display: flex;
  gap: 10px; /* Espacio entre los botones */
}

.button-group button {
  background-color: white;
  color: #dc3545;
  border: 2px solid white;
  border-radius: 5px;
  padding: 8px 15px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.button-group button:hover {
  background-color: #c82333;
  color: white;
}


.vehicles-table-container {
  margin: 20px auto;
  max-width: 90%;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 10px 0;
}

table th,
table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

table th {
  background-color: #dc3545;
  color: white;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: white;
  border-radius: 8px;
  padding: 20px;
  width: 90%;
  max-width: 500px;
  text-align: center;
}

.close-button {
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
}
</style>
