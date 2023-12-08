<template>
  <div id="carouselExampleDark" class="carousel carousel-dark slide">
    <div class="carousel-indicators">
      <button type="button" data-bs-target="#carouselExampleDark" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
      <button type="button" data-bs-target="#carouselExampleDark" data-bs-slide-to="1" aria-label="Slide 2"></button>
      <button type="button" data-bs-target="#carouselExampleDark" data-bs-slide-to="2" aria-label="Slide 3"></button>
    </div>
    <div class="carousel-inner">
      <div class="carousel-item active" data-bs-interval="10000">
        <Top10Instituciones></Top10Instituciones>
      </div>
      <div class="carousel-item" data-bs-interval="2000">
        <RankingServMasSolicitados></RankingServMasSolicitados>
      </div>
      <div class="carousel-item">
        <ColumnasEstadoServicios></ColumnasEstadoServicios>
      </div>
    </div>
    <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleDark" data-bs-slide="prev">
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Previous</span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleDark" data-bs-slide="next">
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>
  </div>
</template>
  
<script>
  import Top10Instituciones from './Top10Instituciones.vue';
  import RankingServMasSolicitados from './RankingServMasSolicitados.vue';
  import ColumnasEstadoServicios from './ColumnasEstadoServicios.vue';

  export default {
    components: {
      Top10Instituciones,
      RankingServMasSolicitados,
      ColumnasEstadoServicios,
    },
  };
</script>
  
<style scoped>
</style>