<template>
  <div class="vehiculos-finalizados">
    <h1>Vehículos Finalizados</h1>

    <!-- Tabla de vehículos finalizados -->
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Tipo de Vehículo</th>
            <th>Patente</th>
            <th>Fecha de Llegada</th>
            <th>Reparación</th>
            <th>Costo Reparación</th>
            <th>Mecánico</th>
            <th>Costo Mecánico</th>
            <th>Salida</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(vehiculo, index) in vehiculos" :key="index">
            <td>{{ vehiculo.tipo_vehiculo }}</td>
            <td>{{ vehiculo.patente }}</td>
            <td>{{ vehiculo.fecha_llegada }}</td>
            <td>{{ vehiculo.reparacion }}</td>
            <td>${{ formatCurrency(vehiculo.monto_total) }}</td>
            <td>{{ obtenerNombreMecanico(vehiculo.mecanico) }}</td> <!-- Mostrar el nombre del mecánico -->
            <td>${{ formatCurrency(vehiculo.monto_mecanico) }}</td>
            <td>{{ formatCurrentDate() }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Botón Atras -->
    <button class="btn-atras" @click="irAtras">Atras</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "VehiculosFinalizados",
  data() {
    return {
      vehiculos: [], // Lista de vehículos finalizados
      mecanicos: []   // Lista de mecánicos
    };
  },
  mounted() {
    // Llamada al endpoint cuando el componente se monta
    this.fetchVehiculos();
    this.fetchMecanicos();
  },
  methods: {
    // Método para obtener los datos de los vehículos finalizados desde el backend
    fetchVehiculos() {
      axios
        .get('http://127.0.0.1:8000/api/v1/Vehiculo-Completo/')
        .then(response => {
          this.vehiculos = response.data;
        })
        .catch(error => {
          console.error('Hubo un error al obtener los vehículos:', error);
        });
    },
    // Método para obtener los datos de los mecánicos desde el backend
    fetchMecanicos() {
      axios
        .get('http://127.0.0.1:8000/api/v1/Mecanico/')
        .then(response => {
          this.mecanicos = response.data;
        })
        .catch(error => {
          console.error('Hubo un error al obtener los mecánicos:', error);
        });
    },
    // Método para obtener el nombre del mecánico a partir de su ID
    obtenerNombreMecanico(idMecanico) {
      const mecanico = this.mecanicos.find(m => m.id === idMecanico);
      return mecanico ? `${mecanico.nombre} ${mecanico.apellido}` : 'Sin asignar';
    },
    // Método para formatear los valores como moneda
    formatCurrency(value) {
      if (value === undefined || value === null) {
        return '0'; // Valor predeterminado si el valor es inválido
      }
      return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    },
    // Método para ir hacia la página anterior
    irAtras() {
      this.$router.go(-1); // Usamos Vue Router para ir hacia atrás
    },
    // Método para obtener la fecha actual en formato YYYY-MM-DD
    formatCurrentDate() {
      const currentDate = new Date();
      const year = currentDate.getFullYear();
      const month = String(currentDate.getMonth() + 1).padStart(2, '0');
      const day = String(currentDate.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    }
  }
};
</script>

<style scoped>
/* Estilos para la página de vehículos finalizados */
.vehiculos-finalizados {
  text-align: center;
  padding: 20px;
  font-family: 'Roboto', sans-serif; /* Fuente para toda la página */
}

h1 {
  color: #dc3545;
  text-align: center;
  margin-bottom: 20px;
  font-family: 'Roboto', sans-serif; /* Fuente para el título */
}

.table-container {
  margin-top: 20px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background-color: #dc3545; /* Rojo */
  color: white;
}

th,
td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

th {
  font-weight: bold;
}

tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

tbody tr:hover {
  background-color: #f1f1f1;
}

/* Estilo para el botón de "Atras" */
.btn-atras {
  position: fixed;
  left: 20px;
  bottom: 20px;
  background-color: #007bff; /* Azul */
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-atras:hover {
  background-color: #0056b3; /* Azul oscuro */
}
</style>
