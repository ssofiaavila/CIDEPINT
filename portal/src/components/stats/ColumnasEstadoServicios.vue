<template>
  <div>
    <h2 class="text-center">Distribución de solicitudes por estado</h2>
    <div class="chart-container d-flex justify-content-center align-items-center">
      <canvas ref="pieChart"></canvas>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import Chart from 'chart.js/auto';

  const baseURL = import.meta.env.VITE_BACKEND_BASE_URL;

  export default {
    data() {
      return {
        requestPerState: {},
      };
    },
    mounted() {
      this.fetchRequestPerState();
    },
    methods: {
      async fetchRequestPerState() {
        try {
          const response = await axios.get(`${baseURL}/services/request_per_state`);
          this.requestPerState = response.data;

          this.renderPieChart();
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      },
      renderPieChart() {
        const ctx = this.$refs.pieChart.getContext('2d');
        new Chart(ctx, {
          type: 'pie',
          data: {
            labels: Object.keys(this.requestPerState),
            datasets: [{
              data: Object.values(this.requestPerState),
              backgroundColor: [
                '#3498db',
                '#e74c3c',
                '#2ecc71',
                '#f39c12',
                '#9b59b6',
                '#16a085',
              ],
            }],
          },
        });
      },
    },
  };
</script>

<style scoped>
  div {
    padding: 0.5em;
    padding-bottom: 2%;
  }
  .chart-container {
    height: 500px;
  }
</style>