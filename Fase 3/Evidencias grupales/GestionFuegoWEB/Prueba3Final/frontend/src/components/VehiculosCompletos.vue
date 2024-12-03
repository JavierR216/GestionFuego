<template>
  <div>
    <h1>Vehículos Completos</h1>
    <button class="boton-atras" @click="irAPaginaDestino">Atrás</button>
    <div class="vehiculos-container">
      <table class="vehiculos-table">
        <thead>
          <tr>
            <th>Tipo de Vehículo</th>
            <th>Patente</th>
            <th>Fecha de Llegada</th>
            <th>Reparación</th>
            <th>Costo Reparacion</th>
            <th>Mecánico</th>
            <th>Costo Mecanico</th>
            <th>Salida</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="vehiculo in vehiculos" :key="vehiculo.patente">
            <td>{{ vehiculo.tipoVehiculo }}</td>
            <td>{{ vehiculo.patente }}</td>
            <td>{{ formatDate(vehiculo.fechaLlegada) }}</td>
            <td>{{ vehiculo.reparacion }}</td>
            <td>${{ vehiculo.montoTotal }}</td>
            <td>{{ vehiculo.mecanico }}</td>
            <td>${{ vehiculo.comision }}</td>
            <td>
              COMPLETADO EL {{ formatCurrentDate() }}   
            </td>
            <td>
              <button class="boton-eliminar" @click="eliminarVehiculo(vehiculo.id)">
                Eliminar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'VehiculosCompletos',
  data() {
    return {
      vehiculos: [], // Array vacío que se llenará con los datos de la API
    };
  },
  mounted() {
    this.obtenerVehiculos(); // Llamar a la función al montar el componente
  },
  methods: {
  // Obtener los vehículos de la API
  async obtenerVehiculos() {
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
        tipoVehiculo: vehiculo.tipo_vehiculo,
        patente: vehiculo.patente,
        fechaLlegada: vehiculo.fecha_llegada,
        reparacion: vehiculo.reparacion,
        montoTotal: vehiculo.monto_total,
        // Concatenar nombre y apellido del mecánico
        mecanico: mecanicoInfo ? `${mecanicoInfo.nombre} ${mecanicoInfo.apellido}` : 'Sin asignar',
        comision: vehiculo.monto_mecanico,
        fechaSalida: vehiculo.fecha_salida,
        horaSalida: this.formatTime(vehiculo.fecha_salida),
      };
    });
    } catch (error) {
      console.error('Error al obtener los vehículos:', error);
    }
  },
  
  // Eliminar un vehículo
    async eliminarVehiculo(id) {
      if (!id) {
        console.error('El ID no se pasó correctamente:', id);
        alert('Error: El ID del vehículo es inválido.');
        return;
      }
      try {
        await axios.delete(`http://127.0.0.1:8000/api/v1/Vehiculo-Completo/${id}/`);
        this.vehiculos = this.vehiculos.filter(vehiculo => vehiculo.id !== id);
        alert('Vehículo eliminado con éxito.');
      } catch (error) {
        console.error('Error al eliminar el vehículo:', error.response || error.message);
        alert('Error al eliminar el vehículo. Verifique el backend o el ID.');
      }
    },




    formatCurrentDate() {
      const currentDate = new Date();
      const formattedDate = new Intl.DateTimeFormat('es-CL', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      }).format(currentDate);

      return formattedDate; // Solo devuelve la fecha sin la hora
    },

    // Formatear la fecha en formato "día de mes año"
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('es-CL', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    },

    // Formatear la hora en formato "HH:mm"
    formatTime(dateString) {
      const date = new Date(dateString);
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      return `${hours}:${minutes}`;
    },
    // Función para redirigir a otra página
    irAPaginaDestino() {
      this.$router.push({ name: 'paginaDestino' });
    },
  },
};
</script>

<style scoped>
h1 {
  color: #c72c3b; /* Cambié el color aquí */
  text-align: center;
  margin-bottom: 20px;
}

.vehiculos-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  position: relative;
}

.vehiculos-table {
  width: 100%;
  border-collapse: collapse;
}

.vehiculos-table th, .vehiculos-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ccc;
}

.vehiculos-table th {
  background-color: #c72c3b; /* Cambié el color aquí */
  color: white;
}

.vehiculos-table tr:hover {
  background-color: #f2f2f2;
}

.boton-atras {
  position: absolute;
  bottom: 20px;
  left: 20px;
  background-color: #6c757d;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.boton-atras:hover {
  background-color: #5a6268;
}

.boton-eliminar {
  background-color: #e74c3c;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.boton-eliminar:hover {
  background-color: #c82333;
}
</style>
