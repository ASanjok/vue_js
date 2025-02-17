from kombu import Connection, exceptions
from queue import Empty 
from first_part.tasks import process_message_from_rabbitmq


def consume_messages_from_rabbitmq():
    with Connection('amqp://celery:celery@rabbitmq:5672') as conn:
        print("Connected to RabbitMQ successfully")
        queue = conn.SimpleQueue('to_django_data')

        while True:
            try:
                message = queue.get(block=True, timeout=10)
                print(f"Received message: {message.payload}")


                message.ack()

            except Empty:
                print("Queue is empty, waiting for new messages...")
                continue

            except Exception as e:
                print(f"Error processing message: {e}")
                continue

            try:
                process_message_from_rabbitmq.delay(message.payload)
            except Exception as e:
                print(f"-------------------------: {e}")

consume_messages_from_rabbitmq()