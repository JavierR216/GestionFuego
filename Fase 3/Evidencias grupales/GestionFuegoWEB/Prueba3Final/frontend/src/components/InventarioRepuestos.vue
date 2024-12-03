<template>
  <div>
    <h1>Inventario de Repuestos</h1>
    <div class="inventario-container">
      <!-- Contenedor de la tabla con barra de desplazamiento -->
      <div class="table-wrapper">
        <table class="inventario-table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Marca</th>
              <th>Stock</th>
              <th>Precio</th>
              <th>Acción</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="repuesto in repuestos" :key="repuesto.id">
              <td>{{ repuesto.nombre }}</td>
              <td>{{ repuesto.marca }}</td>
              <td>{{ repuesto.stock }}</td>
              <td>{{ formatearPrecio(repuesto.precio) }}</td>
              <td>
                <button @click="abrirModalAsignacion(repuesto)">Asignar a vehículo</button>
                <button @click="eliminarRepuesto(repuesto.id)" class="btn-eliminar">
                  🗑️
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="button-container">
        <button class="nuevo-btn" @click="mostrarFormulario = true">Nuevo Repuesto</button>
      </div>

      <div class="button-container-back">
        <button class="atras-btn" @click="irAPaginaDestino">Atrás</button>
      </div>
    </div>

    <!-- Modal para asignar repuesto a vehículo -->
    <div v-if="mostrarModal" class="modal-overlay">
      <div class="modal-content">
        <h2>Asignar Repuesto</h2>
        <p><strong>Repuesto:</strong> {{ repuestoSeleccionado.nombre }}</p>
        <h3>Vehículos en espera</h3>
        <ul>
          <li v-for="vehiculo in vehiculosEnEspera" :key="vehiculo.id">
            <span>{{ vehiculo.patente }} - {{ vehiculo.tipoVehiculo }}</span>
            <button @click="asignarRepuestoAlVehiculo(vehiculo)">Asignar</button>
          </li>
        </ul>
        <div class="form-buttons">
          <button type="button" @click="cancelarModal" class="btn cancelar">Cancelar</button>
        </div>
      </div>
    </div>

    <!-- Modal para agregar un nuevo repuesto -->
    <div v-if="mostrarFormulario" class="modal-overlay">
      <div class="modal-content">
        <h2>Agregar Nuevo Repuesto</h2>
        <form @submit.prevent="guardarRepuesto">
          <div class="form-group">
            <label>Nombre:</label>
            <input type="text" v-model="nuevoRepuesto.nombre" required />
          </div>
          <div class="form-group">
            <label>Marca:</label>
            <input type="text" v-model="nuevoRepuesto.marca" required />
          </div>
          <div class="form-group">
            <label>Stock:</label>
            <input type="number" v-model="nuevoRepuesto.stock" required />
          </div>
          <div class="form-group">
            <label>Precio:</label>
            <div class="precio-container">
              <span class="signo-dolar">$</span>
              <input 
                type="text" 
                v-model="nuevoRepuesto.precio" 
                required 
                @input="formatearInputPrecio" 
                placeholder="Precio"
              />
            </div>
          </div>
          <div class="form-buttons">
            <button type="submit" class="btn guardar">Guardar</button>
            <button type="button" @click="cancelar" class="btn cancelar">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios';

export default {
  name: 'InventarioRepuestos',
  data() {
    return {
      repuestos: [],
      vehiculosEnEspera: [],
      mostrarFormulario: false,
      mostrarModal: false,
      repuestoSeleccionado: null,
      nuevoRepuesto: {
        nombre: '',
        marca: '',
        stock: 0,
        precio: 0,
      },
    };
  },
  mounted() {
    this.cargarRepuestos();
    this.cargarVehiculosEnEspera();
  },
  methods: {
  async cargarRepuestos() {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/v1/Inventario/');
      this.repuestos = response.data;
    } catch (error) {
      console.error('Error al cargar los repuestos:', error);
    }
  },
  async cargarVehiculosEnEspera() {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/v1/vehiculos-en-espera/');
      this.vehiculosEnEspera = response.data;
    } catch (error) {
      console.error('Error al cargar los vehículos en espera:', error);
    }
  },
  abrirModalAsignacion(repuesto) {
    this.repuestoSeleccionado = repuesto;
    this.mostrarModal = true;
  },
  cancelarModal() {
    this.mostrarModal = false;
    this.repuestoSeleccionado = null;
  },
  async asignarRepuestoAlVehiculo(vehiculo) {
  try {
    if (!vehiculo.repuesto) {
      if (this.repuestoSeleccionado.stock <= 0) {
        alert("El stock del repuesto seleccionado no es suficiente.");
        return;
      }

      // Reducir el stock localmente
      this.repuestoSeleccionado.stock--;

      // Realizar la solicitud PATCH para actualizar el vehículo
      const response = await axios.patch(
        `http://127.0.0.1:8000/api/v1/vehiculos-en-espera/${vehiculo.id}/`,
        {
          repuesto: this.repuestoSeleccionado.id,
        }
      );

      if (response.status === 200) {
        // Actualizar el estado local del vehículo
        const index = this.vehiculosEnEspera.findIndex((v) => v.id === vehiculo.id);
        if (index !== -1) {
          this.vehiculosEnEspera[index] = {
            ...this.vehiculosEnEspera[index],
            repuesto: this.repuestoSeleccionado.id,
          };
        }

        alert(`Repuesto "${this.repuestoSeleccionado.nombre}" asignado al vehículo ${vehiculo.patente}.`);
        this.vehiculosEnEspera = this.vehiculosEnEspera.filter((v) => v.id !== vehiculo.id);
        this.cancelarModal();
      } else {
        alert("Hubo un problema al asignar el repuesto al vehículo.");
      }
    } else {
      alert("Este vehículo ya tiene un repuesto asignado.");
    }
  } catch (error) {
    console.error("Error al asignar el repuesto:", error);
    alert("Hubo un error al asignar el repuesto.");
  }
  },

  formatearPrecio(precio) {
    return "$" + precio.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  },
  formatearInputPrecio(event) {
    let input = event.target.value;
    input = input.replace(/\D/g, ''); // Eliminar caracteres no numéricos
    input = input.replace(/\B(?=(\d{3})+(?!\d))/g, "."); // Agregar punto cada tres dígitos
    this.nuevoRepuesto.precio = input;
  },
  async guardarRepuesto() {
    try {
      if (this.nuevoRepuesto.stock <= 0 || this.nuevoRepuesto.precio <= 0) {
        alert("El stock y el precio deben ser mayores a cero.");
        return;
      }

      const nuevoRepuesto = {
        nombre: this.nuevoRepuesto.nombre,
        marca: this.nuevoRepuesto.marca,
        stock: this.nuevoRepuesto.stock,
        precio: this.nuevoRepuesto.precio.replace(/\./g, ''),
      };

      const response = await axios.post('http://127.0.0.1:8000/api/v1/Inventario/', nuevoRepuesto);

      if (response.status === 201) {
        this.repuestos.push(response.data);
        this.cancelar();
        alert('Repuesto agregado exitosamente');
      } else {
        alert('Hubo un problema al guardar el repuesto');
      }
    } catch (error) {
      if (error.response && error.response.data) {
        console.error('Error del backend:', error.response.data);
        alert(`Error del backend: ${JSON.stringify(error.response.data)}`);
      } else {
        alert("Hubo un error al guardar el repuesto.");
        console.error('Error al guardar el repuesto:', error);
      }
    }
  },
  cancelar() {
    this.mostrarFormulario = false;
    this.nuevoRepuesto = {
      nombre: '',
      marca: '',
      stock: 0,
      precio: 0,
    };
  },
  irAPaginaDestino() {
    this.$router.push({ name: 'paginaDestino' });
  },
   // Eliminar un repuesto de la base de datos
   async eliminarRepuesto(id) {
    const confirmacion = confirm("¿Estás seguro de que deseas eliminar este repuesto?");
    if (!confirmacion) return;

    try {
      const response = await axios.delete(`http://127.0.0.1:8000/api/v1/Inventario/${id}/`);
      if (response.status === 204) { // Código de éxito para DELETE
        alert("Repuesto eliminado correctamente.");
        // Eliminar el repuesto localmente
        this.repuestos = this.repuestos.filter(repuesto => repuesto.id !== id);
      } else {
        alert("Hubo un problema al eliminar el repuesto.");
      }
    } catch (error) {
      console.error('Error al eliminar el repuesto:', error);
      alert("Hubo un error al intentar eliminar el repuesto.");
    }
  },
},

};
</script>
 
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5); /* Fondo atenuado */
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000; /* Asegura que esté por encima de otros elementos */
  }

  .modal-content {
    background: white;
    border-radius: 10px;
    padding: 20px;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    text-align: center;
  }

  .modal-content h2 {
    margin-bottom: 10px;
    font-size: 1.5rem;
    color: #c72c3b; /* Rojo */
  }

  .modal-content p,
  .modal-content h3 {
    margin: 10px 0;
  }

  .modal-content ul {
    list-style-type: none;
    padding: 0;
  }

  .modal-content li {
    margin: 10px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .modal-content button {
    padding: 8px 12px;
    border-radius: 5px;
    border: none;
    background-color: #c72c3b; /* Rojo */
    color: white;
    cursor: pointer;
  }

  .modal-content button:hover {
    background-color: #b92b2e; /* Rojo más oscuro */
  }

  .modal-content .form-buttons {
    margin-top: 20px;
  }

  .modal-content .btn.cancelar {
    background-color: #e74c3c;
  }

  .modal-content .btn.cancelar:hover {
    background-color: #c0392b;
  }

  .inventario-container {
    margin: 20px auto;
    width: 90%;
    max-width: 1200px;
  }

  .table-wrapper {
    overflow-x: auto;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  }

  .inventario-table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
    background-color: #fff;
    border-radius: 10px;
    overflow: hidden;
  }

  .inventario-table thead tr {
    background-color: #c72c3b; /* Rojo */
    color: white;
    font-size: 1rem;
    text-transform: uppercase;
  }

  .inventario-table th, .inventario-table td {
    padding: 15px;
    border: 1px solid #ddd;
  }

  .inventario-table tbody tr:nth-child(odd) {
    background-color: #f9f9f9;
  }

  .inventario-table tbody tr:nth-child(even) {
    background-color: #f1f1f1;
  }

  .inventario-table tbody tr:hover {
    background-color: #e1e1e1;
  }

  .inventario-table th {
    font-weight: bold;
  }

  button {
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 0.9rem;
  }

  button:hover {
    opacity: 0.9;
  }

  button:active {
    transform: scale(0.98);
  }

  button.btn-eliminar {
    background-color: #e74c3c;
    color: white;
  }

  button.btn-eliminar:hover {
    background-color: #c0392b;
  }

  button.nuevo-btn {
    background-color: #c72c3b; /* Rojo */
    color: white;
    margin-top: 20px;
  }

  button.nuevo-btn:hover {
    background-color: #b92b2e; /* Rojo más oscuro */
  }

  button.atras-btn {
    background-color: #95a5a6;
    color: white;
    margin-top: 10px;
  }

  button.atras-btn:hover {
    background-color: #7f8c8d;
  }

  /* Responsiveness */
  @media (max-width: 768px) {
    .inventario-table th, .inventario-table td {
      padding: 10px;
    }

    button {
      font-size: 0.8rem;
      padding: 8px 10px;
    }
  }
  </style>

