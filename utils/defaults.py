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
        "gold": 10,
        "wood": 0,
        "metal": 0,
        "stone": 0,
        "enemieskilled": 0,
        "selected_enemy": "None",
        "deaths": 0,
        "exp": 0,
        "lootbag": 0,
        "wearing": "None",
        "guild": "None",
        "skills_learned": [],
        "inventory": [],
        "equip": "None",
        "title": "None",
        "location": "Golden Temple",
        "daily_block": 0,
        "vote_block": 0,
        "voted": "False",
        "hp_potions": 0,
        "keys": 0,
        "mine_block": 0,
        "chop_block": 0,
        "background": "https://i.imgur.com/L6JFu3m.jpg",
        "online": 0,
        "blacklisted": "False",
        "Rachikilled": 0,
        "Draugrkilled": 0,
        "Debinkilled": 0,
        "Stalkerkilled": 0,
        "FireGolemkilled": 0,
        "Wyvernkilled": 0,
        "Ooferkilled": 0,
        "Souleaterkilled": 0,
        "Wolfkilled": 0,
        "Goblinkilled": 0,
        "Zombiekilled": 0,
        "Phantasmkilled": 0,
        "TheCorruptedkilled": 0,
        "TheAccursedkilled": 0,
        "ElderDragonkilled": 0,
        "Hadeskilled": 0,
        "EbonyGuardiankilled": 0,
        "Harpykilled": 0,
        "Dormammukilled": 0,
        "Ettinkilled": 0,
        "TheNamelessKingkilled": 0,
        "Largoskilled": 0,
        "Deathclawkilled": 0,
        "Sauriankilled": 0,
        "TheVenomouskilled": 0,
        "Skeletonkilled": 0,
        "Lizardmenkilled": 0,
        "Giantkilled": 0,
        "DeathKnightkilled": 0,
        "IceWolveskilled": 0,
        "FrostOrckilled": 0,
        "FrostGoblinkilled": 0,
        "FrostDragonkilled": 0,
        "exp_potions": 0,
        "questname": "Basic A",
        "questprogress": 0,
        "questscompleted": [],
        "questpart": 0,
        "enemydifficulty": "None",
        "MaxHealth": 100,
        "EnemyStun": 0,
        "SkillCooldown1": 0,
        "SkillCooldown2": 0,
        "Buff1": "None",
        "Buff1Time": 0,
        "cooldown_infraction": 0,
        "monthlyrewards": 0,
        "sawmill": "False",
        "masonry": "False",
        "smeltery": "False",
        "planks": 0,
        "bricks": 0,
        "iron_plates": 0,
        "saw_block": 0,
        "mason_block": 0,
        "smelt_block": 0,
        "camp": "False",
        "trap": 0,
        "trap1": 0,
        "trap2": 0,
        "trap3": 0,
        "trap4": 0,
        "trap5": 0,
        "trap6": 0,
        "trap7": 0,
        "trap8": 0,
        "trap9": 0,
        "trap10": 0,
        "trap11": 0,
        "trap12": 0,
        "trap13": 0,
        "trap_block": 0,
        "axelvl": 0,
        "pickaxelvl": 0,
        "sawlvl": 0,
        "chisellvl": 0,
        "hammerlvl": 0,
        "trader_time": 0,
        "trader_rarity": "False",
        "trader_block": 0,
        "trader_wood": 0,
        "trader_stone": 0,
        "trader_metal": 0,
        "trader_planks": 0,
        "trader_bricks": 0,
        "trader_iron_plates": 0,
        "trader_profit": 0,
        "Stunned": 0,
        "Debuff1": "None",
        "DebuffTime1": 0,
        "pvpcooldown1": 0,
        "pvpcooldown2": 0,
        "TrapKills": 0,
        "friend_list": [],
        "friend_amount": 0,
        "friend_max_amount": 10,
        "party": "None",
        "pet_find": "None",
        "Pet_list": [],
        "equipped_pet": [],
        "pet_stage": "Golden Goose"
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