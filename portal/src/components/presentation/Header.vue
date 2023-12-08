<template>
    <header class="p-3 text-bg-dark">
        <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
            <a href="/" class="d-flex align-items-center mb-2 mb-lg-0 text-white text-decoration-none">
                <img class="header-logo" src="../../assets/img/cidepint_logo.jpg" alt="logo" />
            </a>  
            <nav class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
              <slot name="nav-links"></slot> <!-- Slot para los enlaces de navegación no logeados -->
              <template v-if="isAuthenticated">
                <slot name="nav-links-log"></slot> <!-- Slot para los enlaces de navegación logeados -->
              </template>
            </nav>  
            <template v-if="isAuthenticated">
              <div class="flex-shrink-0 dropdown">
                <a href="#" class="d-block link-body-emphasis text-decoration-none dropdown-toggle" data-bs-toggle="dropdown"
                  aria-expanded="false">
                  <img class="profile-logo rounded-circle" src="../../assets/img/brocha.png"
                    alt="profile-logo">
                </a>
                <ul class="dropdown-menu text-small shadow">
                  <li><a class="dropdown-item btn btn-light" @click="logout">Cerrar Sesión</a></li>
                </ul>
              </div>
            </template>
            <template v-else>
              <slot name="nav-login-register"></slot>
            </template>
        </div>
    </header>
</template>


<style scoped src="../../assets/presentation/homePresentation.css"></style>


<script>
import { isAuthenticated } from '../../stores/store.js';
import axios from 'axios';
import Swal from 'sweetalert2';
import { useRouter } from 'vue-router';

const baseURL = import.meta.env.VITE_BACKEND_BASE_URL;

export default {
  setup() {
    const router = useRouter();

    const logout = async () => {
      try {
        await axios.post(`${baseURL}/users/api/logout`, {}, {
          headers: {
            'Authorization': `JWT ${localStorage.getItem('token')}`
          }
        });
      } catch (error) {
        console.error('Error during logout:', error);
      } finally {
        localStorage.removeItem('token');
        isAuthenticated.value = false;
        router.push('/');

        Swal.fire({
          icon: 'success',
          title: 'Has cerrado sesión correctamente',
          confirmButtonText: 'OK'
        });
      }
    };

    return {
      isAuthenticated,
      logout,
    };
  },

  beforeMount() {
    isAuthenticated.value = !!localStorage.getItem('token');
  },
};
</script>