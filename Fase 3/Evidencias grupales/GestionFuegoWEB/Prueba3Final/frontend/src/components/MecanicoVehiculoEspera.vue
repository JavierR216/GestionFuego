<template>
    <div class="vehiculos-espera">
      <h1>Vehículos en Espera</h1>
      <p>Lista de vehículos que esperan reparación.</p>
  
      <!-- Tabla de vehículos en espera -->
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Patente</th>
              <th>Tipo de Vehículo</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(vehiculo, index) in vehiculosEnEspera" :key="index">
              <td>{{ vehiculo.patente }}</td>
              <td>{{ vehiculo.tipoVehiculo }}</td>
              <td>{{ vehiculo.estado }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "MecanicoVehiculoEspera",
    data() {
      return {
        vehiculosEnEspera: [
          { patente: "XYZ123", tipoVehiculo: "Camión", estado: "Esperando reparación" },
          { patente: "LMN456", tipoVehiculo: "Ambulancia", estado: "Esperando reparación" },
          { patente: "JKL789", tipoVehiculo: "Carro bomba", estado: "Esperando reparación" },
        ],
      };
    },
  };
  </script>
  
  <style scoped>
  .vehiculos-espera {
    text-align: center;
    padding: 20px;
  }
  
  .table-container {
    margin: 20px auto;
    max-width: 800px;
    overflow-x: auto;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
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
  </style>
  