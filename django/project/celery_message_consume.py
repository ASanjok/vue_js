from kombu import Connection, exceptions
from queue import Empty 
from first_part.tasks import process_message_from_rabbitmq

def consume_messages_from_rabbitmq():
    # Establish a connection to the RabbitMQ broker
    print("Connecting to RabbitMQ from cekery_message_consume.py...")
    with Connection('amqp://admin:Password1234@rabbitmq:5672') as conn:
        print("Connected to RabbitMQ successfully.")
        
        # Connect to a simple named queue
        queue = conn.SimpleQueue('to_django_data')

        while True:
            try:
                # Try to receive a message from the queue with a timeout
                message = queue.get(block=True, timeout=10)

                # Acknowledge the message to remove it from the queue
                message.ack()

                # Send the payload to the Celery task for processing
                process_message_from_rabbitmq.delay(message.payload)

            except Empty:
                # No message was received within the timeout period
                continue

            except Exception as e:
                # Log any unexpected error during message processing
                print(f"Error processing message: {e}")
                continue

# Start consuming messages
consume_messages_from_rabbitmq()
