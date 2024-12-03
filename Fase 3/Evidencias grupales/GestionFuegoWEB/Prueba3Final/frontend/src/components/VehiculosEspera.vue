<template>
  <div>
    <h1>Vehículos en Espera</h1>
    <div class="vehiculos-container">
      <button class="boton-atras" @click="irAPaginaDestino">Atrás</button>

      <!-- Contenedor con barra de desplazamiento -->
      <div class="table-wrapper">
        <table class="vehiculos-table">
          <thead>
            <tr>
              <th>Tipo de Vehículo</th>
              <th>Patente</th>
              <th>Fecha de Llegada</th>
              <th>Reparación</th>
              <th>Repuesto</th>
              <th>Costo Reparacion</th>
              <th>Mecánico</th>
              <th>Costo Mecanico</th>
              <th>Acción</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="vehiculo in vehiculos" :key="vehiculo.patente">
              <td>{{ vehiculo.tipoVehiculo }}</td>
              <td>{{ vehiculo.patente }}</td>
              <td>{{ vehiculo.fechaLlegada }}</td>
              <td>{{ vehiculo.reparacion }}</td>
              <td>{{ vehiculo.nombreRepuesto }}</td>
              <td>{{ formatCurrency(vehiculo.montoTotal) }}</td>
              <td>{{ vehiculo.mecanicoNombre }}</td>
              <td>{{ formatCurrency(vehiculo.comision) }}</td>
              <td>
                <div class="acciones-container">
                  <span class="estado">Esperando</span>
                  <button class="boton-acceso" @click="irARepuestos(vehiculo)">Solicitar Repuesto</button>
                  <button class="boton-eliminar" @click="eliminarVehiculo(vehiculo)">
                    <font-awesome-icon icon="trash" />
                  </button>
                  <button class="boton-completar" @click="abrirModal(vehiculo)">Completar</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
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
    <p><strong>Fecha de Llegada:</strong> {{ vehiculoSeleccionado.fechaLlegada }}</p>
    <p><strong>Reparación:</strong> {{ vehiculoSeleccionado.reparacion }}</p>
    <p><strong>Repuesto:</strong> {{ vehiculoSeleccionado.nombreRepuesto }}</p>
    <p><strong>Precio del Repuesto:</strong> {{ formatCurrency(vehiculoSeleccionado.precioRepuesto) }}</p>
    <p><strong>Costo reparacion:</strong> {{ formatCurrency(vehiculoSeleccionado.montoTotal) }}</p>
    <p><strong>Mecánico:</strong> {{ vehiculoSeleccionado.mecanicoNombre }}</p>
    <p><strong>Costo Mecánico:</strong> {{ formatCurrency(vehiculoSeleccionado.comision) }}</p>
   <p><strong>Precio Total:</strong> {{ formatCurrency(calcularSumaTotal) }}</p>

    <button @click="cerrarModal">Cerrar</button>
    <button class="boton-confirmar" @click="confirmarBoleta">Confirmar</button>
  </div>
</div>
    </div>
    <!--
<div v-if="mostrarModalExitosa" class="modal-overlay">
  <div class="modal-content">
    <h2>¡Boleta Exitosa!</h2>
    <p>La boleta fue confirmada y el vehículo ha sido eliminado de la espera.</p>
    <button @click="cerrarModalExitosa">Cerrar</button>
  </div>
</div>
-->

  </div>
</template>

<script>
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faTrash } from '@fortawesome/free-solid-svg-icons';

library.add(faTrash);

export default {
  name: 'VehiculosEspera',
  components: {
    FontAwesomeIcon,
  },
  
  data() {
    return {
     vehiculos: [],
    mecanicos: [],
    mostrarModal: false,
    mostrarModalAdvertencia: false, // Nuevo estado para el modal de advertencia
    vehiculoSeleccionado: {},
    precioRepuestos: 0, // Precio de repuestos desde Inventario
    };
  },
  computed: {
    calcularSumaTotal() {
    // Sumar los campos con valores monetarios (si están definidos)
    const montoTotal = this.vehiculoSeleccionado.montoTotal || 0;
    const precioRepuesto = this.vehiculoSeleccionado.precioRepuesto || 0;
    const comision = this.vehiculoSeleccionado.comision || 0;

    return montoTotal + precioRepuesto + comision;
  },
   
  },
    methods: {
      
      // Método para obtener la fecha actual en formato YYYY-MM-DD
    obtenerFechaActual() {
      const fecha = new Date();
      const anio = fecha.getFullYear();
      const mes = (fecha.getMonth() + 1).toString().padStart(2, '0'); // Mes siempre con 2 dígitos
      const dia = fecha.getDate().toString().padStart(2, '0'); // Día siempre con 2 dígitos
      return `${anio}-${mes}-${dia}`;
    },
cerrarModalAdvertencia() {
  this.mostrarModalAdvertencia = false;
},
    async fetchVehiculos() {
  try {
    // Obtener vehículos en espera
    const vehiculoEnEsperaResponse = await axios.get('http://127.0.0.1:8000/api/v1/vehiculos-en-espera/');
    const vehiculosEnEspera = vehiculoEnEsperaResponse.data;

    // Obtener inventario de repuestos
    const inventarioResponse = await axios.get('http://127.0.0.1:8000/api/v1/Inventario/');
    const inventarioData = inventarioResponse.data;

    // Obtener datos de los mecánicos
    const mecanicoResponse = await axios.get('http://127.0.0.1:8000/api/v1/Mecanico/');
    const mecanicosData = mecanicoResponse.data;

    // Mapear los datos
    this.vehiculos = vehiculosEnEspera.map((vehiculo) => {
      const repuestoInfo = inventarioData.find(item => item.id === vehiculo.repuesto); // Asegúrate de usar el nombre correcto del campo
      const mecanicoInfo = mecanicosData.find(mecanico => mecanico.id === vehiculo.mecanico); // Buscar el mecánico por ID
      return {
        ...vehiculo,
        nombreRepuesto: repuestoInfo ? repuestoInfo.nombre : 'Sin repuesto', // Asignar "Sin repuesto" si no se encuentra
        fechaLlegada: vehiculo.fecha_llegada,
        montoTotal: vehiculo.monto_total,
        precioRepuesto: repuestoInfo ? repuestoInfo.precio : 0, // Asignar el precio del repuesto (o 0 si no se encuentra)
        comision: vehiculo.monto_mecanico,
        tipoVehiculo: vehiculo.tipo_vehiculo,
        reparacion: vehiculo.Reparación,
        mecanicoNombre: mecanicoInfo ? `${mecanicoInfo.nombre} ${mecanicoInfo.apellido}` : 'Sin asignar', // Concatenar nombre y apellido
      };
    });
  } catch (error) {
    console.error('Error al obtener los vehículos o el inventario:', error);
  }
    },
    async fetchMecanicos() {
      try {
        const mecanicoResponse = await axios.get('http://127.0.0.1:8000/api/v1/Mecanico/');
        this.mecanicos = mecanicoResponse.data;
      } catch (error) {
        console.error('Error al obtener los mecánicos:', error);
      }
    },
    async fetchPrecioRepuestos() {
      try {
        const inventarioResponse = await axios.get('http://127.0.0.1:8000/api/v1/Inventario/');
        this.precioRepuestos = inventarioResponse.data.reduce((total, item) => total + item.precio, 0);
      } catch (error) {
        console.error('Error al obtener el precio de los repuestos:', error);
      }
    },
    // Formatear fecha
    formatDate(date) {
      if (!date) return 'Sin fecha';
      const parsedDate = new Date(date);
      return parsedDate.toLocaleDateString('es-CL', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
      });
    },

    async eliminarVehiculo(vehiculo) {
      try {
        // Cambiar la URL a la correcta: /vehiculos-en-espera/
        await axios.delete(`http://127.0.0.1:8000/api/v1/vehiculos-en-espera/${vehiculo.id}/`);
        
        // Filtrar el vehículo eliminado de la lista
        this.vehiculos = this.vehiculos.filter(v => v.id !== vehiculo.id);
        
        alert('Vehículo eliminado con éxito.');
      } catch (error) {
        console.error('Error al eliminar el vehículo:', error.response ? error.response.data : error.message);
        alert('Ocurrió un error al intentar eliminar el vehículo.');
      }
    },
  
  abrirModal(vehiculo) {
  if (!vehiculo.nombreRepuesto || vehiculo.nombreRepuesto === 'Sin repuesto') {
    this.mostrarModalAdvertencia = true; // Mostrar el modal de advertencia
    return;
  }
    this.vehiculoSeleccionado = vehiculo;
    this.mostrarModal = true; // Mostrar el modal de completar
  },
    
  cerrarModal() {
      this.mostrarModal = false;
    },
      async confirmarBoleta() {
      try {
        // Preparar los datos de la boleta
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

        // Enviar los datos a la nueva API para registrar el vehículo completo
        const response = await axios.post('http://127.0.0.1:8000/api/v1/Vehiculo-Completo/', boletaData);

        // Eliminar el vehículo de la lista de vehículos en espera
        await axios.delete(`http://127.0.0.1:8000/api/v1/vehiculos-en-espera/${this.vehiculoSeleccionado.id}/`);

        // Filtrar el vehículo eliminado de la lista local
        this.vehiculos = this.vehiculos.filter(v => v.id !== this.vehiculoSeleccionado.id);

        // Mostrar el modal de boleta exitosa
        this.mostrarModalExitosa = true;
        console.log('Respuesta del servidor:', response.data);
        this.cerrarModal(); // Cerrar el modal de boleta
      } catch (error) {
        console.error('Error al confirmar la boleta:', error.response ? error.response.data : error.message);
        alert('Ocurrió un error al intentar confirmar la boleta.');
      }
    },
    
    cerrarModalExitosa() {
      this.mostrarModalExitosa = false;
    }


,
   formatCurrency(value) {
  return new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP' }).format(value);
},


    irARepuestos(vehiculo) {
      this.$router.push({ name: 'inventarioRepuestos', params: { vehiculoId: vehiculo.id } });
    },
    irAPaginaDestino() {
      this.$router.push({ name: 'paginaDestino' });
    },
  },
  mounted() {
    this.fetchVehiculos();
    this.fetchMecanicos();
  },
  
};
</script>



<style scoped>
h1 {
  color: #c72c3b;
  text-align: center; 
  margin-bottom: 20px;
}
body {
  background-image: url('https://shop.iturri.com/blog/wp-content/uploads/2024/09/bomberos.jpg');
  background-size: cover; /* La imagen cubre todo el fondo */
  background-position: center; /* Centra la imagen en la pantalla */
  background-attachment: fixed; /* La imagen no se mueve al hacer scroll */
  height: 100vh; /* Asegura que el fondo cubra toda la altura de la pantalla */
  margin: 0;
  padding: 0;
}
.vehiculos-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.table-wrapper {
  max-height: 500px;
  overflow-y: auto; /* Habilita la barra de desplazamiento */
  margin-top: 20px;
}

.vehiculos-table {
  width: 100%;
  border-collapse: collapse;
}

.vehiculos-table th, .vehiculos-table td {
  padding: 12px;
  text-align: center;
  border-bottom: 1px solid #ddd;
}

.vehiculos-table th {
  background-color: #c72c3b;
  color: white;
}

.vehiculos-table tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

.vehiculos-table tbody tr:hover {
  background-color: #f1f1f1;
}

.boton-atras {
  background-color: #ff4d4d;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.boton-atras:hover {
  background-color: #ff3333;
}

.boton-acceso {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 5px;
}

.boton-acceso:hover {
  background-color: #45a049;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 100%;
}

.boton-confirmar {
  background-color: #28a745;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.boton-confirmar:hover {
  background-color: #218838;
}

.boton-eliminar {
  background-color: #e74c3c;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.boton-eliminar:hover {
  background-color: #c0392b;
}

.boton-completar {
  background-color: #e74c3c;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.boton-completar:hover {
  background-color: #c0392b;
}

.acciones-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.estado {
  margin-bottom: 10px;
  font-weight: bold;
  color: #c72c3b;
}

button {
  margin-top: 5px;
}


.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  width: 100%;
  text-align: center;
}

.modal-content h2 {
  margin-bottom: 15px;
  color: #e74c3c;
}

.modal-content button {
  background-color: #e74c3c;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.modal-content button:hover {
  background-color: #c0392b;
}

</style>
