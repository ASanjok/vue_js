from celery import shared_task

@shared_task
def process_message_from_rabbitmq(message):
    print(f"Processing message: {message}")