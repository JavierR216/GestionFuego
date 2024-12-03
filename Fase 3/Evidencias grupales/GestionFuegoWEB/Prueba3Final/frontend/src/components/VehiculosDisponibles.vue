<template>
  <div>
    <h1>Vehículos Disponibles</h1>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Tipo de Vehículo</th>
            <th>Patente</th>
            <th>Reparación</th>
            <th>Mecánico</th>
            <th>Fecha de Salida</th>
            <th>Acción</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="vehiculo in vehiculos" :key="vehiculo.id">
            <td>{{ vehiculo.tipo_vehiculo }}</td>
            <td>{{ vehiculo.patente }}</td>
            <td>{{ vehiculo.reparacion }}</td>
            <td>{{ vehiculo.mecanico }}</td>
            <td>{{ formatCurrentDate() }} </td>
            <td>
              <button class="action-button" @click="abrirModal(vehiculo)">Solicitar Vehículo</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Solicitud Vehiculo -->
    <div v-if="mostrarModal" class="modal-overlay">
      <div class="modal">
        <h2>Solicitud de Vehículo</h2>
        <form>
          <div class="form-group">
            <label>Nombre:</label>
            <input type="text" v-model="solicitud.nombre" disabled />
          </div>
          <div class="form-group">
            <label>Tipo de Vehículo:</label>
            <input type="text" v-model="solicitud.tipoVehiculo" disabled />
          </div>
          <div class="form-group">
            <label>Patente:</label>
            <input type="text" v-model="solicitud.patente" disabled />
          </div>
          <div class="form-group">
            <label>Fecha de Salida:</label>
            <input type="date" v-model="solicitud.fechaSalida" disabled />
          </div>
          <div class="modal-actions">
            <button type="button" class="close-button" @click="cerrarModal">Cerrar</button>
            <button type="button" class="confirm-button" @click="confirmarSolicitud">Confirmar</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Botón Atrás -->
    <button class="back-button" @click="irAtras">Atrás</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "VehiculosDisponibles",
  data() {
    return {
      vehiculos: [], // Lista de vehículos disponibles
      mostrarModal: false, // Controla la visibilidad del modal
      solicitud: {
        nombre: "Bombero",
        tipoVehiculo: "",
        patente: "",
        fechaSalida: "",
      },
    };
  },
  mounted() {
    this.fetchVehiculos(); // Obtiene los vehículos al montar el componente
  },
  methods: {
  async fetchVehiculos() {
    try {
      // Obtener los vehículos completos
      const response = await axios.get('http://127.0.0.1:8000/api/v1/Vehiculo-Completo/');
      const vehiculos = response.data;

      // Obtener los datos de los mecánicos
      const mecanicoResponse = await axios.get('http://127.0.0.1:8000/api/v1/Mecanico/');
      const mecanicosData = mecanicoResponse.data;

      // Mapear los vehículos y agregar el nombre completo del mecánico
      this.vehiculos = vehiculos.map(vehiculo => {
        const mecanicoInfo = mecanicosData.find(mecanico => mecanico.id === vehiculo.mecanico); // Buscar el mecánico por ID
        return {
          id: vehiculo.id,
          tipo_vehiculo: vehiculo.tipo_vehiculo || "No especificado",
          patente: vehiculo.patente,
          reparacion: vehiculo.reparacion || "Sin especificar",
          // Concatenar nombre y apellido del mecánico
          mecanico: mecanicoInfo ? `${mecanicoInfo.nombre} ${mecanicoInfo.apellido}` : 'Sin asignar',
          fecha_salida: vehiculo.fecha_salida || "No disponible",
        };
      });
    } catch (error) {
      console.error("Error al obtener los vehículos disponibles:", error);
    }
  },

  abrirModal(vehiculo) {
    // Llena los campos de la solicitud con los datos del vehículo seleccionado
    this.solicitud.tipoVehiculo = vehiculo.tipo_vehiculo;
    this.solicitud.patente = vehiculo.patente;
    this.solicitud.fechaSalida = this.formatCurrentDate();
    this.mostrarModal = true;
  },

  cerrarModal() {
    // Cierra el modal
    this.mostrarModal = false;
  },

  async confirmarSolicitud() {
    // Prepara la solicitud con los datos que la API espera
    const solicitudData = {
      bombero: "BOMBERO", // Asignamos directamente el valor 'BOMBERO'
      tipo_vehiculo: this.solicitud.tipoVehiculo,
      patente: this.solicitud.patente,
      fecha_salida: this.formatCurrentDate(), // Si no hay fecha de salida, pasa null
    };

    console.log("Datos a enviar:", solicitudData);

    try {
      // Envía la solicitud POST a la API
      const response = await axios.post("http://127.0.0.1:8000/api/v1/Solicitud-bombero/", solicitudData);

      // Si la solicitud se confirma, elimina el vehículo de la lista
      alert("Solicitud confirmada!");
      console.log("Datos de la solicitud confirmada:", response.data);

      // Eliminar el vehículo de la lista local
      this.eliminarVehiculoDeLista(this.solicitud.patente);
      
      this.cerrarModal();
    } catch (error) {
      console.error("Error al confirmar la solicitud:", error);
      if (error.response) {
        console.error("Respuesta del servidor:", error.response.data);
        alert("Hubo un error al enviar la solicitud: " + error.response.data.detail || "Error desconocido");
      } else if (error.request) {
        console.error("No se recibió respuesta del servidor:", error.request);
      } else {
        console.error("Error al realizar la solicitud:", error.message);
      }
    }
  },

  // Método para eliminar el vehículo de la lista
  eliminarVehiculoDeLista(patente) {
    this.vehiculos = this.vehiculos.filter(vehiculo => vehiculo.patente !== patente);
  },

  formatCurrentDate() {
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth() + 1).padStart(2, '0'); // Asegura que el mes tenga 2 dígitos
    const day = String(currentDate.getDate()).padStart(2, '0'); // Asegura que el día tenga 2 dígitos

    // Formato YYYY-MM-DD
    return `${year}-${month}-${day}`;
  },

  irAtras() {
    // Redirige a la página anterior
    this.$router.go(-1);
  },
},

};
</script>

<style scoped>
h1 {
  color: #dc3545;
  text-align: center;
  margin-bottom: 20px;
  font-family: 'Roboto', sans-serif; /* Copiado de la fuente del título */
}

.table-container {
  margin: 0 auto;
  max-width: 800px;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
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

.action-button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.action-button:hover {
  background-color: #218838;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.modal h2 {
  margin-bottom: 20px;
  color: #dc3545;
  font-family: 'Roboto', sans-serif; /* Copiado de la fuente del título */
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

.form-group label {
  display: block;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.modal-actions {
  margin-top: 20px;
}

.close-button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.close-button:hover {
  background-color: #c82333;
}

.confirm-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  margin-left: 10px;
}

.confirm-button:hover {
  background-color: #0056b3;
}

.back-button {
  position: fixed;
  bottom: 20px;
  left: 20px;
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.back-button:hover {
  background-color: #5a6268;
}

/*camibio2*/ 
</style>
