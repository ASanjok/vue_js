from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.contrib.gis.geos import Point
from .models import PositionData, Place
import json
import logging

logger = logging.getLogger(__name__)

# Буферы для накопления данных
position_data_buffer = []
place_buffer = []

# Лимит сообщений для batch-сохранения
BATCH_SIZE = 50


@shared_task
def process_message_from_rabbitmq(json_message):
    """
    Обработка сообщения из RabbitMQ с накоплением данных для batch-сохранения.
    """
    global position_data_buffer, place_buffer

    try:
        dict_message = json.loads(json_message)

        # Создаём объект PositionData
        position_data = PositionData(
            position=Point(
                float(dict_message['Position_longitude']),
                float(dict_message['Position_latitude'])
            ),
            altitude=dict_message['Altitude'],
            speed=dict_message['Speed'],
            track=dict_message['Track'],
            rc=dict_message['Rc'],
            epu=dict_message['EPU'],
            vepu=dict_message['VEPU'],
            hfomr=dict_message['HFOMr'],
            vfomr=dict_message['VFOMr'],
            hex_code=dict_message['HEX'],
            icao_id=dict_message['ICAO'],
            call_sign=dict_message['Callsign']
        )

        # Создаём объект Place
        place = Place(
            place_name=dict_message['place_name'],
            time_received=dict_message['time_received'],
            plane_distance=dict_message['Plane_distance'],
            PositionData=position_data  # Связываем с объектом PositionData
        )

        # Добавляем объекты в буферы
        position_data_buffer.append(position_data)
        place_buffer.append(place)

        # Если буфер заполнен, выполняем сохранение
        if len(position_data_buffer) >= BATCH_SIZE:
            save_buffers_to_database()

        return "completed"

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return f"Error: {e}"


def save_buffers_to_database():
    """
    Сохраняет накопленные данные из буферов в базу данных.
    """
    global position_data_buffer, place_buffer

    try:
        # Сохраняем PositionData
        PositionData.objects.bulk_create(position_data_buffer, ignore_conflicts=True)

        # Обновляем ссылки в Place
        for place in place_buffer:
            # Ищем сохранённый объект PositionData по hex_code
            matching_position = PositionData.objects.get(hex_code=place.PositionData.hex_code)
            place.PositionData = matching_position

        # Сохраняем Place
        Place.objects.bulk_create(place_buffer)

        # Очищаем буферы
        position_data_buffer = []
        place_buffer = []

        logger.info("Batch saved successfully.")

    except Exception as e:
        logger.error(f"Error saving batch to database: {e}")
