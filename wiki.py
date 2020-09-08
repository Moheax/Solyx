import discord
import platform, asyncio, string, operator, textwrap
import random
import os, re, aiohttp
from random import choice as randchoice
from discord.ext import commands
from utils.db import db
from utils.defaults import guilddata, userdata
from utils import checks
from utils.chat_formatting import pagify
from utils.dataIO import fileIO
import math
try:
    from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageOps, ImageFilter
except:
    raise RuntimeError("Can't load pillow. Do 'pip3 install pillow'.")
try:
    import scipy
    import scipy.misc
    import scipy.cluster
except:
    pass


class wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True, aliases=["wikipedia"], no_pm=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def wiki(self, ctx, *, topic=None):
        guild = ctx.guild
       

		if topic == None:
			embed=discord.Embed(color=discord.Colour(0xffffff))
			embed.add_field(name="<:ShieldCheck:560804135545602078>**Wiki Mainpage**", value="\n\nPage 1/3\n\nWiki usage: {}wiki [page].\n Or\nWiki usage: {}wiki [subject].\n\nShield Meanings\n <:ShieldCheck:560804135545602078> = Works Completely! \n <:ShieldBug:649157223905492992> = Working on it!\n <:ShieldBroken:649157253701566474> = Is made but broken...\n <:ShieldCross:560804112548233217> = Hasnt been made yet.\n\n If items dont have the <:ShieldCheck:560804135545602078> Emote you can help and submit a backstory if you want!\n\nCurrent pages 1, 2,3\n\n".format(ctx.prefix, ctx.prefix), inline=False)

			embed.set_footer(text="submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")

			await ctx.send(embed=embed)

#            title="Wiki topics"
#            description="`elf`, `orc`, `phantasm`, `corrupted`, `fire golem`, `test`, `Guild Bonus`"
#            footer="Command usage: {}wiki [subject].".format(ctx.prefix)

#            embed=discord.Embed(color=discord.Colour(0xffffff))
#			 <:ShieldCheck:560804135545602078>
#			 <:ShieldCross:560804112548233217>
#            embed.add_field(name="**Wiki Topics**", value="", inline=False)
#            embed.add_field(name="Armor", value="Chainmail, Barbaric, Pit Fighter, Banded, Leather, Iron, Branded Metal,        Wolf Fur, Enchanted Steel, Bane Of The Goblin Lord, Nighstalker Mantle, Hephaestus Armor, ", inline=False)
#            embed.add_field(name="Bosses", value="Phantasm, Fire Golem, The Corrupted, The Accursed, The Nameless King,    The Venomous", inline=False)
#            embed.add_field(name="Classes", value="Archer, Knight, Mage, Thief, Assassin, Ranger, Samurai, Paladin, Necromancer, Elementalist, Rogue, Mesmer", inline=False)
#            embed.add_field(name="Fighting", value="PVE, PVP", inline=False)
#            embed.add_field(name="Gathering", value="Wood, Stone, Metal, Fish", inline=False)
#            embed.add_field(name="Guild", value="Info, Represent, Mission, Donate, Promote, Demote, Tag", inline=False)
#            embed.add_field(name="Items", value="Health Potions, Keys, Crates, Gold", inline=False)
#            embed.add_field(name="Monsters", value="Rachi, Debin, Oofer, Wyvern, Wolf, Goblin, Zombie, Draugr, Stalker, Souleater, Elder Dragon, Hades, Ebony Guardian, Harpy, Dormammu, Ettin, Largos, Deathclaw, Saurian", inline=False)
#            embed.add_field(name="Races", value="Orc, Human, Elf, Demon", inline=False)
#            embed.add_field(name="Ranking", value="Users, Guilds", inline=False)
#            embed.add_field(name="Weapons", value="Starter Bow, Starter Sword, Starter Staff, Starter Dagger,Iron Claws, Iron Mace, Curved Dagger, Tomb of Water, Spiked Mace, Mithril Sword, Etched Longbow, Verdant Bow, Excalibur, Twilight, Devil's Kiss, Hawkeye, Solarflare, Thunderguard, Doomblade, Deathraze, Soulreaper", inline=True)
#            embed.add_field(name="Daily", value="Checkin, Vote", inline=False)
#            embed.add_field(name="Equip", value="Weapons, armor", inline=False)
#            embed.add_field(name="Market", value="Sell, Buy,", inline=False)
#            embed.set_footer(text="submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
#            await ctx.send(embed=embed)

#			title="Fire Golem"
#			description="**\u27a4 Health** - 30 to 50 \n**\u27a4 Damage** - 10 to 20 \n**\u27a4 Gold** - 18 to 21   \n**\u27a4 Exp** - 10 to 30 \n \nThe fire golem's name speaks for itself. The golems arose from the depths of a volcano, summoned by an ancient group of druids to protect the Golden Temple. The golem's bodies are made from magnetized lava rock. built to withstand high pressure and has strong resistance against piercing attacks. Long have the golems been asleep. But the increase of wandering adventurers have woken them once more. The golems have no feelings and only one objective in mind. To kill tresspassers."
#			footer="Submitted by AceTheBear223#4562\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.".format(ctx.prefix)
#			icon = ('https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/intermediary/f/c7f23f41-5bd8-4b82-a00c-d61b0cfb0160/d9p8w3t-e2e0278a-7b05-4d6b-9a69-c50f3f005126.png/v1/fill/w_700,h_331,q_70,strp/fire_golem_by_sourshade_d9p8w3t-350t.jpg')

#           <:ShieldCheck:560804135545602078> = Works Completely!
#           <:ShieldBug:649157223905492992> = Working on it!
#           <:ShieldBroken:649157253701566474> = Is made but broken...
#           <:ShieldCross:560804112548233217> = Hasnt been made yet.


		elif topic == "2" or topic =="page 2":
			embed=discord.Embed(color=discord.Colour(0xffffff))
			embed.add_field(name="**Wiki topics**", value="Page 2/3".format(ctx.prefix, ctx.prefix), inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>Armor", value="Chainmail, Barbaric, Pit Fighter, Banded, Leather, Iron, Branded Metal,        Wolf Fur, Enchanted Steel, Bane Of The Goblin Lord, Nighstalker Mantle, Hephaestus Armor, ", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>Bosses", value="Phantasm, Fire Golem, The Corrupted, The Accursed, The Nameless King,    The Venomous", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>Classes", value="Archer, Knight, Mage, Thief, Assassin, Ranger, Samurai, Paladin, Necromancer, Elementalist, Rogue, Mesmer", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>Fighting", value="PVE, PVP", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>Gathering", value="Wood, Stone, Metal, Fish", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>Guild", value="Info, Represent, Mission, Donate, Promote, Demote, Tag", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>Items", value="Health Potions, Keys, Crates, Gold", inline=False)
			embed.set_footer(text="submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Chainmail" or topic == "chainmail":
			embed=discord.Embed(title="**Chainmail Armor**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Common", inline=False)
			embed.add_field(name="**Defense**", value="2 - 12", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Barbaric" or topic == "barbaric":
			embed=discord.Embed(title="**Barbaric Armor**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Common", inline=False)
			embed.add_field(name="**Defense**", value="5 - 7", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Pit fighter" or topic == "pit fighter":
			embed=discord.Embed(title="**Pit fighter**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Common", inline=False)
			embed.add_field(name="**Defense**", value="4 - 9", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Banded" or topic == "banded":
			embed=discord.Embed(title="**Banded Armor**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Common", inline=False)
			embed.add_field(name="**Defense**", value="1 - 10", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Leather" or topic == "leather":
			embed=discord.Embed(title="**Leather Armor**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Common", inline=False)
			embed.add_field(name="**Defense**", value="3 - 8", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Iron" or topic == "iron":
			embed=discord.Embed(title="**Iron Armor**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Rare", inline=False)
			embed.add_field(name="**Defense**", value="14 - 16", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Branded Metal" or topic == "branded metal":
			embed=discord.Embed(title="**Branded Metal Armor**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Rare", inline=False)
			embed.add_field(name="**Defense**", value="13 - 17", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Wolf Fur" or topic == "wolf fur":
			embed=discord.Embed(title="**Wolf Fur**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Rare", inline=False)
			embed.add_field(name="**Defense**", value="1 - 24", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Enchanted Steel" or topic == "enchanted steel":
			embed=discord.Embed(title="**Enchanted Steel Armor**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Rare", inline=False)
			embed.add_field(name="**Defense**", value="12 - 17", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Bane Of The Goblin Lord" or topic == "bane of the goblin lord":
			embed=discord.Embed(title="**Bane Of The Goblin Lord**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Legendary", inline=False)
			embed.add_field(name="**Defense**", value="20 - 25", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Nightstalker Mantle" or topic == "nightstalker mantle":
			embed=discord.Embed(title="**Nightstalker Mantle**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Legendary", inline=False)
			embed.add_field(name="**Defense**", value="15 - 28", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Hephaestus Armor" or topic == "hephaestus armor":
			embed=discord.Embed(title="**Hephaestus Armor**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Legendary", inline=False)
			embed.add_field(name="**Defense**", value="16 - 27", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Phantasm" or topic == "phantasm":
			embed=discord.Embed(title="**Phantasm**", description="**<:ShieldCheck:560804135545602078>Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="https://i.imgur.com/BbBmEOF.jpg")
			embed.add_field(name="**Health**", value="60Hp - 80Hp", inline=False)
			embed.add_field(name="**Damage**", value="10Dmg - 15Dmg", inline=False)
			embed.add_field(name="**Gold**", value="16G  - 21G", inline=False)
			embed.add_field(name="**Experience**", value="10Exp - 30Exp", inline=False)
			embed.add_field(name="Back Story", value="The Phantasm has long protected The Forest. The Monks prayed and offered sacrifices to keep it satisfied. The Phantasm resides near hidden lakes throughout the forest, as the water is it's life source. As the praying monks became extinct it no longer has any peace. Whenever the Phantasm feels threatened it gathers dark clouds and density into an eerie storm. It uses it's long slithering body to smother its threats. And guides the lightning of the storm onto it's foes.", inline=False)
			embed.set_footer(text="Submitted by AceTheBear223#4562\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Fire Golem" or topic == "fire golem":
			embed=discord.Embed(title="**Fire Golem**", description="**<:ShieldCheck:560804135545602078>Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/intermediary/f/c7f23f41-5bd8-4b82-a00c-d61b0cfb0160/d9p8w3t-e2e0278a-7b05-4d6b-9a69-c50f3f005126.png/v1/fill/w_700,h_331,q_70,strp/fire_golem_by_sourshade_d9p8w3t-350t.jpg")
			embed.add_field(name="**Health**", value="30Hp - 50Hp", inline=False)
			embed.add_field(name="**Damage**", value="10Dmg - 20Dmg", inline=False)
			embed.add_field(name="**Gold**", value="18G  - 21G", inline=False)
			embed.add_field(name="**Experience**", value="10Exp - 30Exp", inline=False)
			embed.add_field(name="Back Story", value="The fire golem's name speaks for itself. The golems arose from the depths of a volcano, summoned by an ancient group of druids to protect the Golden Temple. The golem's bodies are made from magnetized lava rock. built to withstand high pressure and has strong resistance against piercing attacks. Long have the golems been asleep. But the increase of wandering adventurers have woken them once more. The golems have no feelings and only one objective in mind. To kill tresspassers.", inline=False)
			embed.set_footer(text="Submitted by AceTheBear223#4562\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "corrupted" or topic == "the corrupted" or topic == "The Corrupted" or topic == "Corrupted":
			embed=discord.Embed(title="**The Corrupted**", description="**<:ShieldCheck:560804135545602078>Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="https://i.imgur.com/oTi3K3q.jpg")
			embed.add_field(name="**Health**", value="70Hp - 90Hp", inline=False)
			embed.add_field(name="**Damage**", value="15 - 30Dmg", inline=False)
			embed.add_field(name="**Gold**", value="22G  - 25G", inline=False)
			embed.add_field(name="**Experience**", value="10Exp - 35Exp", inline=False)
			embed.add_field(name="Back Story", value="The Corrupted originally came from a relatively peaceful race of dragons. Their emerald green scales became a very wanted loot amongst adventurers. The adventurers betrayed the race it's trust and slaughtered almost all of the dragons. The survivors went into a frenzy. No longer able to tell any difference between living beings. The Corrupted kill blindly. Their snake like fangs have teared trough many houses and castles alike. Their horns grow as they kill, and their roaring can be heard from afar. Now they roam the ruins of Saker Keep.", inline=False)
			embed.set_footer(text="Submitted by AceTheBear223#4562\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "The Accursed" or topic == "Accursed" or topic == "the accursed" or topic == "accursed":
			embed=discord.Embed(title="**The Accursed**", description="**<:ShieldBug:649157223905492992>Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Health**", value="70Hp - 90Hp", inline=False)
			embed.add_field(name="**Damage**", value="20Dmg - 40Dmg", inline=False)
			embed.add_field(name="**Gold**", value="26G  - 29G", inline=False)
			embed.add_field(name="**Experience**", value="15Exp - 35Exp", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "The Nameless King" or topic == "the nameless king" or topic == "Nameless King" or topic == "nameless king":
			embed=discord.Embed(title="**The Nameless King**", description="**<:ShieldBug:649157223905492992>Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Health**", value="100Hp - 120Hp", inline=False)
			embed.add_field(name="**Damage**", value="25Dmg - 40Dmg", inline=False)
			embed.add_field(name="**Gold**", value="28G  - 31G", inline=False)
			embed.add_field(name="**Experience**", value="20Exp - 40Exp", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "The Venomous" or topic == "the venomous" or topic == "Venomous" or topic == "venomous":
			embed=discord.Embed(title="**The Venomous**", description="**<:ShieldBug:649157223905492992>Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Health**", value="110Hp - 130Hp", inline=False)
			embed.add_field(name="**Damage**", value="25Dmg - 50Dmg", inline=False)
			embed.add_field(name="**Gold**", value="30G - 33G", inline=False)
			embed.add_field(name="**Experience**", value="20Exp - 45Exp", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Archer" or topic == "archer" :
			embed=discord.Embed(title="**Archer**", description="**<:ShieldBug:649157223905492992>Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/639473419703812122.png?")
			embed.add_field(name="**Description**", value="Precise and long ranged damage, chance on critical strike", inline=False)
			embed.add_field(name="**Skills**", value="Shoot", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Special**", value="20% Change to deal 120% dmg", inline=False)
			embed.add_field(name="**Specialization**", value="Assassin or Ranger", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Knight" or topic == "knight" :
			embed=discord.Embed(title="**Knight**", description="**<:ShieldBug:649157223905492992>Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/639473415492861972.png?v=1")
			embed.add_field(name="**Description**", value="Tanky class with close combat damage reduction", inline=False)
			embed.add_field(name="**Skills**", value="Swing", inline=False)
			embed.add_field(name="**Special**", value="8 -15 Damage Reduction", inline=False)
			embed.add_field(name="**Specialization**", value="Paladin or Samurai", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Mage" or topic == "mage" :
			embed=discord.Embed(title="**Mage**", description="**<:ShieldBug:649157223905492992>Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/639473422040301574.png?v=1")
			embed.add_field(name="**Description**", value="Long ranged average damage class with epic items", inline=False)
			embed.add_field(name="**Skills**", value="Cast", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Special**", value="AOE Damage (Area of Effect)", inline=False)
			embed.add_field(name="**Specialization**", value="Necromancer or Elementalist", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Thief" or topic == "thief" :
			embed=discord.Embed(title="**Thief**", description="**<:ShieldBug:649157223905492992>Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/639473408563740681.png?v=1")
			embed.add_field(name="**Description**", value="The most risky class with close ranged high damage", inline=False)
			embed.add_field(name="**Skills**", value="Stab", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Special**", value="Lower Base HP higher Base dmg", inline=False)
			embed.add_field(name="**Specialization**", value="Rogue or Mesmer", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Assassin" or topic == "assassin" :
			embed=discord.Embed(title="**Assassin**", description="**<:ShieldBug:649157223905492992>Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/752638205760897034.png?v=1")
			embed.add_field(name="**Description**", value="Higher Crit damage but low health", inline=False)
			embed.add_field(name="**Skills**", value="Shoot, Strike", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Special**", value="40% Chance to deal 120% Dmg -20Hp", inline=False)
			embed.add_field(name="**Specialization**", value="None yet!", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Ranger" or topic == "ranger" :
			embed=discord.Embed(title="**Ranger**", description="**<:ShieldBug:649157223905492992>Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/752638206285185116.png?v=1")
			embed.add_field(name="**Description**", value="Always sure to hit for a decent amount of damage", inline=False)
			embed.add_field(name="**Skills**", value="Shoot, Strike", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Special**", value="Higher Minimal Dmg", inline=False)
			embed.add_field(name="**Specialization**", value="None yet!", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Samurai" or topic == "samurai" :
			embed=discord.Embed(title="**Samurai**", description="**<:ShieldBug:649157223905492992>Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/752638205920018603.png?v=1")
			embed.add_field(name="**Description**", value="Defensive playstile", inline=False)
			embed.add_field(name="**Skills**", value="Swing, Protrude", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Special**", value="Chance to evade attack", inline=False)
			embed.add_field(name="**Specialization**", value="None yet!", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Paladin" or topic == "paladin" :
			embed=discord.Embed(title="**Paladin**", description="**<:ShieldBug:649157223905492992>Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="")
			embed.add_field(name="**Description**", value="", inline=False)
			embed.add_field(name="**Skills**", value="", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Special**", value="", inline=False)
			embed.add_field(name="**Specialization**", value="", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Necromancer" or topic == "necromancer" :
			embed=discord.Embed(title="**Necromancer**", description="**<:ShieldBug:649157223905492992>Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="")
			embed.add_field(name="**Description**", value="", inline=False)
			embed.add_field(name="**Skills**", value="", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Special**", value="", inline=False)
			embed.add_field(name="**Specialization**", value="", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Elementalist" or topic == "elementalist" :
			embed=discord.Embed(title="**Elementalist**", description="**<:ShieldBug:649157223905492992>Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="")
			embed.add_field(name="**Description**", value="", inline=False)
			embed.add_field(name="**Skills**", value="", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Special**", value="", inline=False)
			embed.add_field(name="**Specialization**", value="", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Rogue" or topic == "rogue" :
			embed=discord.Embed(title="**Rogue**", description="**<:ShieldBug:649157223905492992>Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="")
			embed.add_field(name="**Description**", value="", inline=False)
			embed.add_field(name="**Skills**", value="", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Special**", value="", inline=False)
			embed.add_field(name="**Specialization**", value="", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Mesmer" or topic == "mesmer" :
			embed=discord.Embed(title="**Mesmer**", description="**<:ShieldBug:649157223905492992>Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="")
			embed.add_field(name="**Description**", value="", inline=False)
			embed.add_field(name="**Skills**", value="", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Special**", value="", inline=False)
			embed.add_field(name="**Specialization**", value="", inline=False)
			embed.add_field(name="Back Story", value="None!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "3" or topic =="page 3/3":
			embed=discord.Embed(color=discord.Colour(0xffffff))
			embed.add_field(name="**Wiki topics**", value="Page 3".format(ctx.prefix, ctx.prefix), inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>Monsters", value="Rachi, Debin, Oofer, Wyvern, Wolf, Goblin, Zombie, Draugr, Stalker, Souleater, Elder Dragon, Hades, Ebony Guardian, Harpy, Dormammu, Ettin, Largos, Deathclaw, Saurian", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>Races", value="Orc, Human, Elf, Demon", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>Ranking", value="Users, Guilds", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>Weapons", value="Starter Bow, Starter Sword, Starter Staff, Starter Dagger,Iron Claws, Iron Mace, Curved Dagger, Tomb of Water, Spiked Mace, Mithril Sword, Etched Longbow, Verdant Bow, Excalibur, Twilight, Devil's Kiss, Hawkeye, Solarflare, Thunderguard, Doomblade, Deathraze, Soulreaper", inline=True)
			embed.add_field(name="<:ShieldCross:560804112548233217>Daily", value="Checkin, Vote", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>Equip", value="Weapons, armor", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>Market", value="Sell, Buy,", inline=False)
			embed.set_footer(text="submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)



		elif topic == "elf":
			title="<:ShieldBug:649157223905492992>Elf"
			description="In the lush forested areas of east Solyx, the elves thrive. While their bodies are naturally slim, they are surprisingly strong and can easily hold their own in a fight. However, elves do not prioritize physical strength; instead favoring the charismatic members of society. While many things can be seen as status symbols to individual elf communities, the pointiness of their ears is the most common way an elf shows off their looks."
			footer="Submitted by (8ᘌꇤ⁐ꃳ 三#2369\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.".format(ctx.prefix)
			icon = guild.icon_url

		elif topic == "orc":
			title="<:ShieldBug:649157223905492992>Orc"
			description="To the far west of Solyx, deep into the cold and dangerous mountain ranges, lies the kingdom of the orc. This grand and heavily fortified city is home to the orcs. To survive the cold and harsh lands they live in, the orcs have to go through hellish training, starting from the day they can walk. Once they become of age, these fierce creatures will have been shaped up to be the pinnacle of raw physical strength, and combat prowess."
			footer="Submitted by Rideric#4935\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.".format(ctx.prefix)
			icon = guild.icon_url







		elif topic == "test" or topic == "testing":
			title="<:ShieldBug:649157223905492992>Test123"
			description="**\u27a4 Health** - 1 \n**\u27a4 Damage** - 2 \n**\u27a4 Gold** - 3 \n**\u27a4 Exp** - 4 \n \n  yes sum text blabla big monster RAWR big mad long story \n"
			footer="Submitted by your mom **>:c**\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.".format(ctx.prefix)
			icon = ('https://cdn.discordapp.com/attachments/750681506262810624/751520899848601620/unknown.png')

		elif topic == "guild bonus" or topic == "guildbonus":
			title= "<:ShieldBug:649157223905492992>Guild Bonus"
			description="The guild bonus adds a percentage of gold-gain on top of the regular gold income from an enemy kill.\n\nIt works through an equation which we shall not bore you with here. Simply put, the higher the bonus, the higher the chance of more bonus gold.\n\n-The bonus applies to all those who represent the guild\n-The bonus starts at 0 can be increased by donating gold to the guild"
			footer="submitted by AceTheBear223#4562\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.".format(ctx.prefix)
			icon = ('https://cdn.discordapp.com/emojis/560844076967002112.png?v=1') #https://cdn.discordapp.com/attachments/737821854680744017/751554397456040088/unknown.png

		try:
			em = discord.Embed(title=title, description=description, color=discord.Colour(0xffffff))
			em.set_footer(text=footer)
			em.set_thumbnail(url=icon)
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(ctx.message.channel, "I cound't send the message.")
			except:
				return


def setup(bot):
    n = wiki(bot)
    bot.add_cog(n)
