<template>
    <div class="services-container px-4">
        <h1 class="text-center"> {{ title }} </h1>
        <div class="row justify-content-start pt-3 col-lg-12">
            <div class="input-group input-group mb-3">
                <span class="input-group-text span-custom" id="inputGroup-sizing-sm">Buscar servicio:</span>
                <input type="text" v-model="searchTerm" @keyup.enter="searchService()" class="form-control" placeholder="Ej: Nombre, Descripcion">
                <span class="input-group-text span-custom" id="inputGroup-sizing-sm">Tipo de servicio:</span>
                <select v-model="selectedServiceType" class="form-select">
                    <option v-for="(value, key) in servicesTypes" :key="key" :value="value"> {{ key }} </option>
                </select>
                <a href="#" class="btn btn-outline-primary" @click="searchService()">Aplicar filtros</a>
                <a href="#" class="btn btn-secondary" @click="resetFilters()">Eliminar filtros</a>

                <span class="input-group-text span-custom" id="inputGroup-sizing-sm">Ordenar por nombre:</span>
                <select v-model="selectedOrder" class="form-select" @change="searchService()">
                    <option v-for="(value, key) in orderDict" :key="key" :value="key"> {{ value }} </option>
                </select>
            </div>
        </div>
        <ReusableTable :columnNames="nombresDeColumnas" :items="listaServicios" linkPrefix="/servicios/detalle" buttonColumnName="Acciones" buttonText="Detalle"/>
        <div class="row px-3">
            <div class="col-lg-6">
                <a href="/" type="button" class="btn btn-dark">Volver al Home</a>
            </div>
            <div class="pagination col-lg-6 justify-content-end">
                <ul class="pagination pagination-sm">
                    <li class="page-item">
                        <a href="#" class="page-link" @click="changePage(actual_page-1)" :class="{ 'disabled': actual_page == 1}">Anterior</a>
                    </li>
                    <li class="page-item" v-for="page in total_pages" :key="page" >
                        <a href="#" class="page-link " @click="changePage(page)" :class="{ 'active': page == actual_page }">{{ page }}</a>
                    </li>
                    <li class="page-item">
                        <a href="#" class="page-link" @click="changePage(actual_page+1)" :class="{ 'disabled': actual_page == total_pages}">Siguiente</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../../assets/services/ServicesTable.css';
import ReusableTable from '../reusable/ReusableTable.vue';

const baseURL = import.meta.env.VITE_BACKEND_BASE_URL;

export default {
    data() {
        return {
            title: "Listado de Servicios Disponibles",
            nombresDeColumnas:{
                name: "Nombre",
                description: "Descripcion",
                type: "Tipo de Servicio",
                laboratory: "Institucion",
            },
            listaServicios: [],
            searchTerm: "",
            servicesTypes: [],
            selectedServiceType: "",
            actual_page: "1",
            total_pages: "",
            selectedOrder: "asc",
            orderDict: {
                asc: "Ascendente",
                esc: "Descendente",
            },
        };
    },
    methods: {
        async searchService() {
            try {
                const response = await axios.get(`${baseURL}/services/api/services/search`, {
                    params: {
                        type: this.selectedServiceType,
                        q: this.searchTerm,
                        page: this.actual_page,
                        order: this.selectedOrder,
                    }
                });
                this.listaServicios = response.data.data;
                this.total_pages = response.data.total_pages;
            }
            catch (error) {
                console.error("Error al obtener los datos:", error);
            }
        },
        changePage(page) {
            this.actual_page = page;
            this.searchService();
        },
        resetFilters() {
            this.searchTerm = "";
            this.selectedServiceType = "";
            this.searchService();
        },
        async fetchServiceTypes() {
            try {
                const response = await axios.get(`${baseURL}/services/api/services-types`);
                this.servicesTypes = response.data.data;
                this.servicesTypes["Todos"] = "";
            }
            catch (error) {
                console.error("Error al obtener los datos:", error);
                console.log(error.response);
            }
        }
    },
    mounted() {
        this.searchService();
        this.fetchServiceTypes();
    },
    components: { ReusableTable }
}
</script>

<style scoped></style>