from time import time

def userdata(user):
    return {
        "_id": user.id,
        "name": user.name,
        "race": "None",
        "class": "None",
        "role": "Player", 
        "health": 100,
        "enemyhp": 50,
        "enemylvl": 0,
        "lvl": 0,
        "gold": 0,
        "wood": 0,
        "metal": 0,
        "stone": 0,
        "enemieskilled": 0,
        "selected_enemy": "None",
        "deaths": 0,
        "exp": 0,
        "lootbag": 0,
        "wearing": "None",
        "defence": 0,
        "guild": "None",
        "skills_learned": [],
        "inventory": [],
        "equip": "None",
        "title": "None",
        "wincry": "None",
        "losecry": "None",
        "location": "Golden Temple",
        "roaming": "False",
        "pet": "None",
        "mana": 100,
        "stamina": 100,
        "craftable": [],
        "daily_block": 0,
        "vote_block": 0,
        "voted": "False",
        "rest_block": 0,
        "fight_block": 0,
        "traveling_block": 0,
        "hp_potions": 0,
        "keys": 2,
        "crates": 0,
        "mine_block": 0,
        "chop_block": 0,
        "in_dungeon": "False",
        "dungeon_enemy": "None",
        "duneon_enemy_hp": 0,
        "in_party": [],
        "background": "https://i.imgur.com/L6JFu3m.jpg",
        "online": 0,
        "blacklisted": "False",
        "cooldown_infraction": []
        }

def raiddata(guild, boss):
    return {
        "_id": guild.id,
        "raidserver": guild.id,
        "raidbosshealth": 100,
        "raidlvl": 0,
        "raidexp": 0,
        "raidgold": 0,
        "raidwood": 0,
        "raidstone": 0,
        "raidmetal": 0,
        "raidboss": boss,
        "raidbonus": 0,
        "raidmembers": 0,
        "raidmemberlist": {
            "member0": "None",
            "member1": "None",
            "member2": "None",
            "member3": "None",
            "member4": "None",
            "member5": "None",
            "member6": "None",
            "member7": "None",
            "member8": "None",
            "member9": "None"
        }
    }

def battledata(user):
    return {
        "_id": user.id,
        "battle_user": user.id,
        "battle_enemy": "None",
        "battle_streak": 0,
        "battle_losses": 0,
        "battle_wins": 0,
        "battle_rank": "Beginner",
        "battle_active": "False",
        "battle_turn": "x",
        "lastmove": 0
    }

def titledata(user):
    return {
        "_id": user.id,
        "titles_user": user.id,
        "titles_list": [],
        "titles_amount": 0
    }

def locationdata(data):
    return {
        "name": data["name"] or "Unknown Location",
        "monsters": data["monsters"] or [],
        "descrip": data["descrip"] or "A mysterious, unexplored region...",
        "minlvl": data["lvl"] or 0
    }

def monsterdata(data):
    return {
        "name": data["name"] or "Unknown Monster",
        "descrip": data["descrip"] or "A mysterious, hostile creature...",
        "moves": data["moves"] or ["Slash"],
        "maxdmg": data["max_dmg"] or 20,
        "mindmg": data["min_dmg"] or 10,
        "rarity": data["rarity"] or 75,
        "minhp": data["minhp"] or 50,
        "maxhp": data["maxhp"] or 75
    }

def itemdata(data):
    return {
        "name": data["name"] or "Unknown item",
        "type": data["type"] or "Unknown type",
        "descrip": data["descrip"] or "A mysterious item forged from ancient magic.",
        "class": data["class"] or "all",
        "rarity": data["rarity"] or "Unknown rarity",
        "image": data["image"] or "None",
        "race": data["race"] or "all",
        "stats_min": data["stats_min"] or 5,
        "stats_max": data["stats_max"] or 1,
        "refinement": data["refinement"] or "Unknown refinement"
    }

def skilldata(data):
    return {
        "name": data["name"] or "???",
        "descrip": data["descrip"] or "???",
        "class": data["class"] or "all",
        "race": data["race"] or "all",
        "dmg": data["dmg"] or 5,
        "minlvl": data["minlvl"] or 0
    }

def guilddata(guild):
    return {
        "_id": guild.id,
        "language": "EN",
        "prefixes": [],
        "joinreward": "False",
        "ignore": [],
        "eventchannel": "None",
        "name": guild.name,
        "health": 100,
        "lvl": 0,
        "exp": 0,
        "gold": 0,
        "wood": 0,
        "stone": 0,
        "metal": 0,
        "enemieskilled": 0,
        "enemy": "None",
        "bonus": 0,
        "inventory": [],
        "officers": [],
        "title": "None",
        "members": 0,
        "mission": "None",
        "missionscompleted": 0,
        "missionprogress": 0,
        "tag": "None",
        "joined": [],
        "raiders": [],
        "raidhp": 0,
        "raidstart": "None",
        "welcome_image": "None",
        "welcome_message": ":wave: **Welcome to {1}, {0}!**",
        "welcome_enabled": "False",
        "welcome_channel": "None"
        }