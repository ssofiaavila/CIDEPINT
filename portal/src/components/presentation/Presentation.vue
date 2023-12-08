<template>
    <div class="carousel-container" @wheel="handleWheel">
        <div class="carousel" :style="{ transform: `translateY(-${currentIndex * 100}vh)` }">
            <div class="slide" v-for="(slide, index) in slides" :key="index">
                <img :src="slide.img" class="img-fluid body-circle-logo"/>
                <h2>{{ slide.title }}</h2>
                <p>{{ slide.description }}</p>
            </div>
            <div class="slide">
                <div id="carouselExample" class="carousel slide">
                    <img src="../../assets/img/institutions.png" class="img-fluid body-circle-logo">
                    <h2>Servicio/s por institución</h2>
                    <div class="carousel-inner">
                        <div v-for="(institution, index) in servicesPerInstitution" :key="institution.id"
                            :class="{ 'carousel-item': true, 'active': index == 0 }">
                            <h3>{{ institution.name }}</h3>
                            <ul>
                                <li v-for="service in institution.services" :key="service.name">
                                    {{ service.name }} - {{ service.description }}
                                </li>
                            </ul>
                        </div>
                    </div>
                    <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample"
                        data-bs-slide="prev">
                        <span class="carousel-control-prev-icon bg-black" aria-hidden="true"></span>
                        <span class="visually-hidden">Previous</span>
                    </button>
                    <button class="carousel-control-next" type="button" data-bs-target="#carouselExample"
                        data-bs-slide="next">
                        <span class="carousel-control-next-icon bg-black" aria-hidden="true"></span>
                        <span class="visually-hidden">Next</span>
                    </button>
                </div>  
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import searchImage from '../../assets/img/search.png'
import servicesImage from '../../assets/img/services.png'

const baseURL = import.meta.env.VITE_BACKEND_BASE_URL;


export default {
    data() {
        return {
            currentIndex: 0,
            slides: [
                { img: searchImage,title: 'Busqueda de servicios', description: 'Busca los servicios que necesites contratar en un solo lugar.' },
                { img: servicesImage,title: 'Solicita servicios de forma Rápida y fácil.', description: 'Accede al listado de servicios, selecciona el que estés necesitando, realiza una solicitud y monitorea la confirmación de la misma, todo en un mismo portal.' },
            ],
            servicesPerInstitution: [],
            isLoading: true,
            error: null,
        };
    },
    methods: {
        showSlide(index) {
            this.currentIndex = index;
        },
        handleWheel(event) {
            if (event.deltaY > 0 && this.currentIndex < 2) {
                this.showSlide(this.currentIndex + 1);
            } else if (event.deltaY < 0 && this.currentIndex > 0) {
                this.showSlide(this.currentIndex - 1);
            }
        },
    },
    async created() {
        try {
            const response = await axios.get(`${baseURL}/institutions/api/servicesList`);
            this.servicesPerInstitution = response.data;
        } catch (error) {
            this.error = error.message;
        } finally {
            this.isLoading = false;
        }
    },
};
</script>

<style scoped src="../../assets/presentation/homePresentation.css"></style>
