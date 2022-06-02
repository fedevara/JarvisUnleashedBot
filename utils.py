import variables.variables as config


def assign_players(generalPlatoon, fase, players_data):
    charactersUsedByMembers = {}
    for sector in generalPlatoon:
        print('--- SECTOR: {0}'.format(sector))
        for platoon in generalPlatoon[sector]:
            print('--- PLATOON: {0}'.format(platoon))
            for character in generalPlatoon[sector][platoon]:
                character_by_member = search_character_by_member(character, fase, players_data, charactersUsedByMembers)
                generalPlatoon[sector][platoon][character] = character_by_member[0]
                charactersUsedByMembers = character_by_member[1]
    return generalPlatoon


def search_character_by_member(character, config_given, players_data, charactersUsedByMembers):
    player_selected = None
    min_power = config.CONFIG_TB["min_power"]
    for member in players_data:

        if (checkMemberAvailability(charactersUsedByMembers, character, member["data"]["name"])):
      
            is_selectable_character = False
            minPowerSelected = config.CONFIG_TB[config_given]
    
            for characters in member["units"]:
                iterate_character = characters["data"]
                if (check_character_selectable(iterate_character, character, minPowerSelected, min_power)):
                    min_power = iterate_character["power"]
                    is_selectable_character = True
    
            if (player_selected is None or is_selectable_character):
                player_selected = member["data"]["name"]

    if (min_power == config.CONFIG_TB["min_power"]):
        print("---- {0} no asignado, no hay integrantes del gremio que cumplan las condiciones".format(character))
        return [None, charactersUsedByMembers]

    print("---- Asignado: {0} - {1} - Poder {2}".format(character, player_selected, str(min_power)))

    charactersUsedByMembers = addMember(charactersUsedByMembers, character, player_selected)
    return [player_selected, charactersUsedByMembers]


def addMember(charactersUsedByMembers, character, player_selected):

    if (charactersUsedByMembers.get(player_selected) == None):
        charactersUsedByMembers[player_selected] = [character]
    else:
        characterList = charactersUsedByMembers[player_selected]
        characterList.append(character)
        charactersUsedByMembers[player_selected] = characterList
    
    return charactersUsedByMembers


def check_character_selectable(iCharacter, character, minPowerSelected, minPower):
    return iCharacter["base_id"] == character and iCharacter["rarity"] >= minPowerSelected and iCharacter["power"] <= minPower


def checkMemberAvailability(charactersUsedByMembers, character, member):
  
    if (charactersUsedByMembers.get(member) == None):
        return True

    if (character not in charactersUsedByMembers[member]):
        return True
      
    if (len(charactersUsedByMembers[member]) < 10):
        return True
      
    return False