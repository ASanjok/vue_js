<template>
    <div>
        <b-button @click="sendMessage()">Send Message</b-button>
        <div v-if="message">
            <p>Received Message: {{ message }}</p>
        </div>
    </div>
</template>

<script>
/* eslint-disable */

export default {
    data() {
        return {
            message: null, 
            data: {
                queue: "to_django_requests",
                message: "get_flight_data"
            },
            socket: null, 
        };
    },
    created() {
        this.setupWebSocket(); 
    },
    methods: {
        
        setupWebSocket() {
            this.socket = new WebSocket('ws://localhost:8080'); 

            this.socket.onopen = () => {
                console.log('WebSocket connected');
            };

            
            this.socket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                console.log('Received data:', data);
                this.message = data.message; 
            };

            this.socket.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
        },

        
        sendMessage() {
            fetch('http://localhost:3000/sendMessage', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    queue: this.data.queue,
                    message: this.data.message,
                }),
            })
            .then(response => response.json())
            .then(data => {
                console.log('Request sent:', data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        },
    },
};
</script>
