<template>
    <div class="container mt-4">
        <b-card title="Account Information" class="shadow-sm">
            <b-card-body>
                <!-- Show user data if loaded -->
                <div v-if="userData">
                    <b-row v-for="(value, key) in accountFields" :key="key">
                        <b-col md="4">
                            <b-card-text><strong>{{ value.label }}:</strong></b-card-text>
                        </b-col>
                        <b-col md="8">
                            <b-card-text>{{ userData[key] }}</b-card-text>
                        </b-col>
                    </b-row>
                    
                    <!-- Buttons to open modals -->
                    <b-button variant="primary" class="mt-3" @click="showEditModal = true">Edit</b-button>
                    <b-button variant="danger" class="mt-3 ml-2" @click="showDeleteModal = true">Delete</b-button>
                </div>
                <!-- Loading state -->
                <div v-else>
                    <b-alert variant="info" show>
                        Loading account information...
                    </b-alert>
                </div>
            </b-card-body>
        </b-card>
        
        <!-- Edit Account Modal -->
        <b-modal v-model="showEditModal" title="Edit Account" hide-footer>
            <b-form @submit.prevent="updateAccount">
                <b-form-group label="First Name">
                    <b-form-input v-model="editData.first_name"></b-form-input>
                </b-form-group>
                <b-form-group label="Last Name">
                    <b-form-input v-model="editData.last_name"></b-form-input>
                </b-form-group>
                <b-form-group label="Email">
                    <b-form-input type="email" v-model="editData.email"></b-form-input>
                </b-form-group>
                <b-button type="submit" variant="success">Save</b-button>
                <b-button variant="secondary" class="ml-2" @click="showEditModal = false">Cancel</b-button>
            </b-form>
        </b-modal>
        
        <!-- Delete Account Confirmation Modal -->
        <b-modal v-model="showDeleteModal" title="Delete Account" hide-footer>
            <p>Are you sure you want to delete your account?</p>
            <b-button variant="danger" @click="deleteAccount">Delete</b-button>
            <b-button variant="secondary" class="ml-2" @click="showDeleteModal = false">Cancel</b-button>
        </b-modal>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            userData: null,          // Stores fetched user info
            showEditModal: false,    // Controls edit modal visibility
            showDeleteModal: false,  // Controls delete modal visibility
            editData: {              // Form data for editing
                first_name: '', 
                last_name: '', 
                email: '' 
            },
            accountFields: {         // Fields to display on account info card
                username: { label: 'Username' },
                email: { label: 'Email' },
            }
        };
    },
    mounted() {
        this.fetchAccountInfo();    // Fetch user info on component load
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
                    this.editData = { ...this.userData };  // Initialize edit form with current data
                })
                .catch(error => {
                    console.error('Error fetching account data:', error);
                    this.$router.push('/login'); // Redirect if error occurs (e.g. unauthorized)
                });
            }
        },
        updateAccount() {
            const token = localStorage.getItem('authToken');
            axios.put('http://localhost:8000/api/account/', this.editData, {
                headers: { Authorization: `Bearer ${token}` }
            })
            .then(() => {
                this.fetchAccountInfo();  // Refresh data after update
                this.showEditModal = false;  // Close modal
            })
            .catch(error => console.error('Error updating account:', error));
        },
        deleteAccount() {
            const token = localStorage.getItem('authToken');
            axios.delete('http://localhost:8000/api/account/', {
                headers: { Authorization: `Bearer ${token}` }
            })
            .then(() => {
                localStorage.removeItem('authToken');  // Clear token on delete
                this.$router.push('/login');            // Redirect to login
            })
            .catch(error => console.error('Error deleting account:', error));
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
