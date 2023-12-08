<template>
    <div class="container">
        <div class="row justify-content-center">
            <h1 class="col-lg-12 text-center">{{ service.name }}</h1>
        </div>
        <div class="row justify-content-center pt-4">
            <div class="col-lg-7 container">
                <div class="card row" style="width: 30rem;">
                    <div class="card-header">
                        <h2>Detalle</h2>
                    </div>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">{{ service.description }}</li>
                    </ul>
                </div>
                <div class="card row my-5" style="width: 30rem;">
                    <div class="card-header">
                        <h2>{{ institution.name }}</h2>
                    </div>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">{{ institution.information }}</li>
                    </ul>
                </div>
            </div>
            <div class="col-lg-5 container p-0">
                <div class="row justify-content-center">
                    <button class="btn btn-lg btn-primary col-lg-6" @click="createRequest">Solicitar</button>
                </div>
                <br>
                <div class="row justify-content-center">
                    <h2 class="col-lg-12 text-center">¿Cómo llegar?</h2>
                </div>
                <div class="row justify-content-center">
                    <div id="map"></div>
                </div>
            </div>
        </div>
        <div class="row justify-content-center">
            <router-link :to="`/servicios/`" class="btn btn-lg btn-dark col-lg-6">Volver a Servicios</router-link>
        </div>
    </div>
    <br>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'leaflet/dist/leaflet.css';
import leaflet from 'leaflet';

const baseURL = import.meta.env.VITE_BACKEND_BASE_URL;

export default {
    data(){        
        return {
            service: [],
            institution: [], 
        };
    },

    methods: {
        async fetchService(serviceId) {
            try {
                const response = await axios.get(`${baseURL}/services/api/services/${serviceId}`);
                this.service = response.data;
                this.fetchInstitution(response.data.laboratory);
            }
            catch (error) {
                console.error('Error al obtener los datos:', error);
            }        
        },
        
        async createRequest() {
            const token = localStorage.getItem('token');
            if (!token) {
                Swal.fire({
                    title: 'Error',
                    text: 'Debes estar autenticado para crear una solicitud',
                    icon: 'error',
                    confirmButtonColor: '#0d6efd'
                }).then(() => {
                    this.$router.push({ name: 'iniciarSesion' }); 
                });
                return;
            }

            try {    
                Swal.fire({
                    title: '¡Gracias!',
                    html: `
                <label>Institución:<input id="swal-input1" class="swal2-input" value="${this.institution.name}" readonly></label>
                <label>Servicio:<input id="swal-input2" class="swal2-input" value="${this.service.name}" readonly></label>
                <textarea id="swal-input3" class="swal2-textarea" placeholder="Escribe tu comentario aquí (opcional)"></textarea>
            `,
                    focusConfirm: false,
                    preConfirm: () => {
                        return [
                            document.getElementById('swal-input1').value,
                            document.getElementById('swal-input2').value,
                            document.getElementById('swal-input3').value
                        ]
                    }
                }).then(async (result) => {
                    if (result.isConfirmed) {
                        const [institutionName, serviceName, comment] = result.value;

                        await axios.post(`${baseURL}/services/api/me/requests`, {
                            service_id: this.$route.params.id,
                            user_id: null,
                            comments: comment,
                        }, {
                            headers: {
                                'Authorization': `JWT ${token}`
                            }
                        });

                        Swal.fire({
                            icon: 'success',
                            title: '¡Solicitud creada con éxito!',
                            confirmButtonText: 'OK'
                        });
                    }
                });
            } catch (error) {
                Swal.fire({
                    title: 'Error',
                    text: 'Tu solicitud no ha sido creada correctamente',
                    icon: 'error',
                    confirmButtonColor: '#0d6efd'
                }).then(() => {
                    this.$router.push({ name: 'iniciarSesion' });
                });
            }
        },
        async fetchInstitution(laboratoryId) {
            try {
                const response = await axios.get(`${baseURL}/institutions/api/institution/${laboratoryId}`);
                this.institution = response.data;
                this.initializeMap()
            }
            catch (error) {
                console.error('Error al obtener los datos:', error);
            }        
        },

        initializeMap() {
            // Coordenadas para centrar el mapa
            const lat = this.institution.location.latitude;
            const lon = this.institution.location.longitude;

            // Crea el mapa y lo coloca en el div con id 'map'
            const map = leaflet.map('map').setView([lat, lon], 13);

            // Añade la capa de OpenStreetMap al mapa
            leaflet.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
                    }).addTo(map);

            // Añade un marcador en las coordenadas dadas
            leaflet.marker([lat, lon]).addTo(map)
                .bindPopup('<div style="text-align: center;">' + this.institution.name + '<br>' + this.institution.address + '</div>')
                .openPopup();
        }
    },

    created() {
        this.fetchService(this.$route.params.id);
    },
}
</script>

<style scoped>
    #map {
        height: 400px;
    }
</style>