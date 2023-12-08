<template>
    <div id="login-container">
        <div class="login-box">
            <h2>Registro</h2>
            <form @submit.prevent="register">
                <label for="name">Nombre:</label>
                <input v-model="name" type="text" id="name" required>

                <label for="lastname">Apellido:</label>
                <input v-model="lastname" type="text" id="lastname" required>

                <label for="username">Usuario:</label>
                <input v-model="username" type="text" id="username" required>

                <label for="email">Correo electrónico:</label>
                <input v-model="email" type="email" id="email" required>

                <label for="password">Contraseña:</label>
                <input v-model="password" type="password" id="password" required>

                <button type="submit">Registrarse</button>
            </form>
        </div>
    </div>
</template>
  
<script>
import axios from 'axios';

const baseURL = import.meta.env.VITE_BACKEND_BASE_URL;


export default {
    data() {
        return {
            name: '',
            lastname: '',
            username: '',
            email: '',
            password: '',
        };
    },
    // En tu componente de Vue.js
    methods: {
        async register() {
            try {
                const response = await axios.post(
                    `${baseURL}/registro`,
                    {
                        name: this.name,
                        lastname: this.lastname,
                        username: this.username,
                        email: this.email,
                        password: this.password,
                    },
                    {
                        headers: {
                            'Content-Type': 'application/json', 
                        },
                    }
                );

                if (response.data.success) {
                    // Registro exitoso
                    alert(response.data.message);
                    // falta redirigir
                } else {
                    // Error en el registro
                    alert(response.data.errors.join(', '));
                }
            } catch (error) {
                console.error('Error en el registro:', error);
            }
        },
    },
}
</script>
  
<style scoped>
/* Estilos específicos del componente */

/* Estilos base que se aplicarán en todas las pantallas */
#login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    /* Opcional: Ajusta la altura según tus necesidades */
}

.login-box {
    background-color: #fff;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    padding: 20px;
    width: 300px;
}

h2 {
    margin-bottom: 20px;
    color: #333;
}

form {
    text-align: left;
}

label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

input[type="text"],
input[type="password"],
input[type="email"] {
    width: 100%;
    border: 1px solid #ccc;
    border-radius: 4px;
}

button[type="submit"] {
    width: 100%;
    margin-top: 2%;
    padding: 10px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

button[type="submit"]:hover {
    background-color: #0056b3;
}

/* Media Query para pantallas con resolución menor a 768px */
@media (max-width: 767px) {

    /* Estilos adicionales para pantallas más pequeñas */
    h2 {
        font-size: 1.5em;
    }

    label,
    input[type="text"],
    input[type="password"],
    input[type="email"],
    button[type="submit"] {
        margin-top: 10px;
    }

    .login-box {
        width: 80%;
        /* Ajusta el ancho del contenedor en dispositivos móviles (cambia el valor según sea necesario) */
    }
}
</style>
  