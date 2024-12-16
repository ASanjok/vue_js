from celery import shared_task
import json
import pika
from .models import PositionData

from firstApp.views import FlightsGetAllAPIView

@shared_task
def process_message(message):
    print("message in django recieved")
    try:
        data = json.loads(message) 
        
        if data == 'get_flight_data':
            flight_data = {"altitude":"45500", "speed":"1002"}

            send_to_rabbitmq('to_vue_data', flight_data)

            return {"status": "Data sent to RabbitMQ"}
        
        elif data == 'ping':
            return {"response": "pong"}
        
        else:
            return {"error": "Unknown action"}
    except Exception as e:
        return {"error": str(e)} 