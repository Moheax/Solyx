import discord
import platform, asyncio, string, operator, textwrap
import os, re, aiohttp
import time
import json
import random
import math
import logging
from discord.ext import commands
from discord.utils import find
from __main__ import send_cmd_help
from cogs.utils.dataIO import fileIO
from cogs.utils import checks
from cogs.utils.chat_formatting import pagify
from random import choice as randchoice
from cogs.rpgutils.db import db
from cogs.rpgutils.defaults import userdata, titledata
try:
    import scipy
    import scipy.misc
    import scipy.cluster
except:
    pass
#         weapons_list = ["hp","Hp", "Calcite Staff", "Glyphic Bow", "Abaddon Dagger", "Sclerite Sword", "Iron Greatsword", "Rusted Short Sword", "Staff of Milos", "Obsidian Longbow", "Verdant Bow", "Oblivion", "Reinforced Crossbow", "Etched Long Bow", "Mithril Sword", "Spiked Mace", "Curved Dagger", "Tomb of Water", "Rusted Crossbow", "Makeshift Short Bow", "Iron Mace", "Iron Claws", "Concealed Blade", "Tomb of Fire", "Scroll of Blizzards"]

class shop:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def shop(self, ctx, *, item):
        user = ctx.message.author
        userinfo = db.users.find_one({ "_id": user.id })
        bow = ["Archer", "Ranger", "Assassin"]
        sword = ["Paladin", "Gladiator", "Knight"]
        dagger = ["Thief", "Mesmer", "Rogue"]
        staff = ["Mage", "Elementalist", "Necromancer"]
        light = ["Mesmer", "Assassin", "Thief", "Archer"]
        medium = ["Gladiator", "Mage", "Necromancer", "Rogue"]
        heavy = ["Paladin", "Knight", "Elementalist", "Ranger"]

        if item == "Sclerite Sword":
            itemobj = {"name": "Sclerite Sword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Evoke3O.png"}
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)
            else:
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append(itemobj)
                db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
                em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)

        elif item == "Iron Greatsword":
            itemobj = {"name": "Iron Greatsword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/TlKPvfz.png"}
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)
            else:
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append(itemobj)
                db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
                em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)

        elif item == "Abaddon Dagger":
            itemobj = {"name": "Abaddon Dagger", "type": "dagger", "rarity": "Common", "stats_min": 3, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/yNkqfOo.png"}
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)
            else:
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append(itemobj)
                db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
                em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)

        elif item == "Rusted Short Sword":
            itemobj = {"name": "Rusted Short Sword", "type": "dagger", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Ox1CXhJ.png"}
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)
            else:
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append(itemobj)
                db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
                em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)

        elif item == "Verdant Bow":
            itemobj = {"name": "Verdant Bow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3EyPeH2.png"}
            cost = 2300
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)
            else:
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append(itemobj)
                db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
                em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)

        elif item == "Obsidian Longbow":
            itemobj = {"name": "Obsidian Longbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/0LEmcAH.png"}
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)
            else:
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append(itemobj)
                db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
                em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)

        elif item == "Etched Longbow":
            itemobj = {"name": "Etched Longbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/VvYc9zY.png"}
            cost = 2300
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)
            else:
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append(itemobj)
                db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
                em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)

        elif item == "Mithril Sword":
            itemobj = {"name": "Mithril Sword", "type": "sword", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/UNc4JeO.png"}
            cost = 2300
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)
            else:
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append(itemobj)
                db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
                em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)

        elif item == "Spiked Mace":
            itemobj = {"name": "Spiked Mace", "type": "mace", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3PZfnkC.png"}
            cost = 2300
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)
            else:
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append(itemobj)
                db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
                em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)

        elif item == "Curved Dagger":
            itemobj = {"name": "Curved Dagger", "type": "dagger", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/31mYMgk.png"}
            cost = 2300
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)
            else:
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append(itemobj)
                db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
                em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)

        elif item == "Tomb of Water":
            itemobj = {"name": "Tomb of Water", "type": "staff", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/H7Umwgs.png"}
            cost = 2300
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)
            else:
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append(itemobj)
                db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
                em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)

        elif item == "Makeshift Shortbow":
            itemobj = {"name": "Makeshift Shortbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/IDwPClu.png"}
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)
            else:
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append(itemobj)
                db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
                em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)

        elif item == "Iron Mace":
            itemobj = {"name": "Iron Mace", "type": "mace", "rarity": "Rare", "stats_min": 20, "stats_max": 30, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/eMGSaS5.png"}
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)
            else:
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append(itemobj)
                db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
                em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)

        elif item == "Iron Claws":
            itemobj = {"name": "Iron Claws", "type": "dagger", "rarity": "Rare", "stats_min": 24, "stats_max": 28, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/lrk0y5p.png"}
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)
            else:
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append(itemobj)
                db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
                em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)

        elif item == "Concealed Blade":
            itemobj = {"name": "Concealed Blade", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/dQ6Qt1J.png"}
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)
            else:
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append(itemobj)
                db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
                em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)

        elif item == "Tomb of Fire":
            itemobj = {"name": "Tomb of Fire", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/xOtnEZO.png"}
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)
            else:
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append(itemobj)
                db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
                em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)

        elif item == "Scroll of Blizzards":
            itemobj = {"name": "Scroll of Blizzards", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/5dbmIRN.png"}
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)
            else:
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append(itemobj)
                db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
                em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)

        elif item == "Glyphic Bow":
            itemobj = {"name": "Glyphic Bow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/DzHgPl4.png"}
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)
            else:
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append(itemobj)
                db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
                em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)

        elif item == "Oblivion":
            itemobj = {"name": "Oblivion", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/jVIN9in.png"}
            cost = 2300
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)
            else:
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append(itemobj)
                db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
                em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)

        elif item == "Staff of Milos":
            itemobj = {"name": "Staff of Milos", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/9Lakl7u.png"}
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)
            else:
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append(itemobj)
                db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
                em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)

        elif item == "Calcite Staff":
            itemobj = {"name": "Calcite Staff", "type": "staff", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/ZRV97xu.png"}
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)
            else:
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append(itemobj)
                db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
                em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
                await self.bot.say(embed=em)

# - - - - - Armor - - - - -

        """elif item == "Leather Armor":
            itemobj = {"name": "Leather Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "price": 1000, "description": "?!", "image": "None"}
            cost = 1000

        elif item == "Banded Armor":
            itemobj = {"name": "Banded Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "price": 1000, "description": "?!", "image": "None"}
            cost = 1000

        elif item == "Wolf Fur":
            itemobj = {"name": "Wolf Fur", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "price": 2300, "description": "?!", "image": "None"}
            cost = 2300

        elif item == "Pit Fighter Armor":
            itemobj = {"name": "Pit Fighter Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "price": 1000, "description": "?!", "image": "None"}
            cost = 1000

        elif item == "Chainmail Armor":
            itemobj = {"name": "Chainmail Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "price": 1000, "description": "?!", "image": "None"}
            cost = 1000

        elif item == "Steel Armor":
            itemobj = {"name": "Steel Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "price": 2300, "description": "?!", "image": "None"}
            cost = 2300

        elif item == "Barbaric Armor":
            itemobj = {"name": "Barbaric Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "price": 1000, "description": "?!", "image": "None"}
            cost = 1000

        elif item == "Metal Armor":
            itemobj = {"name": "Metal Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "price": 2300, "description": "?!", "image": "None"}
            cost = 2300

        elif item == "Iron Armor":
            itemobj = {"name": "Iron Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "price": 2300, "description": "?!", "image": "None"}
            cost = 2300"""

    @commands.group(name="items", pass_context=True, no_pm=True)
    @checks.is_owner()
    async def _items(self, ctx):
        if ctx.invoked_subcommand:
            return
        else:
            await self.bot.send_cmd_help(ctx)

    @_items.command(name="weapons", pass_context=True)
    @checks.is_owner()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _items_weapons(self, ctx):
        user = ctx.message.author
        userinfo = db.users.find_one({ "_id": user.id })
        Class = userinfo["class"]
        if Class == "Mage" or Class == "Elementalist" or Class == "Necromancer":
            em = discord.Embed(title="Weapon list for the {} class".format(Class), description="Common:<:Common:573784881012932618> Rare:<:Rare:573784880815538186> Legendary:<:Legendary:639425368167809065> Mythical:<:Mythical:573784881386225694>", color=discord.Colour(0xffffff))
            em.add_field(name="Calcite Staff <:Common:573784881012932618>", value="1,000 gold")
            em.add_field(name="Staff of Milos <:Common:573784881012932618>", value="1,000 gold")
            em.add_field(name="Tomb of Fire <:Common:573784881012932618>", value="1,000 gold")
            em.add_field(name="Scroll of Blizzards <:Common:573784881012932618>", value="1,000 gold")
            em.add_field(name="Oblivion <:Rare:573784880815538186>", value="2,300 gold")
            em.add_field(name="Tomb of Water <:Rare:573784880815538186>", value="2,300 gold")
            em.add_field(name="Thunderguard <:Legendary:639425368167809065>", value="Not buyable")
            em.add_field(name="Solarflare <:Legendary:639425368167809065>", value="Not buyable")
            await self.bot.say(embed=em)
        elif Class == "Paladin" or Class == "Gladiator" or Class == "Knight":
            em = discord.Embed(title="Weapon list for the {} class".format(Class), description="Common:<:Common:573784881012932618> Rare:<:Rare:573784880815538186> Legendary:<:Legendary:639425368167809065> Mythical:<:Mythical:573784881386225694>", color=discord.Colour(0xffffff))
            em.add_field(name="Sclerite Sword <:Common:573784881012932618>", value="1,000 gold")
            em.add_field(name="Iron Greatsword <:Common:573784881012932618>", value="1,000 gold")
            em.add_field(name="Iron Mace <:Common:573784881012932618>", value="1,000 gold")
            em.add_field(name="Mithril Sword <:Rare:573784880815538186>", value="2,300 gold")
            em.add_field(name="Spiked Mace <:Rare:573784880815538186>", value="2,300 gold")
            em.add_field(name="Excalibur <:Legendary:639425368167809065>", value="Not buyable")
            em.add_field(name="Twilight <:Legendary:639425368167809065>", value="Not buyable")
            await self.bot.say(embed=em)
        elif Class == "Thief" or Class == "Mesmer" or Class == "Rogue":
            em = discord.Embed(title="Weapon list for the {} class".format(Class), description="Common:<:Common:573784881012932618> Rare:<:Rare:573784880815538186> Legendary:<:Legendary:639425368167809065> Mythical:<:Mythical:573784881386225694>", color=discord.Colour(0xffffff))
            em.add_field(name="Abaddon Dagger <:Common:573784881012932618>", value="1,000 gold")
            em.add_field(name="Rusted Short Sword <:Common:573784881012932618>", value="1,000 gold")
            em.add_field(name="Iron Claws <:Common:573784881012932618>", value="1,000 gold")
            em.add_field(name="Concealed Blade <:Common:573784881012932618>", value="1,000 gold")
            em.add_field(name="Curved Dagger <:Rare:573784880815538186>", value="2,300 gold")
            em.add_field(name="Deathraze <:Legendary:639425368167809065>", value="Not buyable")
            em.add_field(name="Doomblade <:Legendary:639425368167809065>", value="Not buyable")
            em.add_field(name="Soulreaper <:Legendary:639425368167809065>", value="Not buyable")
            await self.bot.say(embed=em)
        elif Class == "Archer" or Class == "Ranger" or Class == "Assassin":
            em = discord.Embed(title="Weapon list for the {} class".format(Class), description="Common:<:Common:573784881012932618> Rare:<:Rare:573784880815538186> Legendary:<:Legendary:639425368167809065> Mythical:<:Mythical:573784881386225694>", color=discord.Colour(0xffffff))
            em.add_field(name="Glyphic Bow <:Common:573784881012932618>", value="1,000 gold")
            em.add_field(name="Obsidian Longbow <:Common:573784881012932618>", value="1,000 gold")
            em.add_field(name="Rusted Crossbow <:Common:573784881012932618>", value="1,000 gold")
            em.add_field(name="Makeshift Short Bow <:Common:573784881012932618>", value="1,000 gold")
            em.add_field(name="Verdant Bow <:Rare:573784880815538186>", value="2,300 gold")
            em.add_field(name="Reinforced Crossbow <:Rare:573784880815538186>", value="2,300 gold")
            em.add_field(name="Etched Long Bow <:Rare:573784880815538186>", value="2,300 gold")
            em.add_field(name="Hawkeye <:Legendary:639425368167809065>", value="Not buyable")
            em.add_field(name="Devil's Kiss <:Legendary:639425368167809065>", value="Not buyable")
            await self.bot.say(embed=em)
        else:
            em = discord.Embed(description="Sorry, your class is not supported!", color=discord.Colour(0xffffff))
            await self.bot.say(embed=em)

    @_items.command(name="armor", pass_context=True)
    @checks.is_owner()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _items_armor(self, ctx):
        user = ctx.message.author
        userinfo = db.users.find_one({ "_id": user.id })
        Class = userinfo["class"]

        if Class == "Mesmer" or Class == "Assassin" or Class == "Thief" or Class == "Archer":
            em = discord.Embed(title="Armor list for the {} class (Light)".format(Class), description="Common:<:Common:573784881012932618> Rare:<:Rare:573784880815538186> Legendary:<:Legendary:639425368167809065> Mythical:<:Mythical:573784881386225694>", color=discord.Colour(0xffffff))
            em.add_field(name="Leather Armor <:Common:573784881012932618>", value="1,000 gold")
            em.add_field(name="Banded Armor <:Common:573784881012932618>", value="1,000 gold")
            em.add_field(name="Wolf Fur <:Rare:573784880815538186>", value="2,300 gold")
            em.add_field(name="Nightstalker Mantle <:Legendary:639425368167809065>", value="Not buyable")
            await self.bot.say(embed=em)
        elif Class == "Gladiator" or Class == "Mage" or Class == "Necromancer" or Class == "Rogue":
            em = discord.Embed(title="Armor list for the {} class (Medium)".format(Class), description="Common:<:Common:573784881012932618> Rare:<:Rare:573784880815538186> Legendary:<:Legendary:639425368167809065> Mythical:<:Mythical:573784881386225694>", color=discord.Colour(0xffffff))
            em.add_field(name="Chainmail Armor <:Common:573784881012932618>", value="1,000 gold")
            em.add_field(name="Pit Fighter Armor <:Common:573784881012932618>", value="1,000 gold")
            em.add_field(name="Enchanted Steel Armor <:Rare:573784880815538186>", value="2,300 gold")
            em.add_field(name="Bane Of The Goblin Lord <:Legendary:639425368167809065>", value="Not buyable")
            await self.bot.say(embed=em)
        elif Class == "Paladin" or Class == "Knight" or Class == "Elementalist" or Class == "Ranger":
            em = discord.Embed(title="Armor list for the {} class (Heavy)".format(Class), description="Common:<:Common:573784881012932618> Rare:<:Rare:573784880815538186> Legendary:<:Legendary:639425368167809065> Mythical:<:Mythical:573784881386225694>", color=discord.Colour(0xffffff))
            em.add_field(name="Barbaric Armor <:Common:573784881012932618>", value="1,000 gold")
            em.add_field(name="Branded Metal Armor <:Rare:573784880815538186>", value="2,300 gold")
            em.add_field(name="Iron Armor <:Rare:573784880815538186>", value="2,300 gold")
            em.add_field(name="Hephaestus Armor <:Legendary:639425368167809065>", value="Not buyable")
            await self.bot.say(embed=em)
        else:
            em = discord.Embed(description="Sorry, your class is not supported!", color=discord.Colour(0xffffff))
            await self.bot.say(embed=em)

def setup(bot):
    n = shop(bot)
    bot.add_cog(n)