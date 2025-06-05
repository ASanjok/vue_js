const amqp = require('amqplib');
const express = require('express');
const ws = require('ws');
const app = express();
const serverWS = new ws.Server({ port: 8082, host: '0.0.0.0' });; 

app.use(express.json());

const RABBITMQ_URL = 'amqp://admin:Password1234@rabbitmq:5672';
const QUEUE_NAME = 'to_django_data';

let channel;

async function initializeRabbitMQ() {
    try {
        const connection = await amqp.connect(RABBITMQ_URL);
        channel = await connection.createChannel();

        await channel.assertQueue(QUEUE_NAME, {
            durable: true, 
        });

        console.log('RabbitMQ connection and channel initialized.');
    } catch (error) {
        console.error('Failed to initialize RabbitMQ:', error);
        process.exit(1);
    }
}


async function sendMessageToQueue(message) {
    try {
        if (!channel) {
            throw new Error('RabbitMQ channel is not initialized.');
        }
        channel.sendToQueue(QUEUE_NAME, Buffer.from(JSON.stringify(message)), {
            persistent: true, 
        });
        console.log(` [x] Sent message to queue '${QUEUE_NAME}':`);
    } catch (error) {
        console.error('Failed to send message:', error);
    }
}

async function sendMessageToVue(message) {
    try {
        serverWS.clients.forEach((client) => {
            if (client.readyState === ws.OPEN) {
                const filteredMessage = {
                    RC: message.Rc,
                    EPU: message.EPU,
                    HEX_code: message.HEX,
                    ICAO: message.ICAO,
                    VEPU: message.VEPU,
                    HFOMr: message.HFOMr,
                    Speed: message.Speed,
                    Track: message.Track,
                    VFOMr: message.VFOMr,
                    Altitude: message.Altitude,
                    Callsign: message.Callsign,
                    MlatTime: message.mlat_time,
                    PlaceName: message.place_name,
                    TimeReceived: message.time_received,
                    PlaneDistance: message.Plane_distance,
                    Position_latitude: message.Position_latitude,
                    Position_longitude: message.Position_longitude,
                };
                client.send(JSON.stringify(filteredMessage));
                console.log('Message sent to WebSocket client:', filteredMessage);
            }
        });
    } catch (error) {
        console.error('Failed to send message to WebSocket:', error);
    }
}


app.post('/sendMessage', async (req, res) => {
    const message = req.body;

    if (!message) {
        return res.status(400).send('"message" is required in request body.');
    }

    await sendMessageToQueue(message);
    await sendMessageToVue(message);
    res.send('Message sent to RabbitMQ.');
});

app.listen(3000, async () => {
    console.log('Server running on http://localhost:3000');
    await initializeRabbitMQ(); 
});
