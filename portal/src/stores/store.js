import { ref } from 'vue';

export const isAuthenticated = ref(false);

export function setAuthentication(status) {
    isAuthenticated.value = status;
}