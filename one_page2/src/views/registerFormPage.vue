<template>
    <div class="d-flex justify-content-center align-items-center" style="height: 100vh; background-color: #f8f9fa;">
        <b-card class="p-4" style="width: 400px;">
            <h4 class="text-center mb-4">Reģistracija</h4>

            <!-- Registration form -->
            <form @submit.prevent="register">
                <b-form-group label="Lietotājvārds" label-for="lietotājvārds">
                    <b-form-input v-model="form.username" type="text" id="username" required></b-form-input>
                </b-form-group>

                <b-form-group label="E-pasts" label-for="e-pasts">
                    <b-form-input v-model="form.email" type="email" id="email" required></b-form-input>
                </b-form-group>

                <b-form-group label="Parole" label-for="parole">
                    <b-form-input v-model="form.password" type="password" id="password" required></b-form-input>
                </b-form-group>

                <b-button type="submit" variant="primary" block>Reģistrēties</b-button>
            </form>

            <!-- Link to login page -->
            <div class="mt-3 text-center">
                <p>Jau ir konts?</p>
                <b-button variant="link" @click="goToLogin">Pieteikties</b-button>
            </div>

            <!-- Show registration error message -->
            <p v-if="error" class="text-danger text-center mt-3">{{ error }}</p>
        </b-card>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            form: {
                username: '',
                email: '',
                password: ''
            },
            error: ''
        };
    },
    methods: {
        // Submit registration data to API
        async register() {
            try {
                await axios.post('http://localhost:8000/api/register/', this.form);

                // On successful registration, redirect to login page
                this.$router.push('/login');
            } catch (err) {
                // Show generic error message on failure
                this.error = 'Registration failed. Please try again.';
            }
        },
        // Navigate user to login page
        goToLogin() {
            this.$router.push('/login');
        }
    }
};
</script>
