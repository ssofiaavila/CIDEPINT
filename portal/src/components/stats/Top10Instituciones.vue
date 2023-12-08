<template>
  <div>
    <h2 class="text-center">Top 10 instituciones con mayor cantidad de solicitudes</h2>
    <div class="chart-container d-flex justify-content-center align-items-center">
      <canvas ref="barChart"></canvas>
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
        topInstitutions: [],
      };
    },
    mounted() {
      this.fetchTopInstitutionsData();
    },
    methods: {
      async fetchTopInstitutionsData() {
        try {
          const response = await axios.get(`${baseURL}/institutions/top-institutions`);
          this.topInstitutions = response.data;
          this.renderBarChart(); 
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      },
      renderBarChart() {
        const ctx = this.$refs.barChart.getContext('2d');
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: this.topInstitutions.map(institution => institution.name),
            datasets: [{
              label: 'Cantidad de solicitudes',
              data: this.topInstitutions.map(institution => institution.request_count),
              backgroundColor: 'rgba(52, 152, 219, 0.7)',
              borderColor: 'rgba(52, 152, 219, 1)',
              borderWidth: 1,
            }],
          },
          options: {
            scales: {
              y: {
                beginAtZero: true,
                ticks: {
                  stepSize: 1,
                },
              },
            },
          },
        });
      },
    },
  };
</script>

<style scoped>
  div {
    padding: 0.5em;
  }
  .chart-container {
    height: 500px;
  }
</style>
