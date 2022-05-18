import discord
import os

import src.user_data_caller as udCaller
import variables.variables as config
import utils as utils

client = discord.Client()
players_data = None

###########################################################################


def process_tb_platoon(search_params):

    global players_data
    if (players_data is None):
        print('--- Datos de jugadores inexistente, cargando datos de jugadores')
        players_data = udCaller.retieve_data()

    phase_sectors = config.TERRITORY_BATTLES[search_params[1]][0]
    respuesta = utils.assign_players(phase_sectors, search_params[2], players_data)

    print(respuesta)
    return respuesta


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
        hola = process_tb_platoon(content_message.split("-"))
        for sector in hola:
            hola1 = hola[sector]
            await message.channel.send(sector)
            for platoon in hola1:
                hola2 = hola1[platoon]
                await message.channel.send(platoon)
                for character in hola2:
                    await message.channel.send(character + "  ----  " + hola2[character])
      
client.run(os.getenv('TOKEN'))
