<template>
    <div class="container mt-4">
        <b-card title="Account Information" class="shadow-sm">
            <b-card-body>
                <div v-if="userData">
                    <b-row v-for="(value, key) in accountFields" :key="key">
                        <b-col md="4">
                            <b-card-text><strong>{{ value.label }}:</strong></b-card-text>
                        </b-col>
                        <b-col md="8">
                            <b-card-text>{{ userData[key] }}</b-card-text>
                        </b-col>
                    </b-row>
                    
                    <b-button variant="primary" class="mt-3" @click="showEditModal = true">Редактировать</b-button>
                    <b-button variant="danger" class="mt-3 ml-2" @click="showDeleteModal = true">Удалить</b-button>
                </div>
                <div v-else>
                    <b-alert variant="info" show>
                        Loading account information...
                    </b-alert>
                </div>
            </b-card-body>
        </b-card>
        
        <!-- Модальное окно редактирования -->
        <b-modal v-model="showEditModal" title="Редактирование аккаунта" hide-footer>
            <b-form @submit.prevent="updateAccount">
                <b-form-group label="Имя">
                    <b-form-input v-model="editData.first_name"></b-form-input>
                </b-form-group>
                <b-form-group label="Фамилия">
                    <b-form-input v-model="editData.last_name"></b-form-input>
                </b-form-group>
                <b-form-group label="Email">
                    <b-form-input type="email" v-model="editData.email"></b-form-input>
                </b-form-group>
                <b-button type="submit" variant="success">Сохранить</b-button>
                <b-button variant="secondary" class="ml-2" @click="showEditForm = false">Отмена</b-button>
            </b-form>
        </b-modal>
        
        <!-- Модальное окно подтверждения удаления -->
        <b-modal v-model="showDeleteModal" title="Удаление аккаунта" hide-footer>
            <p>Вы уверены, что хотите удалить свой аккаунт? Это действие необратимо.</p>
            <b-button variant="danger" @click="deleteAccount">Удалить</b-button>
            <b-button variant="secondary" class="ml-2" @click="showDeleteModal = false">Отмена</b-button>
        </b-modal>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            userData: null,
            showEditModal: false,
            showDeleteModal: false,
            editData: { first_name: '', last_name: '', email: '' },
            accountFields: {
                username: { label: 'Username' },
                email: { label: 'Email' },
                first_name: { label: 'First Name' },
                last_name: { label: 'Last Name' }
            }
        };
    },
    mounted() {
        this.fetchAccountInfo();
    },
    methods: {
        fetchAccountInfo() {
            const token = localStorage.getItem('authToken');
            if (token) {
                axios.get('http://localhost:8000/api/account/', {
                    headers: { Authorization: `Bearer ${token}` }
                })
                .then(response => {
                    this.userData = response.data;
                    this.editData = { ...this.userData };
                })
                .catch(error => {
                    console.error('Ошибка при получении данных аккаунта:', error);
                    this.$router.push('/login');
                });
            }
        },
        updateAccount() {
            const token = localStorage.getItem('authToken');
            axios.put('http://localhost:8000/api/account/', this.editData, {
                headers: { Authorization: `Bearer ${token}` }
            })
            .then(() => {
                this.fetchAccountInfo();
                this.showEditModal = false;
            })
            .catch(error => console.error('Ошибка обновления данных:', error));
        },
        deleteAccount() {
            const token = localStorage.getItem('authToken');
            axios.delete('http://localhost:8000/api/account/', {
                headers: { Authorization: `Bearer ${token}` }
            })
            .then(() => {
                localStorage.removeItem('authToken');
                this.$router.push('/login');
            })
            .catch(error => console.error('Ошибка при удалении аккаунта:', error));
        }
    }
};
</script>

<style scoped>
.container {
    max-width: 800px;
    margin-top: 20px;
}
</style>
