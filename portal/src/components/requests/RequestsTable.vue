<template>
    <div class="requests-container px-4">
        <div class="table-container"  v-if="!showModal">
            <h1> {{ title }}</h1>
            <div class="row justify-content-start pt-3 col-lg-8">
                <div class="input-group input-group mb-3">
           
                    <span class="input-group-text span-custom" id="inputGroup-sizing-sm">Buscar por Fechas:</span>
                    <input type="date" v-model="fechaInicio" placeholder="Fecha de inicio" class="form-control">
                    <input type="date" v-model="fechaFin" placeholder="Fecha de fin" class="form-control">
                    <span class="input-group-text span-custom" id="inputGroup-sizing-sm">Estado de solicitud:</span>
                    <select v-model="selectedState" class="form-select">
                        <option v-for="est in states" :key="est" :value="est"> {{ est }} </option>
                    </select>
                    <a href="#" class="btn btn-outline-primary my-2 my-sm-0" @click="fetchData">Aplicar filtros</a>
                    <a href="#" class="btn btn-secondary" @click="resetFilters">Eliminar filtros</a>

                </div>
            </div>
            <div class="row justify-content-start pt-3 col-lg-8">
                <div class="input-group input-group mb-3">
           
                    <span class="input-group-text span-custom" id="inputGroup-sizing-sm">Ordenar por:</span>
                    <select v-model="sort" class="form-select">
                        <option v-for="criterio in ['Fecha de Solicitud','Estado']" :key="criterio" :value="criterio"> {{ criterio.toUpperCase() }} </option>
                    </select>
                    <span class="input-group-text span-custom" id="inputGroup-sizing-sm">Criterio de ordenamiento</span>
                    <select  v-model="order" class="form-select">
                        <option v-for="ord in ['desc', 'asc']" :key="ord" :value="ord"> {{ `${ord}endente`.toUpperCase() }} </option>
                    </select>
                    <a href="#" class="btn btn-outline-primary my-2 my-sm-0" @click="fetchData">Aplicar Orden</a>
                </div>
            </div>
            <div class="table-responsive">
                <table>
                    <thead>
                        <tr>
                            <th v-for="columna in nombresDeColumnas">{{ columna }}</th>
                        </tr>
                    </thead>

                    <tbody v-for="pedido in listaPedidos">
                        <tr :key="pedido.id">
                            <td>{{ pedido.service }}</td>
                            <td>{{ pedido.institution }}</td>
                            <td>{{ pedido.requested }}</td>
                            <td>{{ pedido.status }}</td>
                            <td><button class="btn btn-sm btn-primary" @click="() => handleViewDetail(pedido)">Ver detalle</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <a href="/" type="button" class="btn btn-dark">Volver al Home</a>
            <div class="pagination col-lg-6 pagination">
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

        <div class="modal-details" v-if="showModal">
            <div class="card" style="width: 50rem;">
                <div class="card-body">
                    <h5 class="card-title"> {{details.service }}</h5>
                    <h6 class="card-title">Tipo de servicio: {{details.service_type}}</h6>
                
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">Solicitado por: {{details.user}}</li>
                        <li class="list-group-item">Institución: {{details.institution }}</li>
                        <li class="list-group-item">Fecha de solicitud: {{details.requested }}</li>
                        <li class="list-group-item">Estado: {{details.status}} </li>
                    </ul>
                </div>
                <div class="card-comments" style="width: 50rem;">
                    <h6 class="card-title">Comentarios: </h6>
                    <div class="card-comments">
                        <p class="text-start" v-html="details.comment"></p>
                    </div>
                </div>
                <div class="new-comment">
                    <h6 class="card-title">Contestar: </h6>
                    <textarea type="text-area"  v-model="comentario" class="form-control comment-area" id="addComment" name="addComment" placeholder="Comentario"></textarea>
                    <button type="submit" :disabled="!comentario" class="btn btn-primary comment-button"  @click="postComment">Publicar comentario</button>
                </div>
            </div>
            <button class="btn btn-sm btn-dark volver-button" @click="handleHideDetail">Volver</button>
        </div>
        
    </div>
</template>

<script>
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../../assets/requests/RequestsTable.css';

const token = localStorage.getItem('token');

const baseURL = import.meta.env.VITE_BACKEND_BASE_URL;

export default {
    data() {
        return {
            title: "Listado de Solcitudes enviadas del usuario",
            nombresDeColumnas: ["Servicio", "Institucion", "Fecha de Solicitud", "Estado", "Acciones"],
            listaPedidos: [],
            showModal: false,
            details: {},
            states: [],
            selectedState: 'Todos',
            fechaInicio: '',
            fechaFin: '',
            comentario: '',
            order:"desc",
            sort: "Fecha de Solicitud",
            actual_page: 1,
            total_pages: 0,
        };
    },
    methods: {
        async fetchData() {
            const config = {
                headers: {
                    "Authorization": `JWT ${token}`
                },
                params :{
                    estado: this.selectedState,
                    fechaInicio: this.fechaInicio ==="" ? "2000-01-01": this.fechaInicio,
                    fechaFin: this.fechaFin === "" ? "2040-01-01" : this.fechaFin,
                    order: this.order,
                    sort: this.sort,
                    page: this.actual_page
                }
            };
            try {
                const response = await axios.get(`${baseURL}/services/api/me/requests`, config);
                this.listaPedidos = response.data.data;
                this.total_pages = response.data.total_pages;
            }
            catch (error) {
                console.error("Error al obtener los datos:", error);
            }
        },

        handleSelectChange() {
            this.searchService();
        },
        handleViewDetail(pedido) {
            this.details = pedido;
            this.showModal = true;
        },
        handleHideDetail(){
            this.details = {};
            this.showModal = false;
        },
        async fetchStates() {
            try {
                const response = await axios.get(`${baseURL}/services/api/requests-states`);
                this.states = response.data.data;
                this.states.push('Todos');
            } catch (error) {
                console.error('Error al obtener los datos:', error);
                console.log(error.response);
            }
        },

        async postComment(){
            const data = {
                params :{
                    request_id: this.details.id,
                    add_comment: this.comentario,
            }
            }
            try {
                const response = await axios.post(`${baseURL}/services/api/request_comment`, data, {
                    headers: {
                    "Authorization": `JWT ${token}`
                }
                });
                this.comentario = '';
                this.handleViewDetail(response.data.data);
                this.fetchData();
            }
            catch (error) {
                console.error('Error al obtener los datos:', error);
            }  

        },
        changePage(page) {
            this.actual_page = page;
            this.fetchData();
        },
        resetFilters(){
            this.selectedState= 'Todos';
            this.fechaInicio= '';
            this.fechaFin= '';
            this.fetchData();
        }
        
    },
    mounted() {
        this.fetchStates();
        this.fetchData();
    }
}
</script>

<style scoped>
.card{
    margin-bottom: 0%;
    padding-bottom: 1%;
}
.modal-details{
    margin: 1% 25%;
    justify-content: center;
}
.card-comments{
    padding: 2%
}
.volver-button{
    align-self: center;
    margin: 2% 45%;
}
.new-comment{
    padding: 2%;
    margin-bottom: 0%;
}
.comment-button{
    margin-top: 2%;
}
textarea{
    height:50%;
}
.pagination{
    margin-left: 50%;
    margin-right: 50%;
}
</style>