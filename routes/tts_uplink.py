from flask import Blueprint, request
from prisma.models import Device, Measurement
from auth import basic_auth

# Url Prefix /tts/uplink
tts_uplink_blueprint = Blueprint('tts_uplink', __name__)

@tts_uplink_blueprint.route('/message', methods=['POST'])
@basic_auth.required
def uplink_message():
    if request.method == 'POST':
        data = request.json
        print(data)

        if data is None:
            return '', 400
        
        try:
            deviceId = data["end_device_ids"]['device_id']
            devEui = data["end_device_ids"]["dev_eui"]

            existing_device = Device.prisma().find_first(where={'deviceID': deviceId})
            if existing_device is None:
                device = Device.prisma().create(
                    data={
                        'deviceID': deviceId,
                        'devEui': devEui
                    }
                )
            else:
                device = existing_device
            print(device)

            payload = data['uplink_message']['decoded_payload']
            batV = payload['BatV']
            humidity = payload['Hum_SHT']
            tempC = payload['TempC_SHT']
            tempCExt = payload['TempC_DS']

            metadata = data['uplink_message']['rx_metadata']
            time = metadata[0]['time']
            rssi = metadata[0]['rssi']
            snr = metadata[0]['snr']

            measurement = Measurement.prisma().create(
                data={
                        'device': { 'connect': { 'id': device.id}},
                        'time': time,
                        'tempC': tempC,
                        'tempCExt': tempCExt,
                        'humidity': humidity,
                        'batteryV': batV,
                        'rssidB': rssi,
                        'snrdB': snr
                },
            )
            print(measurement)
            return '', 201
        except Exception as e:
            print(e)
            return '', 301
