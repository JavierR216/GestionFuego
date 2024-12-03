<template>
  <div>
    <h1>Lista de Vehículos</h1>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Tipo de Vehículo</th>
            <th>Patente</th>
            <th>Fecha de Llegada</th>
            <th>Reparación</th>
            <th>Repuesto</th>
            <th>Costo Reparación</th>
            <th>Mecánico</th>
            <th>Costo Mecánico</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(vehiculo, index) in vehiculos" :key="index">
            <td>{{ vehiculo.tipoVehiculo }}</td>
            <td>{{ vehiculo.patente }}</td>
            <td>{{ vehiculo.fechaLlegada }}</td>
            <td>{{ vehiculo.reparacion }}</td>
            <td>{{ vehiculo.nombreRepuesto }}</td>
            <td>{{ formatCurrency(vehiculo.montoTotal) }}</td>
            <td>{{ vehiculo.mecanicoNombre }}</td>
            <td>{{ formatCurrency(vehiculo.comision) }}</td>
            <td>
              <button @click="abrirModal(vehiculo)">Completar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Contenedor para los botones -->
    <div class="action-buttons">
      <button @click="irARepuestos">Solicitar Repuesto</button>
      <button @click="irAPaginaDestino">Atrás</button>
     
    </div>

    <!-- Modal de Advertencia -->
    <div v-if="mostrarModalAdvertencia" class="modal-overlay">
      <div class="modal-content">
        <h2>Advertencia</h2>
        <p>Este vehículo no tiene un repuesto asignado. Por favor, asigna un repuesto antes de completar la boleta.</p>
        <button @click="cerrarModalAdvertencia">Cerrar</button>
      </div>
    </div>

    <!-- Modal de Boleta -->
    <div v-if="mostrarModal" class="modal-overlay">
      <div class="modal-content">
        <h2>Boleta de Reparación</h2>
        <p><strong>Tipo de Vehículo:</strong> {{ vehiculoSeleccionado.tipoVehiculo }}</p>
        <p><strong>Patente:</strong> {{ vehiculoSeleccionado.patente }}</p>
        <p><strong>Fecha de Llegada:</strong> {{ formatDate(vehiculoSeleccionado.fechaLlegada) }}</p>
        <p><strong>Reparación:</strong> {{ vehiculoSeleccionado.reparacion }}</p>
        <p><strong>Repuesto:</strong> {{ vehiculoSeleccionado.nombreRepuesto }}</p>
        <p><strong>Costo Reparación:</strong> {{ formatCurrency(vehiculoSeleccionado.montoTotal) }}</p>
        <p><strong>Mecánico:</strong> {{ vehiculoSeleccionado.mecanicoNombre }}</p>
        <p><strong>Costo Mecánico:</strong> {{ formatCurrency(vehiculoSeleccionado.comision) }}</p>
        <p><strong>Total:</strong> {{ formatCurrency(calcularSumaTotal) }}</p>
        <button @click="cerrarModal">Cerrar</button>
        <button @click="confirmarBoleta">Confirmar</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "ListaVehiculos",
  data() {
    return {
      vehiculos: [],
      mostrarModal: false,
      mostrarModalAdvertencia: false,
      vehiculoSeleccionado: {},
      precioRepuestos: 0,
    };
  },
  computed: {
    calcularSumaTotal() {
      const montoTotal = this.vehiculoSeleccionado.montoTotal || 0;
      const precioRepuesto = this.vehiculoSeleccionado.precioRepuesto || 0;
      const comision = this.vehiculoSeleccionado.comision || 0;
      return montoTotal + precioRepuesto + comision;
    },
  },
  
   formatDate(date) {
      if (!date) return 'Sin fecha';
      const parsedDate = new Date(date);
      return parsedDate.toLocaleDateString('es-CL', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
      });
    },

  methods: {
    async obtenerVehiculos() {
      try {
        const vehiculoEnEsperaResponse = await axios.get('http://127.0.0.1:8000/api/v1/vehiculos-en-espera/');
        const vehiculosEnEspera = vehiculoEnEsperaResponse.data;
        const inventarioResponse = await axios.get('http://127.0.0.1:8000/api/v1/Inventario/');
        const inventarioData = inventarioResponse.data;
        const mecanicoResponse = await axios.get('http://127.0.0.1:8000/api/v1/Mecanico/');
        const mecanicosData = mecanicoResponse.data;

        this.vehiculos = vehiculosEnEspera.map((vehiculo) => {
          const repuestoInfo = inventarioData.find(item => item.id === vehiculo.repuesto);
          const mecanicoInfo = mecanicosData.find(mecanico => mecanico.id === vehiculo.mecanico);
          return {
            ...vehiculo,
            nombreRepuesto: repuestoInfo ? repuestoInfo.nombre : 'Sin repuesto',
            fechaLlegada: vehiculo.fecha_llegada,
            montoTotal: vehiculo.monto_total,
            precioRepuesto: repuestoInfo ? repuestoInfo.precio : 0,
            comision: vehiculo.monto_mecanico,
            tipoVehiculo: vehiculo.tipo_vehiculo,
            reparacion: vehiculo.Reparación,
            mecanicoNombre: mecanicoInfo ? `${mecanicoInfo.nombre} ${mecanicoInfo.apellido}` : 'Sin asignar',
          };
        });
      } catch (error) {
        console.error('Error al obtener los vehículos:', error);
      }
    },
    abrirModal(vehiculo) {
      if (!vehiculo.nombreRepuesto || vehiculo.nombreRepuesto === 'Sin repuesto') {
        this.mostrarModalAdvertencia = true;
        return;
      }
      this.vehiculoSeleccionado = vehiculo;
      this.mostrarModal = true;
    },
    cerrarModal() {
      this.mostrarModal = false;
    },
    cerrarModalAdvertencia() {
      this.mostrarModalAdvertencia = false;
    },
    async confirmarBoleta() {
      try {
        const boletaData = {
          tipo_vehiculo: this.vehiculoSeleccionado.tipoVehiculo,
          patente: this.vehiculoSeleccionado.patente,
          fecha_llegada: this.vehiculoSeleccionado.fechaLlegada,
          reparacion: this.vehiculoSeleccionado.reparacion,
          repuesto: this.vehiculoSeleccionado.repuesto.id,
          precio_repuestos: this.precioRepuestos,
          mecanico: this.vehiculoSeleccionado.mecanico,
          monto_mecanico: this.vehiculoSeleccionado.comision,
          monto_total: this.calcularSumaTotal,
        };

        const response = await axios.post('http://127.0.0.1:8000/api/v1/Vehiculo-Completo/', boletaData);
        await axios.delete(`http://127.0.0.1:8000/api/v1/vehiculos-en-espera/${this.vehiculoSeleccionado.id}/`);
        
        this.vehiculos = this.vehiculos.filter(v => v.id !== this.vehiculoSeleccionado.id);
        alert('Boleta confirmada, vehículo eliminado de la espera.');
        console.log('Respuesta del servidor:', response.data);
        this.cerrarModal();
      } catch (error) {
        console.error('Error al confirmar la boleta:', error);
        alert('Ocurrió un error al confirmar la boleta.');
      }
    },
    formatDate(date) {
      const parsedDate = new Date(date);
      return parsedDate.toLocaleDateString('es-CL', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
      });
    },
    formatCurrency(value) {
      return new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP' }).format(value);
    },
    irARepuestos() {
      this.$router.push({ name: 'repuestosMecanico' });
    },
    irAPaginaDestino() {
      this.$router.push({ name: 'paginaMecanico' });
    },
  },
  mounted() {
    this.obtenerVehiculos();
  },
};
</script>

<style scoped>
h1 {
  color: #dc3545; /* Rojo */
  text-align: center;
  font-size: 2rem;
  margin-bottom: 20px;
  font-family: 'Arial', sans-serif;
}

.table-container {
  margin: 30px auto;
  max-width: 1200px;
  overflow-x: auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

table {
  width: 100%;
  border-collapse: collapse;
  border-radius: 8px;
}

thead {
  background-color: #dc3545; /* Rojo */
  color: white;
  text-transform: uppercase;
}

th,
td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: center;
  font-size: 1rem;
  font-family: 'Arial', sans-serif;
}

th {
  font-weight: bold;
  letter-spacing: 1px;
}

tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

tbody tr:hover {
  background-color: #f1f1f1;
  transform: scale(1.02);
  transition: transform 0.2s ease-in-out;
}

button {
  padding: 8px 16px;
  background-color: #28a745; /* Verde */
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-family: 'Arial', sans-serif;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

button:hover {
  background-color: #218838; /* Verde oscuro */
  transform: scale(1.05);
}

/* Estilo para los botones en la misma fila */
.action-buttons {
  display: flex;
  justify-content: center;
  gap: 15px; /* Espacio entre los botones */
  margin-top: 20px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 10px;
  text-align: center;
  width: 450px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out;
}

.modal-content h2 {
  margin-bottom: 20px;
  color: #dc3545; /* Rojo */
  font-size: 1.5rem;
  font-family: 'Arial', sans-serif;
}

.modal-content button {
  padding: 12px 24px;
  background-color: #28a745; /* Verde */
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.modal-content button:hover {
  background-color: #218838; /* Verde oscuro */
  transform: scale(1.05);
}
</style>