import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from '../components/HelloWorld.vue';
import PaginaDestino from '../components/PaginaDestino.vue'; //Página para admin
import PaginaBombero from '../components/PaginaBombero.vue'; //Pagina para Bombero
import VehiculosEspera from '../components/VehiculosEspera.vue';
import VehiculosCompletos from '../components/VehiculosCompletos.vue';
import AgregarVehiculo from '../components/AgregarVehiculo.vue';
import InventarioRepuestos from '../components/InventarioRepuestos.vue'; // Importa el componente de Inventario de Repuestos
import VehiculosDisponibles from '../components/VehiculosDisponibles.vue'
import PaginaMecanico from '../components/PaginaMecanico.vue';
import ListaVehiculos from '../components/ListaVehiculos.vue';
import RepuestosMecanico from '../components/RepuestosMecanico.vue';
import VehiculosFinalizados from '../components/VehiculosFinalizados.vue';



const routes = [
  {
    path: '/',
    name: 'Home',
    component: HelloWorld,
  },
  {
    path: '/pagina-destino',
    name: 'paginaDestino',
    component: PaginaDestino,
  },
  {
    path: '/vehiculos-espera',
    name: 'vehiculosEspera',
    component: VehiculosEspera,
  },
  {
    path: '/vehiculos-completos',
    name: 'vehiculosCompletos',
    component: VehiculosCompletos,
  },
  {
    path: '/agregar',
    name: 'agregarVehiculo',
    component: AgregarVehiculo,
  },
  {
    path: '/vehiculorepuestos', // Ruta para el Inventario de Repuestos
    name: 'inventarioRepuestos',
    component: InventarioRepuestos,
  },
  {
    path: '/paginabombero', // Ruta para la pagina de bombero
    name: 'paginaBombero',
    component: PaginaBombero,
  },
  {
    path: '/vehiculos-disponibles',
    name: 'vehiculosDisponibles',
    component: VehiculosDisponibles,
  },
  { path: '/pagina-mecanico', 
    name: 'paginaMecanico', 
    component: PaginaMecanico 
  },
  { path: "/lista-vehiculos", 
    name: "listaVehiculos", 
    component: ListaVehiculos },

  {
    path: '/repuestos-mecanico',
    name: 'repuestosMecanico',
    component: RepuestosMecanico, 
  },
  {
    path: '/vehiculos-finalizados',
    name: 'vehiculosFinalizados',
    component: VehiculosFinalizados,  // Configura la ruta para el componente VehiculosFinalizados
  },

  
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
