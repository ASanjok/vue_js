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
            socketget: null,
            socketsend: null,
        };
    },
    created() {
        this.setupWebSocket();
    },
    methods: {

        setupWebSocket() {
            this.socketget = new WebSocket('ws://localhost:8081');

            this.socketget.onopen = () => {
                console.log('WebSocket connected');
            };


            this.socketget.onmessage = (event) => {
                const data = JSON.parse(event.data);
                console.log('Received data:', data);
                this.message = data.message;
            };

            this.socketget.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
        },


        sendMessage() {
            fetch('http://localhost:8081/sendMessage', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    queue: this.data.queue, // Имя очереди
                    message: this.data.message, // Сообщение
                }),
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Message sent:', data);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        },
    },
};
</script>
