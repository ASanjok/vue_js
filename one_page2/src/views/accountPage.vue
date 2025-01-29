<template>
    <div class="container mt-4">
        <b-card title="Account Information" class="shadow-sm">
            <b-card-body>
                <div v-if="userData">
                    <b-row>
                        <b-col md="4">
                            <b-card-text><strong>Username:</strong></b-card-text>
                        </b-col>
                        <b-col md="8">
                            <b-card-text>{{ userData.username }}</b-card-text>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col md="4">
                            <b-card-text><strong>Email:</strong></b-card-text>
                        </b-col>
                        <b-col md="8">
                            <b-card-text>{{ userData.email }}</b-card-text>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col md="4">
                            <b-card-text><strong>First Name:</strong></b-card-text>
                        </b-col>
                        <b-col md="8">
                            <b-card-text>{{ userData.first_name }}</b-card-text>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col md="4">
                            <b-card-text><strong>Last Name:</strong></b-card-text>
                        </b-col>
                        <b-col md="8">
                            <b-card-text>{{ userData.last_name }}</b-card-text>
                        </b-col>
                    </b-row>
                </div>
                <div v-else>
                    <b-alert variant="info" show>
                        Loading account information...
                    </b-alert>
                </div>
            </b-card-body>
        </b-card>
    </div>
</template>

<script>
import axios from 'axios';
import { BCard, BCardText, BRow, BCol, BAlert } from 'bootstrap-vue';

export default {
    components: {
        BCard,
        BCardText,
        BRow,
        BCol,
        BAlert,
    },
    data() {
        return {
            userData: null,
        };
    },
    mounted() {
        this.fetchAccountInfo();
    },
    methods: {
        fetchAccountInfo() {
            const token = localStorage.getItem('authToken');
            if (token) {
                axios
                    .get('http://localhost:8000/api/account/', {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    })
                    .then((response) => {
                        this.userData = response.data;
                    })
                    .catch((error) => {
                        console.error('Error fetching account data:', error);
                        this.$router.push('/login'); // Перенаправление на страницу логина, если ошибка
                    });
            }
        },
    },
};
</script>

<style scoped>
.container {
    max-width: 800px;
    margin-top: 20px;
}
</style>