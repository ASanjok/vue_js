// sender.js
const amqp = require('amqplib/callback_api');
const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());


function sendMessageToQueue(queue, message) {
    amqp.connect('amqp://admin:Password1234@localhost:5672', function (error0, connection) {
        if (error0) {
            console.error('Failed to connect to RabbitMQ:', error0);
            return;
        }
        connection.createChannel(function (error1, channel) {
            if (error1) {
                console.error('Failed to create channel:', error1);
                return;
            }
            
            channel.sendToQueue(queue, Buffer.from(message));
            console.log(" [x] Sent '%s' to queue '%s'", message, queue);
        });

        setTimeout(() => {
            connection.close();
        }, 500);
    });
}


app.post('/sendMessage', (req, res) => {
    const { queue, message } = req.body;
    if (!queue || !message) {
        return res.status(400).json({ error: 'Both "queue" and "message" are required.' });
    }

    sendMessageToQueue(queue, message);
    res.json({ status: 'Message sent to RabbitMQ', queue, message });
});

app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});