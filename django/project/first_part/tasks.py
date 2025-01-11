from celery import shared_task
import json
from .models import PositionData, Place
from collections import OrderedDict
from django.contrib.gis.geos import Point

@shared_task
def process_message_from_rabbitmq(json_message):
    print(f"Processing message: {json_message}")

    dict_message = json.loads(json_message)
    
    try:
        orderedDictPlace = OrderedDict()
        orderedDictPositionData = OrderedDict()

        orderedDictPlace['place_name'] = dict_message['place_Name']
        orderedDictPlace['time_received'] = dict_message['time_received']
        orderedDictPlace['plane_distance'] = dict_message['Plane_distance']
        orderedDictPlace['PositionData'] = None

        orderedDictPositionData['position'] = Point(dict_message['Position_longitude'], dict_message['Position_latitude'])
        orderedDictPositionData['altitude'] = dict_message['Altitude']
        orderedDictPositionData['speed'] = dict_message['Speed']
        orderedDictPositionData['track'] = dict_message['Track']
        orderedDictPositionData['rc'] = dict_message['Rc']
        orderedDictPositionData['epu'] = dict_message['EPU']
        orderedDictPositionData['vepu'] = dict_message['VEPU']
        orderedDictPositionData['hfomr'] = dict_message['HFOMr']
        orderedDictPositionData['vfomr'] = dict_message['VFOMr']
        orderedDictPositionData['hex_code'] = dict_message['HEX']
        orderedDictPositionData['icao'] = dict_message['ICAO']
        orderedDictPositionData['call_sign'] = dict_message['Callsign']

        position_data, created = PositionData.objects.get_or_create(
            hex_code = orderedDictPositionData['hex_code'],
            defaults = orderedDictPositionData
        )

        Place.objects.create(
            place_name = orderedDictPlace['place_name'],
            time_recieved = orderedDictPlace['time_recieved'],
            plane_distance = orderedDictPlace['plane_distance'],
            PositionData = position_data
        )

    except Exception as e:
        print(f"Error: {e}")