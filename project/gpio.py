# copied and changed from: https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import Adafruit_DHT
from .settings import get_settings, set_settings
from .common import export_log, log_text
import time
import requests
import datetime

def safe_data(humidity, temperature_c):
    try:
        row = [
            datetime.datetime.fromtimestamp(
                time.time()).strftime('%Y-%m-%d %H:%M:%S'),
            "{:.1f}".format(humidity),
            "{:.1f}".format(temperature_c)
        ]
        header = ["Timestamp", "Humidity [%]", "Temperature [C]"]

        # Log
        export_log(row, header)
    except Exception as e:
        message = "Failed to save data in csv:"
        for arg in e.args:
            message += "\n"+ arg
        log_text(message)


def send_data():
    """Read data from Pin and send request to server.
    Safes data in csv. file, when error occured
    """

    # Initial the dht device, with data pin connected to:
    settings = get_settings()
    PIN = settings.get('pin')
    SERVER_URL =settings.get('server_base_url')
    DHT_DEVICE = Adafruit_DHT.DHT22  # DHT22 is simular to AM2302


    # Read temperature from method
    humidity, temperature_c = Adafruit_DHT.read_retry(DHT_DEVICE, PIN)

    data = {
        'humid_perc': humidity,
        'temp_in_deg': temperature_c,
    }

    # Add Sensor to 
    if settings.get('sensor') != None:
        data['sensor'] = settings.get('sensor')

    try:
        responce = requests.post(SERVER_URL + '/api/entries/', json=data, timeout=2.5)

        if responce.status_code == 201:
            # See if Sensor was initialised
            sensor = responce.json().get('sensor')

            if sensor != None and settings.get('sensor') != sensor:
                # sensor was changed
                settings['sensor'] = sensor
                set_settings(settings)

        else:
            # Safe data in csv file, as data was not send
            log_text("Failed to init sensort. Responce: " + responce.reason + "\n" + responce.text)
            safe_data(humidity, temperature_c)
            
    except Exception as e:
        # Safe data in csv file, as data was not send
        safe_data(humidity, temperature_c)

        message = "Failed to make request:"
        for arg in e.args:
            message += "\n" + arg
        log_text(message)
