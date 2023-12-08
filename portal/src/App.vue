<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Header from './components/presentation/Header.vue'

</script>

<template>
  <Header>
    <template #nav-links>  
      <router-link to="/" class="nav-link px-2 text-white">Home</router-link>
      <router-link to="/servicios" class="nav-link px-2 text-white">Servicios</router-link>
      <router-link to="/estadisticas" class="nav-link px-2 text-white">Estadísticas</router-link>      
    </template>
    <template #nav-links-log>
      <router-link to="/misPedidos" class="nav-link px-2 text-white">Mis Pedidos</router-link>
    </template>
    <template #nav-login-register>
      <router-link to="/iniciarSesion" class="btn btn-outline-light me-2">Iniciar sesión</router-link>
      <router-link class="btn btn-outline-light me-2" to="/registro">Registrarse</router-link>
    </template>
  </Header>
    
    <RouterView />
</template>