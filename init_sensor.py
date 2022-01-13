# Obsolete version

import requests
from project.common import log_text
from project.settings import get_settings, set_settings

# Get data from settings
settings = get_settings()
base_url = settings.get('server_base_url')
init = settings.get('sensor').get('init')

responce = requests.post(base_url+"/api/sensors/", json=init, timeout=2.5)

# If code is created
if responce.status_code == 201:
    settings.get('sensor')['id'] = responce.json().get('id')
    set_settings(settings)
    log_text("Sensor was created successffully")

else:
    log_text("Failed to init sensort. Responce: " + responce.reason + "\n" + responce.text)