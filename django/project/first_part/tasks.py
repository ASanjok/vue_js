from __future__ import absolute_import, unicode_literals
from celery import shared_task
import json
from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)

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