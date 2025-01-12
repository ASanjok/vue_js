from __future__ import absolute_import, unicode_literals
import os
from celery import shared_task
from kombu import Connection, exceptions
import json
from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)


# Настройка подключения к RabbitMQ
RABBITMQ_URL = 'amqp://admin:Password1234@localhost:5672/'
QUEUE_NAME = 'to_django_requests'


# @shared_task
# def consume_messages_from_rabbitmq():
#     """
#     Задача для потребления сообщений из RabbitMQ.
#     """
#     with Connection(RABBITMQ_URL) as conn:
#         logger.info("Connected to RabbitMQ successfully")
#         queue = conn.SimpleQueue(QUEUE_NAME)

#         while True:
#             try:
#                 message = queue.get(block=True, timeout=10)
#                 logger.info(f"Received message: {message.payload}")

#                 # Передача сообщения на обработку
#                 process_message_from_rabbitmq.delay(message.payload)
#                 message.ack()

#             except exceptions.Empty:
#                 logger.info("Queue is empty, waiting for new messages...")

#             except Exception as e:
#                 logger.info(f"Error processing message: {e}")


@shared_task
def process_message_from_rabbitmq(json_message):
    from django.contrib.gis.geos import Point
    from .models import PositionData, Place
    """
    Обработка сообщения из RabbitMQ.
    """
    logger.info(f"Processing message: {json_message}")

    try:
        dict_message = json.loads(json_message)

        orderedDictPlace = OrderedDict()
        orderedDictPositionData = OrderedDict()

        orderedDictPlace['place_name'] = dict_message['place_name']
        orderedDictPlace['time_received'] = dict_message['time_received']
        orderedDictPlace['plane_distance'] = dict_message['Plane_distance']
        orderedDictPlace['PositionData'] = None

        # Convert strings to float for Point
        orderedDictPositionData['position'] = Point(
            float(dict_message['Position_longitude']), float(dict_message['Position_latitude'])
        )
        orderedDictPositionData['altitude'] = dict_message['Altitude']
        orderedDictPositionData['speed'] = dict_message['Speed']
        orderedDictPositionData['track'] = dict_message['Track']
        orderedDictPositionData['rc'] = dict_message['Rc']
        orderedDictPositionData['epu'] = dict_message['EPU']
        orderedDictPositionData['vepu'] = dict_message['VEPU']
        orderedDictPositionData['hfomr'] = dict_message['HFOMr']
        orderedDictPositionData['vfomr'] = dict_message['VFOMr']
        orderedDictPositionData['hex_code'] = dict_message['HEX']
        orderedDictPositionData['icao_id'] = dict_message['ICAO']
        orderedDictPositionData['call_sign'] = dict_message['Callsign']

        # Save PositionData and Place
        position_data, created = PositionData.objects.get_or_create(
            hex_code=orderedDictPositionData['hex_code'],
            defaults=orderedDictPositionData
        )

        Place.objects.create(
            place_name=orderedDictPlace['place_name'],
            time_received=orderedDictPlace['time_received'],
            plane_distance=orderedDictPlace['plane_distance'],
            PositionData=position_data  # Corrected field name here
        )

        # logger.info("Processed and saved position data successfully.")
        return "completed"

    except Exception as e:
        logger.info(f"Error: {e}")