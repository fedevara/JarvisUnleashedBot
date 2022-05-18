import discord
import os
import requests
import json

from variables import *

client = discord.Client()
players_data = None

###########################################################################

def process_tb_platoon(search_params):
    global players_data
    if (players_data is None):
        print('--- Player data inexistente, cargando Player data')
        response = requests.get("https://swgoh.gg/api/guild/{0}".format(os.getenv('ID_GREMIO')))
        json_data = json.loads(response.text)
        players_data = json_data["players"]

    phase_sectors = TERRITORY_BATTLES[search_params[1]][0]
    for sector in phase_sectors:
        print('--- SECTOR: {0}'.format(sector))
        for platoon in phase_sectors[sector]:
            print('--- PLATOON: {0}'.format(platoon))
            for character in phase_sectors[sector][platoon]:
                phase_sectors[sector][platoon][character] = search_character_by_member(character, search_params[2])

    return (format_response(phase_sectors))

###########################################################################

def search_character_by_member(character, config_given):
    global players_data
    player_selected = None
    min_power = CONFIG_TB["min_power"]
    for member in players_data:
        is_selectable_character = False
        config = CONFIG_TB[config_given]

        for characters in member["units"]:
            iterate_character = characters["data"]
            if (iterate_character["base_id"] == character):
                if (iterate_character["rarity"] >= config and iterate_character["power"] <= min_power):
                    min_power = iterate_character["power"]
                    is_selectable_character = True
                break

        if (player_selected is None or is_selectable_character):
            player_selected = member["data"]["name"]

    if (min_power == CONFIG_TB["min_power"]):
        print("---- {0} no asignado, no hay integrantes del gremio que cumplan las condiciones".format(character))
        return None

    print("---- Asignado: {0} - {1} - Poder {2}".format(character, player_selected, str(min_power)))

    return (player_selected)

###########################################################################

def format_response(response):
  hola = response
  return hola

###########################################################################



###########################################################################

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content_message = message.content
    if content_message.startswith('/search-tbhls-f1'):
        print('-- Iniciando proceso de calculo de sectores, llamado: {0}'.format(content_message))
        await message.channel.send(process_tb_platoon(content_message.split("-")))

client.run(os.getenv('TOKEN'))