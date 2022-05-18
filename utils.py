import variables.variables as config


def assign_players(generalPlatoon, fase, players_data):
    for sector in generalPlatoon:
        print('--- SECTOR: {0}'.format(sector))
        for platoon in generalPlatoon[sector]:
            print('--- PLATOON: {0}'.format(platoon))
            for character in generalPlatoon[sector][platoon]:
                generalPlatoon[sector][platoon][character] = search_character_by_member(character, fase, players_data)
    return generalPlatoon


def search_character_by_member(character, config_given, players_data):
    player_selected = None
    min_power = config.CONFIG_TB["min_power"]
    for member in players_data:
        is_selectable_character = False
        minPowerSelected = config.CONFIG_TB[config_given]

        for characters in member["units"]:
            iterate_character = characters["data"]
            if (iterate_character["base_id"] == character):
                if (iterate_character["rarity"] >= minPowerSelected and iterate_character["power"] <= min_power):
                    min_power = iterate_character["power"]
                    is_selectable_character = True
                break

        if (player_selected is None or is_selectable_character):
            player_selected = member["data"]["name"]

    if (min_power == config.CONFIG_TB["min_power"]):
        print("---- {0} no asignado, no hay integrantes del gremio que cumplan las condiciones".format(character))
        return None

    print("---- Asignado: {0} - {1} - Poder {2}".format(character, player_selected, str(min_power)))

    return (player_selected)