const amqp = require('amqplib/callback_api');
const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 8080 });

let channel; 
let hasClients = false; 
const queue = 'to_django_requests'; 


function startConsuming() {
    if (channel && hasClients) {
        console.log("Starting to consume messages...");
        channel.consume(queue, function (msg) {
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
        }, {
            noAck: false
        });
    }
}

wss.on('connection', ws => {
    console.log("Client connected");
    hasClients = true;

    startConsuming();

    ws.on('close', () => {
        console.log("Client disconnected");

        hasClients = [...wss.clients].some(client => client.readyState === WebSocket.OPEN);
    });

    ws.on('message', message => {
        console.log(`Received: ${message}`);
    });
});

amqp.connect('amqp://admin:Password1234@localhost:5672', function (error0, connection) {
    if (error0) {
        throw error0;
    }
    connection.createChannel(function (error1, ch) {
        if (error1) {
            throw error1;
        }
        channel = ch;

        console.log("Connected to RabbitMQ, waiting for clients to start consuming.");
        
        if (hasClients) {
            startConsuming();
        }
    });
});
