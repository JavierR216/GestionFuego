<template>
  <div class="pagina-mecanico">
    <!-- Banner rojo -->
    <div class="banner">
      <h1 class="banner-title">Control de Vehículos</h1>
      <div class="banner-buttons">
        <button @click="irAListaVehiculos">Lista de Vehículos</button>
        <button @click="irAVehiculosFinalizados">Vehículos Finalizados</button>
        <button @click="irARepuestos">Repuestos</button>
      </div>
    </div>

    <!-- Contenido principal -->
    <div class="content">
      <h2>Bienvenido MECÁNICO</h2>
      

      <!-- Tabla de datos -->
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Mecánico</th>
              <th>Reparación</th>
              <th>Patente</th>
              <th>Tipo de Vehículo</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in datos" :key="index">
              <td>{{ obtenerNombreMecanico(item.mecanico) }}</td> <!-- Mostrar el nombre del mecánico -->
              <td>{{ item.Reparación }}</td>
              <td>{{ item.patente }}</td>
              <td>{{ item.tipo_vehiculo }}</td>
            </tr>
          </tbody>
        </table>
        <p v-if="datos.length === 0">No hay datos disponibles.</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "PaginaMecanico",
  data() {
    return {
      datos: [], // Inicializamos la lista de datos como un arreglo vacío
      mecanicos: [] // Añadimos un array para almacenar los datos de los mecánicos
    };
  },
  methods: {
    irAListaVehiculos() {
      this.$router.push({ name: "listaVehiculos" });
    },
    irARepuestos() {
      this.$router.push({ name: "repuestosMecanico" });
    },
    irAVehiculosFinalizados() {
      this.$router.push({ name: "vehiculosFinalizados" });
    },
    async obtenerDatos() {
      try {
        // Obtener los vehículos en espera
        const respuestaVehiculos = await axios.get("http://127.0.0.1:8000/api/v1/vehiculos-en-espera/");
        this.datos = respuestaVehiculos.data;

        // Obtener los datos de los mecánicos
        const respuestaMecanicos = await axios.get("http://127.0.0.1:8000/api/v1/Mecanico/");
        this.mecanicos = respuestaMecanicos.data;
      } catch (error) {
        console.error("Error al obtener los datos:", error);
      }
    },
    obtenerNombreMecanico(idMecanico) {
      // Buscar el nombre del mecánico usando el ID
      const mecanico = this.mecanicos.find(m => m.id === idMecanico);
      return mecanico ? `${mecanico.nombre} ${mecanico.apellido}` : 'Sin asignar';
    }
  },
  mounted() {
    this.obtenerDatos(); // Llamamos a la función para cargar los datos al montar el componente
  },
};
</script>

<style scoped>
/* Estilo para el contenedor principal */
.pagina-mecanico {
  text-align: center;
  padding: 20px;
  font-family: 'Roboto', sans-serif; /* Fuente para toda la página */
}

/* Estilo del banner */
.banner {
  background-color: #dc3545;
  color: white;
  padding: 15px 20px;
  text-align: left;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: 'Roboto', sans-serif; /* Fuente para el banner */
}

/* Estilo del título en el banner */
.banner-title {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
  font-family: 'Roboto', sans-serif; /* Fuente para el título */
}

/* Botones en el banner */
.banner-buttons button {
  background-color: white;
  color: #dc3545;
  border: 1px solid white;
  border-radius: 5px;
  padding: 8px 12px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
  margin-left: 10px;
  font-family: 'Roboto', sans-serif; /* Fuente para los botones */
}

.banner-buttons button:hover {
  background-color: #dc3545;
  color: white;
}

/* Estilo del contenido principal */
.content {
  margin-top: 20px;
  font-family: 'Roboto', sans-serif; /* Fuente para el contenido principal */
}

/* Estilo de la tabla */
.table-container {
  margin: 20px auto;
  max-width: 800px;
  overflow-x: auto;
  font-family: 'Roboto', sans-serif; /* Fuente para la tabla */
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

thead {
  background-color: #dc3545;
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
</style>
