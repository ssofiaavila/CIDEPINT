<template>
  <div>
    <h2 class="text-center">Ranking de servicios más solicitados</h2>
    <div class="chart-container d-flex justify-content-center align-items-center">
      <canvas ref="doughnutChart"></canvas>
    </div>
  </div>
</template>

<script>
  import Chart from 'chart.js/auto';
  import axios from 'axios';

  const baseURL = import.meta.env.VITE_BACKEND_BASE_URL;

  export default {
    data() {
      return {
        topServices: [],
      };
    },
    mounted() {
      this.fetchTopRequestedServices();
    },
    methods: {
      async fetchTopRequestedServices() {
        try {
          const response = await axios.get(`${baseURL}/services/top-requested-services`);
          this.topServices = response.data.data;
          this.renderDoughnutChart();
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      },
      renderDoughnutChart() {
        const ctx = this.$refs.doughnutChart.getContext('2d');
        new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels: this.topServices.map(service => `${service.name} - ${service.institution_name}`),
            datasets: [{
              label: 'Cantidad de solicitudes',
              data: this.topServices.map(service => service.request_count),
              backgroundColor: [
                'rgba(52, 152, 219, 0.7)',
                'rgba(231, 76, 60, 0.7)',
                'rgba(46, 204, 113, 0.7)',
              ],
              borderColor: [
                'rgba(52, 152, 219, 1)',
                'rgba(231, 76, 60, 1)',
                'rgba(46, 204, 113, 1)',
              ],
              borderWidth: 1,
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
