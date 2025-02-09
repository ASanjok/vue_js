<template>
    <div class="d-flex justify-content-center align-items-center" style="height: 100vh; background-color: #f8f9fa;">
        <b-card class="p-4" style="width: 400px;">
            <h4 class="text-center mb-4">Login</h4>
            <form @submit.prevent="login">
                <b-form-group label="Username" label-for="username">
                    <b-form-input v-model="form.username" type="text" id="username" required></b-form-input>
                </b-form-group>

                <b-form-group label="Password" label-for="password">
                    <b-form-input v-model="form.password" type="password" id="password" required></b-form-input>
                </b-form-group>

                <b-button type="submit" variant="primary" block>Login</b-button>
            </form>

            <div class="mt-3 text-center">
                <p>Don't have an account?</p>
                <b-button variant="link" @click="goToRegister">Register</b-button>
            </div>

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
                password: ''
            },
            error: ''
        };
    },
    methods: {
        async login() {
            try {
                const response = await axios.post('http://localhost:8000/api/login/', this.form);
                const token = response.data.access;
                const refreshtoken = response.data.refresh;
                localStorage.setItem('authToken', token);
                localStorage.setItem('refreshToken', refreshtoken)

                // Перенаправление после успешного входа
                this.$router.push('/map');
            } catch (err) {
                this.error = 'Login failed. Please check your credentials.';
            }
        },
        goToRegister() {
            this.$router.push('/register');  // Замените '/register' на путь к странице регистрации
        }
    }
};
</script>