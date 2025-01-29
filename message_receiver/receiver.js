const amqp = require('amqplib');
const express = require('express');
const ws = require('ws');
const app = express();
const serverWS = new ws.Server({ port: 8082 });; 

app.use(express.json()); // Для обработки текстового тела запроса

const RABBITMQ_URL = 'amqp://admin:Password1234@localhost:5672';
const QUEUE_NAME = 'to_django_data';

let channel; // Переменная для хранения канала

// Инициализация подключения и канала RabbitMQ
async function initializeRabbitMQ() {
    // try {
    //     const connection = await amqp.connect(RABBITMQ_URL);
    //     channel = await connection.createChannel();

    //     // Убедимся, что очередь существует
    //     await channel.assertQueue(QUEUE_NAME, {
    //         durable: true, // Очередь устойчивая
    //     });

    //     console.log('RabbitMQ connection and channel initialized.');
    // } catch (error) {
    //     console.error('Failed to initialize RabbitMQ:', error);
    //     process.exit(1); // Завершаем процесс, если RabbitMQ недоступен
    // }
}

// Функция для отправки сообщения
async function sendMessageToQueue(message) {
    try {
        if (!channel) {
            throw new Error('RabbitMQ channel is not initialized.');
        }

        // Отправляем сообщение в очередь
        channel.sendToQueue(QUEUE_NAME, Buffer.from(JSON.stringify(message)), {
            persistent: true, // Сообщение сохраняется на диске
        });
        console.log(` [x] Sent message to queue '${QUEUE_NAME}':`);
    } catch (error) {
        console.error('Failed to send message:', error);
    }
}

async function sendMessageToVue(message) {
    try {
        // Отправляем сообщение всем подключенным WebSocket-клиентам
        serverWS.clients.forEach((client) => {
            if (client.readyState === ws.OPEN) {
                const filteredMessage = {
                    Position_latitude: message.Position_latitude,
                    Position_longitude: message.Position_longitude,
                    Callsign: message.Callsign,
                    direction: message.Track
                };
                client.send(JSON.stringify(filteredMessage));
                console.log('Message sent to WebSocket client:', filteredMessage);
            }
        });
    } catch (error) {
        console.error('Failed to send message to WebSocket:', error);
    }
}

// Маршрут для приёма сообщений
app.post('/sendMessage', async (req, res) => {
    const message = req.body;
    // console.log(req)
    // console.log(req.body)

    if (!message) {
        return res.status(400).send('"message" is required in request body.');
    }

    await sendMessageToQueue(message);
    await sendMessageToVue(message);
    res.send('Message sent to RabbitMQ.');
});

// Запуск сервера и RabbitMQ
app.listen(3000, async () => {
    console.log('Server running on http://localhost:3000');
    await initializeRabbitMQ(); // Инициализируем RabbitMQ при запуске
});
