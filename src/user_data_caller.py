import requests
import os
import json

def retieve_data():
    response = requests.get("http://api.swgoh.gg/guild/{0}".format(os.getenv('ID_GREMIO')))
    json_data = json.loads(response.text)
    respuesta = json_data["players"]

    print('--- Datos de jugadores cargados correctamente')
    return respuesta