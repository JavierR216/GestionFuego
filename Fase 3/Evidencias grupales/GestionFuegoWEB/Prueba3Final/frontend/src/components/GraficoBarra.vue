<!-- src/components/GraficoBarra.vue -->
<template>
    <div>
      <canvas ref="grafico"></canvas>
    </div>
  </template>
  
  <script>
  import { Bar } from 'chart.js';
  
  export default {
    name: 'GraficoBarra',
    props: {
      datos: {
        type: Array,
        required: true
      }
    },
    mounted() {
      this.crearGrafico();
    },
    methods: {
      crearGrafico() {
        const ctx = this.$refs.grafico.getContext('2d');
        new Bar(ctx, {
          type: 'bar',
          data: {
            labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo'],
            datasets: [
              {
                label: 'Resumen Semanal',
                data: this.datos,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
              }
            ]
          },
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      }
    }
  };
  </script>
  
  <style scoped>
  canvas {
    max-width: 600px;
    margin: auto;
  }
  </style>
  