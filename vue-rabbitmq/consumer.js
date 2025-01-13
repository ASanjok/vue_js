const express = require('express');
const bodyParser = require('body-parser');
const amqp = require('amqplib');
const WebSocket = require('ws');
const cors = require('cors');

const app = express();
app.use(bodyParser.json());
app.use(cors());

// Настройка WebSocket-сервера поверх HTTP-сервера Express
const server = require('http').createServer(app);
const wss = new WebSocket.Server({ server });

let channel; // Канал RabbitMQ
let hasClients = false; // Указывает, есть ли подключённые клиенты WebSocket

// Отправка сообщений в RabbitMQ
async function sendToQueue(queue, message) {
    try {
        const connection = await amqp.connect('amqp://admin:Password1234@localhost:5672');
        const channel = await connection.createChannel();
        await channel.assertQueue(queue, { durable: true });

        channel.sendToQueue(queue, Buffer.from(message));
        console.log('Message sent:', message);

        await channel.close();
        await connection.close();
    } catch (error) {
        console.error('Error sending message to RabbitMQ:', error);
    }
}

// Маршрут для отправки сообщений в RabbitMQ
app.post('/sendMessage', async (req, res) => {
    const { queue, message } = req.body;

    if (!queue || !message) {
        return res.status(400).send({ error: 'Queue and message are required' });
    }

    try {
        await sendToQueue(queue, message);
        res.status(200).send({ status: 'Message sent successfully' });
    } catch (error) {
        res.status(500).send({ error: 'Failed to send message to RabbitMQ' });
    }
});




// Получение данных из RabbitMQ
async function startConsuming() {
    if (channel && hasClients) {
        console.log("Starting to consume messages...");
        channel.consume('to_django_data', (msg) => {
            if (msg !== null) {
                console.log(" [x] Received %s", msg.content.toString());

                const message = msg.content.toString();

                wss.clients.forEach(client => {
                    if (client.readyState === WebSocket.OPEN) {
                        client.send(JSON.stringify(message));
                    }
                });

                channel.ack(msg);
            }
        }, { noAck: false });
    }
}

// WebSocket-события для обработки подключений
wss.on('connection', (ws) => {
    console.log("WebSocket client connected");
    hasClients = true;

    startConsuming();

    ws.on('close', () => {
        console.log("WebSocket client disconnected");
        hasClients = [...wss.clients].some(client => client.readyState === WebSocket.OPEN);
    });

    ws.on('message', (message) => {
        console.log(`WebSocket received: ${message}`);
    });
});

// Подключение к RabbitMQ
amqp.connect('amqp://admin:Password1234@localhost:5672')
    .then(connection => connection.createChannel())
    .then(ch => {
        channel = ch;
        return channel.assertQueue('to_django_data', { durable: true });
    })
    .then(() => {
        console.log("Connected to RabbitMQ, waiting for clients...");
    })
    .catch(error => {
        console.error("Failed to connect to RabbitMQ:", error);
    });

// Запуск HTTP и WebSocket-сервера
server.listen(8081, () => {
    console.log(`HTTP and WebSocket server running on http://localhost:8081`);
});
