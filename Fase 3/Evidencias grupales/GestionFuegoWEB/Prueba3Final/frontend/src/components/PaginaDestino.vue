<template>
  <div>
    <header class="navbar">
      <nav>
        <ul>
          <li><span class="menu-text">Control de Vehículos</span></li>
          <li><router-link class="menu-item" to="/vehiculos-espera">Vehículos en Espera</router-link></li>
          <li><router-link class="menu-item" to="/vehiculos-completos">Vehículos Completos</router-link></li>
          <li><router-link class="menu-item" to="/agregar">Agregar</router-link></li>
          <li><router-link class="menu-item" to="/vehiculorepuestos">Inventario de Repuestos</router-link></li>
        </ul>
      </nav>
    </header>
    
    <main>
      <h2>RESUMEN SEMANAL</h2>
      
      <div class="panels-container">
        <div class="panel">
          <h3 class="panel-title">Resumen Mecánico</h3>
          <p>{{ resumenMecanico }}</p>
          <button class="consult-button" @click="toggleTablaMecanico">Ver Detalle</button>
        </div>
      
        
        <!-- Resumen Bombero -->
<div class="panel">
  <h3 class="panel-title">Resumen Bombero</h3>
  <button class="consult-button" @click="toggleTablaBombero">Ver Detalle</button>
</div>

      </div>

      <!-- Gráfico de Barras -->
      <div class="chart-container">
        <BarChart :data="chartData" :options="chartOptions" />
      </div>
      

      <!-- Tabla de Resumen Mecánico -->
      <div v-if="mostrarTablaMecanico" class="overlay" @click.self="toggleTablaMecanico">
        <div class="detalle-mecanico">
          <h3>Resumen Mecanico</h3> <!-- Título agregado -->
          <table class="detalle-table">
            <thead>
              <tr>
                <th>Mecánico</th>
                <th>Reparación</th>
                <th>Patente</th>
                <th>Tipo de Vehículo</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(detalle, index) in detallesMecanico" :key="index">
                <td>{{ detalle.mecanico }}</td>
                <td>{{ detalle.reparacion }}</td>
                <td>{{ detalle.patente }}</td>
                <td>{{ detalle.tipoVehiculo }}</td>
              </tr>
            </tbody>
          </table>
          <button class="close-button" @click="toggleTablaMecanico">Cerrar</button>
        </div>
      </div>
    </main>
  </div>
  <!-- Tabla de Resumen Bombero -->
<div v-if="mostrarTablaBombero" class="overlay" @click.self="toggleTablaBombero">
  <div class="detalle-bombero">
    <h3>Resumen del Bombero</h3>
    <table class="detalle-table">
      <thead>
        <tr>
          <th>Bomero</th>
          <th>Tipo de Vehículo</th>
          <th>Patente</th>
          <th>Fecha de Salida</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(detalle, index) in detallesBombero" :key="index">
          <td>{{ detalle.bombero }}</td>
          <td>{{ detalle.tipoVehiculo }}</td>
          <td>{{ detalle.patente }}</td>
          <td>{{ formatCurrentDate() }} </td>
        </tr>
      </tbody>
    </table>
    <button class="close-button" @click="toggleTablaBombero">Cerrar</button>
  </div>
</div>

</template>



<script>
import axios from 'axios';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

// Registrar los componentes de ChartJS
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

export default {
  name: 'PaginaDestino',
  components: {
    BarChart: Bar,  // Asegúrate de que BarChart está correctamente importado
  },
  data() {
    return {
      mostrarTablaMecanico: false,
      mostrarTablaBombero: false,  // Nueva variable para la tabla de Bombero
      detallesMecanico: [],
      detallesBombero: [],  // Datos para la tabla de Bombero
      resumenMecanico: "",
      chartData: {
        labels: ['Vehículos en Espera', 'Vehículos Completos'],
        datasets: [
          {
            label: 'Cantidad de Vehículos',
            data: [0, 0],
            backgroundColor: 'rgba(0, 123, 255, 0.5)',
          },
        ],
      },
      chartOptions: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: 'Resumen de Vehículos',
          },
        },
      },
    };
  },
  methods: {
    toggleTablaMecanico() {
      this.mostrarTablaMecanico = !this.mostrarTablaMecanico;
      if (this.mostrarTablaMecanico) {
        this.fetchDetallesMecanico();
      }
    },
    toggleTablaBombero() {
      this.mostrarTablaBombero = !this.mostrarTablaBombero;
      if (this.mostrarTablaBombero) {
        this.fetchDetallesBombero();  // Traer los detalles del bombero
      }
    },
    async fetchDetallesMecanico() {
      try {
        const responseVehiculos = await axios.get('http://127.0.0.1:8000/api/v1/vehiculos-en-espera/');
        this.detallesMecanico = await Promise.all(responseVehiculos.data.map(async (vehiculo) => {
          let mecanico = 'Desconocido';
          if (vehiculo.mecanico) {
            try {
              const responseMecanico = await axios.get(`http://127.0.0.1:8000/api/v1/Mecanico/${vehiculo.mecanico}`);
              mecanico = responseMecanico.data.nombre;
            } catch (mecanicoError) {
              console.error('Error al obtener el mecánico:', mecanicoError);
            }
          }
          return {
            mecanico: mecanico,
            reparacion: vehiculo.Reparación || 'N/A',
            tipoVehiculo: vehiculo.tipo_vehiculo || 'N/A',
            patente: vehiculo.patente || 'N/A',
          };
        }));
        this.resumenMecanico = `Hay ${responseVehiculos.data.length} vehículo(s) en espera.`;
      } catch (error) {
        console.error('Error al obtener los detalles de los vehículos:', error);
      }
    },

    async fetchDetallesBombero() {
      try {
        // Aquí puedes obtener la información de los bomberos relacionados con los vehículos
        const responseVehiculos = await axios.get('http://127.0.0.1:8000/api/v1/Solicitud-bombero/');
        
        this.detallesBombero = responseVehiculos.data.map(vehiculo => ({
          bombero: vehiculo.bombero || 'N/A',
          tipoVehiculo: vehiculo.tipo_vehiculo || 'N/A',
          patente: vehiculo.patente || 'N/A',
          fechaSalida: vehiculo.fecha_salida || 'N/A',
        }));
      } catch (error) {
        console.error('Error al obtener los detalles de los bomberos:', error);
      }
    },

    async fetchResumenVehiculos() {
      try {
        const responseEspera = await axios.get('http://127.0.0.1:8000/api/v1/Vehiculo/?estado=espera');
        const responseCompletos = await axios.get('http://127.0.0.1:8000/api/v1/Vehiculo/?estado=completo');
        
        this.chartData.datasets[0].data = [responseEspera.data.length, responseCompletos.data.length];
      } catch (error) {
        console.error('Error al obtener los vehículos:', error);
      }
    },
    formatCurrentDate() {
      const currentDate = new Date();
      const year = currentDate.getFullYear();
      const month = String(currentDate.getMonth() + 1).padStart(2, '0'); // Asegura que el mes tenga 2 dígitos
      const day = String(currentDate.getDate()).padStart(2, '0'); // Asegura que el día tenga 2 dígitos

      // Formato YYYY-MM-DD
      return `${year}-${month}-${day}`;
    },
  },
  mounted() {
    this.fetchResumenVehiculos();
  },

};
</script>

<style scoped>
/* Aplicar imagen de fondo desde una URL externa */
main {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  margin-top: 20px;
  text-align: center;
  background-image: url('https://www.bomberos.cl/images/logo-bomberos-2.png'); /* Ruta de la imagen externa */
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  background-attachment: fixed; /* La imagen no se mueve al hacer scroll */
  min-height: 100vh; /* Asegura que el fondo cubra toda la pantalla */
  font-family: 'Poppins', sans-serif; /* Fuente personalizada */
}

/* Opcional: Filtro semitransparente para mejorar la visibilidad del contenido */
main::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3); /* Filtro de sombra */
  z-index: -1; /* Asegura que no tape el contenido */
}

/* Navbar que ocupa todo el ancho */
.navbar {
  background-color: #2c3e50; /* Color oscuro de fondo */
  padding: 20px 40px; /* Espaciado interno */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%; /* Asegura que ocupe todo el ancho */
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  display: flex;
  justify-content: space-between; /* Distribuye el contenido */
  align-items: center;
  font-family: 'Poppins', sans-serif; /* Fuente personalizada */
}

/* Contenedor del menú */
.navbar ul {
  list-style-type: none;
  padding: 0;
  display: flex;
  gap: 30px; /* Espacio entre los elementos */
  margin: 0;
}

/* Logo o texto principal en el navbar */
.menu-text {
  color: #ecf0f1; /* Color claro */
  font-size: 2rem;
  font-weight: bold;
  letter-spacing: 2px;
  font-family: 'Poppins', sans-serif; /* Fuente personalizada */
}

/* Elementos del menú */
.menu-item {
  color: #ecf0f1;
  text-decoration: none;
  font-size: 1.2rem;
  font-weight: 500;
  padding: 12px 20px;
  border-radius: 5px;
  transition: all 0.3s ease;
  font-family: 'Poppins', sans-serif; /* Fuente personalizada */
}

/* Efecto hover */
.menu-item:hover {
  background-color: #e67e22; /* Color para el hover */
  color: white;
  transform: scale(1.1); /* Aumento de tamaño con hover */
}

/* Logo o texto a la izquierda */
.navbar .logo {
  color: #ecf0f1;
  font-size: 2rem;
  font-weight: bold;
  font-family: 'Poppins', sans-serif; /* Fuente personalizada */
}

/* Responsividad */
@media (max-width: 768px) {
  .navbar ul {
    flex-direction: column; /* Los elementos en columna en pantallas pequeñas */
    align-items: center;
    gap: 10px;
  }

  .menu-item {
    padding: 10px 15px;
    font-size: 1.1rem;
  }
}

.menu-text {
  color: white;
  font-size: 1.8rem;
  font-weight: bold;
  font-family: 'Poppins', sans-serif; /* Fuente personalizada */
}

.menu-item {
  color: white;
  text-decoration: none;
  font-size: 1.2rem;
  padding: 10px 15px;
  border-radius: 5px;
  transition: background-color 0.3s;
  font-family: 'Poppins', sans-serif; /* Fuente personalizada */
}

.menu-item:hover {
  background-color: #9b1f25;
}

main {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  margin-top: 20px;
  text-align: center;
  font-family: 'Poppins', sans-serif; /* Fuente personalizada */
}

.panels-container {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.panel {
  padding: 20px;
  background: rgba(255, 255, 255, 0.3); /* Fondo blanco con 30% de transparencia */
  border: 2px solid #c72c3b;
  border-radius: 10px;
  width: 200px;
  text-align: center;
  backdrop-filter: blur(5px); /* Opcional, añade un desenfoque de fondo */
  font-family: 'Poppins', sans-serif; /* Fuente personalizada */
}

.consult-button {
  background-color: #c72c3b;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1.2rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-family: 'Poppins', sans-serif; /* Fuente personalizada */
}

.consult-button:hover {
  background-color: #9b1f25;
}

/* Gráfico */
.chart-container {
  width: 50%;
  height: 400px;
  margin-top: 20px;
}

/* Overlay y estilo del modal */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.detalle-mecanico {
  background: rgba(255, 255, 255, 0.9); /* Fondo blanco con 85% de opacidad */
  padding: 30px;
  border-radius: 10px;
  width: 80%;
  max-width: 1200px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.5); /* Sombra más oscura */
  border: 2px solid rgba(0, 0, 0, 0.7); /* Borde oscuro (negrísimo) */
  backdrop-filter: blur(5px); /* Opcional, añade un desenfoque de fondo */
}

.detalle-table {
  width: 100%;  
  border-collapse: collapse;
}

.detalle-table th, .detalle-table td {
  padding: 10px;
  border: 1px solid #ccc;
  text-align: left;
}

.close-button {
  background-color: #c72c3b;
  color: white;
  padding: 10px 20px;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 20px;
  border-radius: 5px;
}

.close-button:hover {
  background-color: #9b1f25;
}

/* Estilo para el título 'Resumen del Día' */
.detalle-mecanico h3 {
  font-size: 1.5rem;
  color: #c72c3b; /* Mismo color que el navbar */
  margin-bottom: 20px;
  text-align: center;
  font-family: 'Poppins', sans-serif; /* Fuente personalizada */
}

.detalle-bombero {
  background: rgba(255, 255, 255, 0.9); /* Fondo blanco con 85% de opacidad */
  padding: 30px;
  border-radius: 10px;
  width: 80%;
  max-width: 1200px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.5); /* Sombra más oscura */
  border: 2px solid rgba(0, 0, 0, 0.7); /* Borde oscuro (negrísimo) */
  backdrop-filter: blur(5px); /* Opcional, añade un desenfoque de fondo */
}

/* Estilo para el título 'Resumen del Bombero' */
.detalle-bombero h3 {
  font-size: 1.5rem;
  color: #c72c3b; /* Mismo color que el navbar */
  margin-bottom: 20px;
  text-align: center;
  font-family: 'Poppins', sans-serif; /* Fuente personalizada */
}
</style>
