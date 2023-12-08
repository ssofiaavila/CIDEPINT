import { createRouter, createWebHistory } from 'vue-router'
import MyRequestsView from '../views/MyRequestsView.vue'
import presentation from '../views/PresentationView.vue'
import ServiceDetailsView from '../views/services/ServiceDetailsView.vue'
import InicioSesionView from '../views/InicioSesionView.vue'
import RegistroView from '../views/RegistroView.vue'
import ServicesTable from '../components/services/ServicesTable.vue'
import EstadisticasView from '../views/EstadisticasView.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: presentation
    },
    {
      path: '/misPedidos',
      name: 'misPedidos',
      component: MyRequestsView
    },
    {
      path: '/servicios',
      name: 'servicios',
      component: ServicesTable
    },
     {
      path: '/servicios/detalle/:id',
      name: 'detalle',
      component: ServiceDetailsView
    },
    {
      path: '/iniciarSesion',
      name: 'iniciarSesion',
      component: InicioSesionView,
    },
    {
      path: '/registro',
      name: 'registro',
      component: RegistroView,
    },
    {
      path: '/estadisticas',
      name: 'estadisticas',
      component: EstadisticasView,
    }
  ]
})

export default router
