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
		user = ctx.author

		if topic == None:
			embed=discord.Embed(color=discord.Colour(0xffffff))
			embed.add_field(name="<:ShieldCheck:560804135545602078>**Wiki Mainpage**", value="\n\nPage 1/4\n\nWiki usage: {}wiki [page].\n Or\nWiki usage: {}wiki [subject].\n\nEmote Meanings\n <:ShieldCheck:560804135545602078> = Works Completely! \n :book: = Missing Backstory \n <:ShieldBug:649157223905492992> = Working on it!\n <:ShieldBroken:649157253701566474> = Is made but broken...\n <:ShieldCross:560804112548233217> = Hasnt been made yet.\n\n If a item has a :book: emote you can help to submit a backstory if you want!\n\nCurrent pages 1, 2, 3, 4\n\n".format(ctx.prefix, ctx.prefix), inline=False)

			embed.set_footer(text="submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")

			await ctx.send(embed=embed)

#			abcdefghijklmnopqsrtuvwxyz

#           <:ShieldCheck:560804135545602078> = Works Completely!
#           <:ShieldBug:649157223905492992> = Working on it!
#			:book: = Story not been submitted yet.
#           <:ShieldBroken:649157253701566474> = Is made but broken...
#           <:ShieldCross:560804112548233217> = Hasnt been made yet.
#			<:Archer:639473419703812122> = Archer emote
#			<:ThumbsUp:560804155321614347> = Thumbs up!
#			<:Gold:639484869809930251> = Gold
#			<:HealingPotion:573577125064605706> = Hp pot small
#			<:Lootbag:573575192224464919> = lb  
#			<:Key:573780034355986432>= key
#			<:Wood:573574660185260042> = wood 
#			<:Stone:573574662525550593> = stone
#			<:Metal:573574661108006915> = metal


		elif topic == "Emotes" or topic == "emotes":
			embed=discord.Embed(color=discord.Colour(0xffffff))
			embed.add_field(name="**Emotes list**", value="<:ShieldCheck:560804135545602078> <:ShieldBug:649157223905492992> <:ShieldBroken:649157253701566474> <:ShieldCross:560804112548233217> <:Archer:752633441282949222> <:Knight:752633441362903120> <:Mage:752633441626882058> <:Thief:752633441811693638> <:Assasin:752638205760897034> <:Ranger:752638206285185116> <:Paladin:752638205869949168> <:Samurai:752638205920018603> <:Necromancer:752638205832069191> <:Elementalist:752638205584474164> <:Mesmer:752638205697851413> <:Rogue:752638205928538252>", inline=False)
			await ctx.send(embed=embed)
			 

		elif topic == "2" or topic =="page 2" or topic == "page 2/4" or topic =="2/4":
			embed=discord.Embed(color=discord.Colour(0xffffff))
			embed.add_field(name="**Wiki topics**", value="Page 2/3".format(ctx.prefix, ctx.prefix), inline=False)
			embed.add_field(name="<:ShieldCheck:560804135545602078>Armor", value="Chainmail, Barbaric, Pit Fighter, Banded, Leather, Iron, Branded Metal,        Wolf Fur, Enchanted Steel, Bane Of The Goblin Lord, Nighstalker Mantle, Hephaestus Armor, ", inline=False)
			embed.add_field(name="<:ShieldCheck:560804135545602078>Bosses", value="Phantasm, Fire Golem, The Corrupted, The Accursed, The Nameless King, The Venomous, Death Knight, Frost Dragon", inline=False)
			embed.add_field(name="<:ShieldCheck:560804135545602078>Classes", value="Archer, Knight, Mage, Thief, Assassin, Ranger, Samurai, Paladin, Necromancer, Elementalist, Rogue, Mesmer", inline=False)
			embed.add_field(name="<:ShieldCheck:560804135545602078>Daily", value="Daily/Checkin, Vote", inline=False)
			embed.add_field(name="<:ShieldCheck:560804135545602078>Equip", value="Weapons, armor", inline=False)			
			embed.add_field(name="<:ShieldCheck:560804135545602078>Fighting", value="PVE, PVP", inline=False)
			embed.add_field(name="<:ShieldCheck:560804135545602078>Gathering", value="Chop, Mine, Wood, Stone, Metal, Fish", inline=False)
			embed.add_field(name="<:ShieldCheck:560804135545602078>Guild", value="Info, Represent, Mission, Donate, Promote, Demote, Tag", inline=False)
			embed.set_footer(text="submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
		elif topic == "Chainmail" or topic == "chainmail" or topic == "Chainmail Armor" or topic == "chainmail armor":
			embed=discord.Embed(title="**Chainmail Armor**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Common", inline=False)
			embed.add_field(name="**Defense**", value="2 - 12", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Barbaric" or topic == "barbaric" or  topic == "Barbaric Armor" or topic == "barbaric armor":
			embed=discord.Embed(title="**Barbaric Armor**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Common", inline=False)
			embed.add_field(name="**Defense**", value="5 - 7", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Pit fighter" or topic == "pit fighter" or topic == "Pit fighter Armor" or topic == "pit fighter armor":
			embed=discord.Embed(title="**Pit fighter**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Common", inline=False)
			embed.add_field(name="**Defense**", value="4 - 9", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Banded" or topic == "banded" or topic == "Banded Armor" or topic == "banded armor":
			embed=discord.Embed(title="**Banded Armor**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Common", inline=False)
			embed.add_field(name="**Defense**", value="1 - 10", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Leather" or topic == "leather" or topic == "Leather Armor" or topic == "leather armor":
			embed=discord.Embed(title="**Leather Armor**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Common", inline=False)
			embed.add_field(name="**Defense**", value="3 - 8", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Iron" or topic == "iron" or topic == "Iron Armor" or topic == "iron armor":
			embed=discord.Embed(title="**Iron Armor**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Rare", inline=False)
			embed.add_field(name="**Defense**", value="14 - 16", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Branded Metal" or topic == "branded metal" or topic == "Branded Metal Armor" or topic == "branded metal":
			embed=discord.Embed(title="**Branded Metal Armor**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Rare", inline=False)
			embed.add_field(name="**Defense**", value="13 - 17", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Wolf Fur" or topic == "wolf fur" or  topic == "Wolf Fur Armor" or topic == "wolf fur armor":
			embed=discord.Embed(title="**Wolf Fur**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Rare", inline=False)
			embed.add_field(name="**Defense**", value="1 - 24", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Enchanted Steel" or topic == "enchanted steel" or topic == "Enchanted Steel Armor" or topic == "enchanted steel armor":
			embed=discord.Embed(title="**Enchanted Steel Armor**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Rare", inline=False)
			embed.add_field(name="**Defense**", value="12 - 17", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Bane Of The Goblin Lord" or topic == "bane of the goblin lord" or topic == "Bane Of The Goblin Lord Armor" or topic == "bane of the goblin lord armor":
			embed=discord.Embed(title="**Bane Of The Goblin Lord**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Legendary", inline=False)
			embed.add_field(name="**Defense**", value="20 - 25", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Nightstalker Mantle" or topic == "nightstalker mantle" or topic == "Nightstalker Mantle Armor" or topic == "nightstalker mantle armor":
			embed=discord.Embed(title="**Nightstalker Mantle**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Legendary", inline=False)
			embed.add_field(name="**Defense**", value="15 - 28", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Hephaestus Armor" or topic == "hephaestus armor":
			embed=discord.Embed(title="**Hephaestus Armor**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Armor", inline=False)
			embed.add_field(name="**Rarity**", value="Legendary", inline=False)
			embed.add_field(name="**Defense**", value="16 - 27", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Phantasm" or topic == "phantasm" or  topic == "Phantasm" or topic == "phantasm":
			embed=discord.Embed(title="**Phantasm**", description="**<:ShieldCheck:560804135545602078>Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="https://i.imgur.com/BbBmEOF.jpg")
			embed.add_field(name="**Type**", value="Boss", inline=False)
			embed.add_field(name="**Place**", value="The Forest", inline=False)
			embed.add_field(name="**Health**", value="60Hp - 80Hp", inline=False)
			embed.add_field(name="**Damage**", value="10Dmg - 15Dmg", inline=False)
			embed.add_field(name="**Gold**", value="20G  - 30G", inline=False)
			embed.add_field(name="**Experience**", value="15Exp - 30Exp", inline=False)
			embed.add_field(name="Back Story", value="The Phantasm has long protected The Forest. The Monks prayed and offered sacrifices to keep it satisfied. The Phantasm resides near hidden lakes throughout the forest, as the water is it's life source. As the praying monks became extinct it no longer has any peace. Whenever the Phantasm feels threatened it gathers dark clouds and density into an eerie storm. It uses it's long slithering body to smother its threats. And guides the lightning of the storm onto it's foes.", inline=False)
			embed.set_footer(text="Submitted by AceTheBear223#4562\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Fire Golem" or topic == "fire golem":
			embed=discord.Embed(title="**Fire Golem**", description="**<:ShieldCheck:560804135545602078>Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/intermediary/f/c7f23f41-5bd8-4b82-a00c-d61b0cfb0160/d9p8w3t-e2e0278a-7b05-4d6b-9a69-c50f3f005126.png/v1/fill/w_700,h_331,q_70,strp/fire_golem_by_sourshade_d9p8w3t-350t.jpg")
			embed.add_field(name="**Type**", value="Boss", inline=False)
			embed.add_field(name="**Place**", value="Golden Temple", inline=False)
			embed.add_field(name="**Health**", value="30Hp - 50Hp", inline=False)
			embed.add_field(name="**Damage**", value="10Dmg - 20Dmg", inline=False)
			embed.add_field(name="**Gold**", value="25G  - 35G", inline=False)
			embed.add_field(name="**Experience**", value="20Exp - 35Exp", inline=False)
			embed.add_field(name="Back Story", value="The fire golem's name speaks for itself. The golems arose from the depths of a volcano, summoned by an ancient group of druids to protect the Golden Temple. The golem's bodies are made from magnetized lava rock. built to withstand high pressure and has strong resistance against piercing attacks. Long have the golems been asleep. But the increase of wandering adventurers have woken them once more. The golems have no feelings and only one objective in mind. To kill tresspassers.", inline=False)
			embed.set_footer(text="Submitted by AceTheBear223#4562\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "corrupted" or topic == "the corrupted" or topic == "The Corrupted" or topic == "Corrupted":
			
			embed=discord.Embed(title="**The Corrupted**", description="**<:ShieldCheck:560804135545602078>Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="https://i.imgur.com/oTi3K3q.jpg")
			embed.add_field(name="**Type**", value="Boss", inline=False)
			embed.add_field(name="**Place**", value="Saker Keep", inline=False)
			embed.add_field(name="**Health**", value="70Hp - 90Hp", inline=False)
			embed.add_field(name="**Damage**", value="15 - 30Dmg", inline=False)
			embed.add_field(name="**Gold**", value="30G  - 50G", inline=False)
			embed.add_field(name="**Experience**", value="30Exp - 40Exp", inline=False)
			embed.add_field(name="Back Story", value="The Corrupted originally came from a relatively peaceful race of dragons. Their emerald green scales became a very wanted loot amongst adventurers. The adventurers betrayed the race it's trust and slaughtered almost all of the dragons. The survivors went into a frenzy. No longer able to tell any difference between living beings. The Corrupted kill blindly. Their snake like fangs have teared trough many houses and castles alike. Their horns grow as they kill, and their roaring can be heard from afar. Now they roam the ruins of Saker Keep.", inline=False)
			embed.set_footer(text="Submitted by AceTheBear223#4562\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "The Accursed" or topic == "Accursed" or topic == "the accursed" or topic == "accursed":
			embed=discord.Embed(title="**The Accursed**", description="**:book:Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Boss", inline=False)
			embed.add_field(name="**Place**", value="Ebony Mountains", inline=False)
			embed.add_field(name="**Health**", value="70Hp - 90Hp", inline=False)
			embed.add_field(name="**Damage**", value="20Dmg - 40Dmg", inline=False)
			embed.add_field(name="**Gold**", value="40G  - 55G", inline=False)
			embed.add_field(name="**Experience**", value="35Exp - 45Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "The Nameless King" or topic == "the nameless king" or topic == "Nameless King" or topic == "nameless king":
			embed=discord.Embed(title="**The Nameless King**", description="**:book:Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Boss", inline=False)
			embed.add_field(name="**Place**", value="Township of Arkina", inline=False)
			embed.add_field(name="**Health**", value="100Hp - 120Hp", inline=False)
			embed.add_field(name="**Damage**", value="25Dmg - 40Dmg", inline=False)
			embed.add_field(name="**Gold**", value="45G  - 60G", inline=False)
			embed.add_field(name="**Experience**", value="40Exp - 50Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "The Venomous" or topic == "the venomous" or topic == "Venomous" or topic == "venomous":
			embed=discord.Embed(title="**The Venomous**", description="**:book:Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="https://i.pinimg.com/originals/d3/5e/fb/d35efb16a4e1aeee4e0119c8a2257fca.jpg")
			embed.add_field(name="**Type**", value="Boss", inline=False)
			embed.add_field(name="**Place**", value="Zulanthu", inline=False)
			embed.add_field(name="**Health**", value="110Hp - 130Hp", inline=False)
			embed.add_field(name="**Damage**", value="25Dmg - 50Dmg", inline=False)
			embed.add_field(name="**Gold**", value="45G - 55G", inline=False)
			embed.add_field(name="**Experience**", value="40Exp - 55Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Death Knight" or topic == "death knight":
			embed=discord.Embed(title="**Death Knight**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="https://i.imgur.com/ELd7Ll5.jpg")
			embed.add_field(name="**Type**", value="Boss", inline=False)
			embed.add_field(name="**Place**", value="Lost city", inline=False)
			embed.add_field(name="**Health**", value="110Hp - 130Hp", inline=False)
			embed.add_field(name="**Damage**", value="45Dmg - 66Dmg", inline=False)
			embed.add_field(name="**Gold**", value="35G  - 37G", inline=False)
			embed.add_field(name="**Experience**", value="45Exp - 60Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Frost Dragon" or topic == "frost dragon":
			embed=discord.Embed(title="**Frost Dragon**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="https://cdn.wallpapersafari.com/11/55/3hBQ9Z.jpg")
			embed.add_field(name="**Type**", value="Boss", inline=False)
			embed.add_field(name="**Place**", value="Drenheim", inline=False)
			embed.add_field(name="**Health**", value="130Hp - 150Hp", inline=False)
			embed.add_field(name="**Damage**", value="35Dmg - 60Dmg", inline=False)
			embed.add_field(name="**Gold**", value="55G  - 70G", inline=False)
			embed.add_field(name="**Experience**", value="50Exp - 65Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Archer" or topic == "archer" :
			embed=discord.Embed(title="**Archer**", description="**:book:Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/639473419703812122.png?")
			embed.add_field(name="**Description**", value="Precise and long ranged damage, chance at a critical strike.", inline=False)
			embed.add_field(name="**Skills**", value="Shoot", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Special**", value="20% Change to deal 120% Damage.", inline=False)
			embed.add_field(name="**Specialization**", value="Assassin or Ranger", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Knight" or topic == "knight" :
			embed=discord.Embed(title="**Knight**", description="**:book:Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/639473415492861972.png?v=1")
			embed.add_field(name="**Description**", value="Tanky class with close combat damage reduction.", inline=False)
			embed.add_field(name="**Skills**", value="Swing", inline=False)
			embed.add_field(name="**Special**", value="8 - 15 Damage reduction.", inline=False)
			embed.add_field(name="**Specialization**", value="Paladin or Samurai", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Mage" or topic == "mage" :
			embed=discord.Embed(title="**Mage**", description="**:book:Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/639473422040301574.png?v=1")
			embed.add_field(name="**Description**", value="Long ranged average damage class with epic items.", inline=False)
			embed.add_field(name="**Skills**", value="Cast", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Special**", value="AOE damage (Area of Effect).", inline=False)
			embed.add_field(name="**Specialization**", value="Necromancer or Elementalist", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Thief" or topic == "thief" :
			embed=discord.Embed(title="**Thief**", description="**:book:Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/639473408563740681.png?v=1")
			embed.add_field(name="**Description**", value="The most risky class with close ranged attackes with high damage.", inline=False)
			embed.add_field(name="**Skills**", value="Stab", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Special**", value="Lower base health higher base damage.", inline=False)
			embed.add_field(name="**Specialization**", value="Rogue or Mesmer", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Assassin" or topic == "assassin" :
			embed=discord.Embed(title="**Assassin**", description="**:book:Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/752638205760897034.png?v=1")
			embed.add_field(name="**Description**", value="Higher Crit damage but low health.", inline=False)
			embed.add_field(name="**Skills**", value="Shoot, Corrupt", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Special**", value="40% Chance to deal 120% Damage -20 Health.", inline=False)
			embed.add_field(name="**Specialization**", value="None yet!", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Ranger" or topic == "ranger" :
			embed=discord.Embed(title="**Ranger**", description="**:book:Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/752638206285185116.png?v=1")
			embed.add_field(name="**Description**", value="Always sure to hit for a decent amount of damage.", inline=False)
			embed.add_field(name="**Skills**", value="Shoot, Strike", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Special**", value="Higher Minimal damage.", inline=False)
			embed.add_field(name="**Specialization**", value="None yet!", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Samurai" or topic == "samurai" :
			embed=discord.Embed(title="**Samurai**", description="**:book:Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/752638205920018603.png?v=1")
			embed.add_field(name="**Description**", value="Defensive playstyle.", inline=False)
			embed.add_field(name="**Skills**", value="Swing, Protrude", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Special**", value="Chance to evade attack!", inline=False)
			embed.add_field(name="**Specialization**", value="None yet!", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Paladin" or topic == "paladin" :
			embed=discord.Embed(title="**Paladin**", description="**:book:Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/752638205869949168.png?v=1")
			embed.add_field(name="**Description**", value="Brutal attacks.", inline=False)
			embed.add_field(name="**Skills**", value="Swing, Fussilade", inline=False)
			embed.add_field(name="**Special**", value="5 - 10 Reduced enemy damage.", inline=False)
			embed.add_field(name="**Specialization**", value="None yet!", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Necromancer" or topic == "necromancer" :
			embed=discord.Embed(title="**Necromancer**", description="**:book:Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/752638205832069191.png?v=1")
			embed.add_field(name="**Description**", value="Wield the power of the dead.", inline=False)
			embed.add_field(name="**Skills**", value="Cast, Reap", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Special**", value="Be able to revive your Companion!", inline=False)
			embed.add_field(name="**Specialization**", value="None yet!", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Elementalist" or topic == "elementalist" :
			embed=discord.Embed(title="**Elementalist**", description="**:book:Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/752638205584474164.png?v=1")
			embed.add_field(name="**Description**", value="Controll all the elements.", inline=False)
			embed.add_field(name="**Skills**", value="Cast, Overload", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Special**", value="Chance to stun an enemy with an element!", inline=False)
			embed.add_field(name="**Specialization**", value="None yet!", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Rogue" or topic == "rogue" :
			embed=discord.Embed(title="**Rogue**", description="**:book:Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/752638205928538252.png?v=1")
			embed.add_field(name="**Description**", value="Quick and brutal attacks", inline=False)
			embed.add_field(name="**Skills**", value="Stab, Parry", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Special**", value="Small chance to attack twice!", inline=False)
			embed.add_field(name="**Specialization**", value="None yet", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Mesmer" or topic == "mesmer" :
			embed=discord.Embed(title="**Mesmer**", description="**:book:Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/752638205697851413.png?v=1")
			embed.add_field(name="**Description**", value="Master of confusion and movement.", inline=False)
			embed.add_field(name="**Skills**", value="Stab, Distort", inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Special**", value="Small chance for the enemy to inflict self damage.", inline=False)
			embed.add_field(name="**Specialization**", value="None yet!", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Daily" or topic == "daily" or topic == "Checkin" or topic == "checkin":
			embed=discord.Embed(title="**Daily**", description="<:ShieldBug:649157223905492992>**Wiki** Page 1/2", color=discord.Colour(0xffffff))
			embed.add_field(name="**Useage**", value="Just type {}daily <:ThumbsUp:560804155321614347>.".format(ctx.prefix), inline=False)
			embed.add_field(name="**Rewards Normal**", value="<:Gold:639484869809930251> = 200 to 400\n<:HealingPotion:573577125064605706> = 2 to 5\n<:Lootbag:573575192224464919> = 3 to 5\n<:Key:573780034355986432> = 3 to 5\n<:Wood:573574660185260042> = 10 to 20 \n<:Stone:573574662525550593> = 10 to 20 \n<:Metal:573574661108006915> = 4 to 10", inline=False)
			embed.add_field(name="**Cooldown**", value="Every 24 hours!".format(ctx.prefix), inline=False)
			await ctx.send(embed=embed)

		elif topic == "Daily 2" or topic == "daily 2" or topic == "Checkin 2" or topic == "checkin 2":
			embed=discord.Embed(title="**Daily**", description="<:ShieldBug:649157223905492992>**Wiki** Page 2/2", color=discord.Colour(0xffffff))
			embed.add_field(name="**Rewards Donator**", value="<:Gold:639484869809930251> = 360 to 600\n<:HealingPotion:573577125064605706> = 3 to 6\n<:Lootbag:573575192224464919> = 5 to 9\n<:Key:573780034355986432> = 5 to 9\n<:Wood:573574660185260042> = 15 to 25 \n<:Stone:573574662525550593> = 15 to 25 \n<:Metal:573574661108006915> = 6 to 12", inline=False)
			embed.add_field(name="**Rewards Subscriber**", value="<:Gold:639484869809930251> = 450 to 750\n<:HealingPotion:573577125064605706> = 6 to 9\n<:Lootbag:573575192224464919> = 7 to 12\n<:Key:573780034355986432> = 7 to 12\n<:Wood:573574660185260042> = 20 to 30 \n<:Stone:573574662525550593> = 20 to 30 \n<:Metal:573574661108006915> = 10 to 18", inline=False)
			await ctx.send(embed=embed)

		elif topic == "Weapon" or topic == "weapon" or topic == "equip weapon" or topic == "Equip Weapon":
			embed=discord.Embed(title="**Equip Weapon**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.add_field(name="**Equiping a weapon**", value="Will give you extra damage in battle", inline=False)
			embed.add_field(name="**how to use**", value="type {}equip weapon <number>\n Rules: you can only equip a weapon fit for your class \nstaff for mage and bow for archer etc.".format(ctx.prefix), inline=False)
			await ctx.send(embed=embed)
		
		elif topic == "armor" or topic == "Armor" or topic == "equip armor" or topic == "Equip Armor":
			embed=discord.Embed(title="**Equip Armor**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.add_field(name="**Equiping Armor**", value="Will give you extra damage reduction in battle\nArmor is being made soon!", inline=False)
			embed.add_field(name="**how to use**", value="type {}equip armor <number>\n Any character can equip any armor!".format(ctx.prefix), inline=False)
			await ctx.send(embed=embed)

		elif topic == "PVE" or topic == "pve":
			embed=discord.Embed(title="**PVE**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.add_field(name="**Pve meaning**", value="short for player versus environment.", inline=False)
			embed.add_field(name="**Pve in Solyx**", value="For now the only pve fights are with {}fight.".format(ctx.prefix), inline=False)
			await ctx.send(embed=embed)

		elif topic == "PVP" or topic == "pvp":
			embed=discord.Embed(title="**PVP**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/573580993055686657.png?v=1")
			embed.add_field(name="**PvP meaning**", value="short for player versus player.", inline=False)
			embed.add_field(name="**PvP in Solyx**", value="For now the only pvp fights are with {}battle.".format(ctx.prefix), inline=False)
			await ctx.send(embed=embed)

		elif topic == "Chop" or topic == "chop":
			embed=discord.Embed(title="**Chop**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/573574740220969007.png?v=1")
			embed.add_field(name="**Usage**", value="Just type {}chop <:ThumbsUp:560804155321614347>".format(ctx.prefix), inline=False)
			embed.add_field(name="**Chopping**", value="With the {}chop command you gather 1 to 5 wood.".format(ctx.prefix), inline=False)
			embed.add_field(name="**Cooldown**", value="10 Minutes", inline=False)
			await ctx.send(embed=embed)
			
		elif topic == "Mine" or topic == "mine":
			embed=discord.Embed(title="**Mine**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/573574740640530471.png?v=1")
			embed.add_field(name="**Usage**", value="Just type {}mine <:ThumbsUp:560804155321614347>".format(ctx.prefix), inline=False)
			embed.add_field(name="**Mining**", value="With the {}mine command you gather 1 to 5 stone and 0 to 2.".format(ctx.prefix), inline=False)
			embed.add_field(name="**Cooldown**", value="10 Minutes", inline=False)
			await ctx.send(embed=embed)

		elif topic == "Fish" or topic == "fish":
			embed=discord.Embed(title="**Fish**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://discord.com/assets/2d827842d29f3408d9eb56fcdd96e589.svg")
			embed.add_field(name="**Usage**", value="Just type {}fish <:ThumbsUp:560804155321614347>".format(ctx.prefix), inline=False)
			embed.add_field(name="**Fishing**", value="With the {}fish command you can fish up multiple things.\n"":fish:"" = +5G\n"":tropical_fish:"" = +10G\n"":blowfish:"" = +4G\n"":prayer_beads:"" = +15G\n"":key2:"" = +2G\n"":paperclip:"" = +2G\n"":potato:"" = +2G\n"":wastebasket:"" = -10G\n"":crab:"" = -5G\n".format(ctx.prefix), inline=False)
			embed.add_field(name="**Cooldown**", value="4 seconds", inline=False)
			embed.add_field(name="**Texts**", value=":fishing_pole_and_fish: **| "+ (user.name) + " , you caught (fish or item)!** *+GoldAmount*\n:fishing_pole_and_fish: **|"+ (user.name) + ", your line broke when you caught (fish or item)!** *+GoldAmount*\n:fishing_pole_and_fish: **|"+ (user.name) + ", you caught (fish or item)!** *-GoldAmount*\n"":fishing_pole_and_fish: **| Uh-oh! "+ (user.name) + " failed to catch anything!**")
			await ctx.send(embed=embed)

		elif topic == "Wood" or topic == "wood":
			embed=discord.Embed(title="**Wood**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/573574660185260042.png?v=1")
			embed.add_field(name="**Gathering**", value="There are multiple ways you can get wood.", inline=False)
			embed.add_field(name="**Chopping**", value="With the {}chop command you gather 1 to 5 wood.".format(ctx.prefix), inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Crates**", value="With the {}crate/{}lb you gather 1 to 3 wood.".format(ctx.prefix, ctx.prefix), inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Daily**", value="With the {}daily/{}checkin you gather 10 to 20 wood.".format(ctx.prefix, ctx.prefix), inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Vote**", value="With the {}vote you gather 10 to 20 wood.".format(ctx.prefix), inline=False)
			await ctx.send(embed=embed)

		elif topic == "Stone" or topic == "stone":
			embed=discord.Embed(title="**Stone**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/573574662525550593.png?v=1")
			embed.add_field(name="**Gathering**", value="There are multiple ways you can get stone.", inline=False)
			embed.add_field(name="**Mining**", value="With the {}mine command you gather 1 to 5 stone.".format(ctx.prefix), inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Crates**", value="With the {}crate/{}lb you gather 1 to 3 stone.".format(ctx.prefix, ctx.prefix), inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Daily**", value="With the {}daily/{}checkin you gather 10 to 20 stone.".format(ctx.prefix, ctx.prefix), inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Vote**", value="With the {}vote you gather 10 to 20 stone.".format(ctx.prefix), inline=False)
			await ctx.send(embed=embed)

		elif topic == "Metal" or topic == "metal":
			embed=discord.Embed(title="**Metal**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/573574661108006915.png?v=1")
			embed.add_field(name="**Gathering**", value="There are multiple ways you can get metal.", inline=False)
			embed.add_field(name="**Chopping**", value="With the {}mine command you gather 0 to 2 metal.".format(ctx.prefix), inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Crates**", value="With the {}crate/{}lb you gather 1 metal.".format(ctx.prefix, ctx.prefix), inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Daily**", value="With the {}daily/{}checkin you gather 3 to 9 metal.".format(ctx.prefix, ctx.prefix), inline=False)
			embed.add_field(name="<:ShieldCross:560804112548233217>**Vote**", value="With the {}vote you gather 4 to 10 metal.".format(ctx.prefix), inline=False)
			await ctx.send(embed=embed)

		elif topic == "info" or topic == "Info" or topic == " Guild Info" or topic == "guild info":
			embed=discord.Embed(title="**Guild Info**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="**Guild info**", value="it does not represent Server info it shows the info of the RPG guild.\nEvery server solyx is in is a guild.", inline=False)
			embed.add_field(name="Name", value="Name of the server.", inline=False)
			embed.add_field(name="Title", value="represents the level of the guild. (check {}wiki Titles Guilds).".format(ctx.prefix), inline=False)
			embed.add_field(name="Leader", value="Server owner.", inline=False)
			embed.add_field(name="Members", value="server members", inline=False)
			embed.add_field(name="Level", value="level of the guild not Nitro boost.", inline=False)
			embed.add_field(name="Exp", value="the guild Exp.", inline=False)
			embed.add_field(name="Bonus", value="Guild Bonus (check {}wiki guild bonus).".format(ctx.prefix), inline=False)
			embed.add_field(name="Health", value="the guild HP If the guild hp reaches 0 the stats get reset back to 0\n level, exp and bonus.\n to keep the hp up, complete missions!.", inline=False)
			await ctx.send(embed=embed)

		elif topic == "Guild Represent" or topic == "Represent" or topic == "guild represent" or topic == "represent":
			embed=discord.Embed(title="**Guild Represent**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="Usage", value="Just type {}guild Represent<:ThumbsUp:560804155321614347>".format(ctx.prefix), inline=False)
			embed.add_field(name="Explanation", value="When you represent a guild you join that guild you said it in.\nThe guild name will be shown in you status.\n you also gain that guilds guildbonus.\nYou also will join the guild mission!", inline=False)
			await ctx.send(embed=embed)

		elif topic == "Guild Mission" or topic == "Mission" or topic == "guild mission" or topic == "mission":
			embed=discord.Embed(title="**Guild Mission**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="Usage", value="Just type {}guild mission<:ThumbsUp:560804155321614347>".format(ctx.prefix), inline=False)
			embed.add_field(name="Meaning", value="Guild missions keep your guild HP up to 100 and give it Exp to level up!", inline=False)
			embed.add_field(name="Missions", value="Collect 200 wood, Collect 120 metal, Check-in 10 times, Kill 400 Oofers, Kill 100 Goblins, Donate 35000 to the guild", inline=False)
			embed.add_field(name="Rewards", value="All missions get 10 to 40 exp once finshed except,\nKill 400 Oofers gets 10 - 50Exp\nKill 100 Goblins gets 10 - 30Exp", inline=False)
			await ctx.send(embed=embed)

		elif topic == "Guild Donate" or topic == "Donate" or topic == "guild donate" or topic == "donate":
			embed=discord.Embed(title="**Guild Donate**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="Usage", value="Just type {}guild donate <amount><:ThumbsUp:560804155321614347>".format(ctx.prefix), inline=False)
			embed.add_field(name="Benefits", value="Donation gold to your guild grants it a Guildbonus.", inline=False)
			embed.add_field(name="Stats", value="Guild bonus is maxed at 200\nGuild bonus is calculated with\nTaxes = AmountDonated / 1000\nGuildbonus = taxes : ( 2 x membercount)", inline=False)
			await ctx.send(embed=embed)

		elif topic == "Guild Promote" or topic == "Promote" or topic == "guild promote" or topic == "promote":
			embed=discord.Embed(title="**Guild Promote**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="Usage", value="Just type {}guild promote<:ThumbsUp:560804155321614347>".format(ctx.prefix), inline=False)
			embed.add_field(name="Officers", value="can promote and demote members".format(ctx.prefix), inline=False)
			await ctx.send(embed=embed)

		elif topic == "Guild Demote" or topic == "Demote" or topic == "guild demote" or topic == "demote":
			embed=discord.Embed(title="**Guild Demote**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="Usage", value="Just type {}guild demote<:ThumbsUp:560804155321614347>".format(ctx.prefix), inline=False)
			embed.add_field(name="Officers", value="can demote members".format(ctx.prefix), inline=False)
			embed.add_field(name="Leader", value="can promote and demote officers and members".format(ctx.prefix), inline=False)
			await ctx.send(embed=embed)

		elif topic == "Guild Tag" or topic == "Tag" or topic == "guild tag" or topic == "tag":
			embed=discord.Embed(title="**Guild Tag**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="Usage", value="Just type {}guild tag (3 Letters)<:ThumbsUp:560804155321614347>".format(ctx.prefix), inline=False)
			embed.add_field(name="Leaderboard", value="The guild tag will be show in  the guild leaderboard.".format(ctx.prefix), inline=False)
			embed.add_field(name="Rules", value="Only guild owner can change the guild tag.".format(ctx.prefix), inline=False)
			await ctx.send(embed=embed)

		elif topic == "3" or topic =="page 3/4" or topic == "page 3" or topic =="3/4":
			embed=discord.Embed(color=discord.Colour(0xffffff))
			embed.add_field(name="**Wiki topics**", value="Page 3/4".format(ctx.prefix, ctx.prefix), inline=False)
			embed.add_field(name="<:ShieldCheck:560804135545602078>Items", value="Health Potions, Keys, Crates, Gold", inline=False)
			embed.add_field(name="<:ShieldCheck:560804135545602078>Market", value="Sell, Buy,", inline=False)
			embed.add_field(name="<:ShieldCheck:560804135545602078>Monsters", value="Rachi, Debin, Oofer, Wyvern, Wolf, Goblin, Zombie, Draugr, Stalker, Souleater, Elder Dragon, Hades, Ebony Guardian, Harpy, Dormammu, Ettin, Largos, Deathclaw, Saurian, Skeleton, Lizardmen, Giant, Ice Wolves, Frost Orc, Frost Goblin", inline=False)
			embed.add_field(name="<:ShieldCheck:560804135545602078>Races", value="Orc, Human, Elf, Demon", inline=False)
			embed.add_field(name="<:ShieldCheck:560804135545602078>Ranking", value="Users, Guilds", inline=False)
			embed.add_field(name="<:ShieldCheck:560804135545602078>Skills", value="Swing, Stab, Shoot, Cast, Parry, Distort, Reap, Overload, Fusillade, Protrude, Strike, Corrupt", inline=False)
			embed.add_field(name="<:ShieldCheck:560804135545602078>Titles", value="Titles Guilds, Titles Users, Achievement Titles, Level Titles, Monster Titles, Monster Titles 2", inline=False)
			embed.add_field(name="<:ShieldCheck:560804135545602078>Travel", value="Golden Temple,  Saker Keep, The Forest, Ebony Mountains, Township of Arkina,  Zulanthu, Lost City, Drenheim, Havelow, Sacred Cave, The Haunted Tomb", inline=False)
			embed.set_footer(text="submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			
			await ctx.send(embed=embed)

		elif topic == "Health" or topic == "health" or topic == "Health potion" or topic == "health potion" or topic == "Health potions" or topic == "health potions":
			embed=discord.Embed(title="**Health Potion**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/573577125064605706.png?v=1")
			embed.add_field(name="Usage", value="Just type {}heal<:ThumbsUp:560804155321614347>".format(ctx.prefix), inline=False)
			embed.add_field(name="Buy", value="To buy it type {}buy hp <amount>\nThe price changes on your level".format(ctx.prefix), inline=False)
			embed.add_field(name="Price", value="Level 0+ = 5G\nLevel 10+ = 10G\nLevel 30+ = 15G\nLevel  50+ = 20G\nLevel  70+ = 25G".format(ctx.prefix, ctx.prefix, ctx.prefix), inline=False)
			embed.add_field(name="How to get", value="You can get Health potions with {}daily, {}vote and {}lb".format(ctx.prefix, ctx.prefix, ctx.prefix), inline=False)
			embed.add_field(name="Stats", value="Minor health potions will heal you between 25 and 55 hp\nDaily will get you 2 to 5 Health potions.\nMore health potions will be added later.".format(ctx.prefix), inline=False)
			embed.set_footer(text="G = Gold, HP = Health, Level = User level.")
			await ctx.send(embed=embed)

		elif topic == "Key" or topic == "key" or topic == "Keys"or topic == "keys":
			embed=discord.Embed(title="**Key**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/573780034355986432.png?v=1")
			embed.add_field(name="Usage", value="You need 1 Key and 1 Crate to open a crate!".format(ctx.prefix), inline=False)
			embed.add_field(name="how to get.", value="You can get keys by fighting monsters.\n By daily's in and voting".format(ctx.prefix), inline=False)
			embed.add_field(name="Stats", value="Fighting monsters = 6.25% chance of getting a key\nDaily will get you 3 to 5 keys.\nVoting will get you 3 to 5 Keys.".format(ctx.prefix), inline=False)
			embed.set_footer(text="Donaters and subscribers get more.")
			await ctx.send(embed=embed)

		elif topic == "Crate" or topic == "crate" or topic == "Crates" or topic == "crates":
			embed=discord.Embed(title="**Crate**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/639425690072252426.png?v=1")
			embed.add_field(name="Usage", value="You need 1 Key and 1 Crate to open a crate!".format(ctx.prefix), inline=False)
			embed.add_field(name="how to get.", value="You can get Crates by fighting monsters.\n By daily's in and voting".format(ctx.prefix), inline=False)
			embed.add_field(name="Stats", value="Fighting monsters = 6.25% chance of getting a crate\nDaily will get you 3 to 5 crates.\nVoting will get you 3 to 5 crates.".format(ctx.prefix), inline=False)
			embed.set_footer(text="Donaters and subscribers get more.")
			await ctx.send(embed=embed)

		elif topic == "Gold" or topic == "gold":
			embed=discord.Embed(title="**Gold**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/639484869809930251.png?v=1")
			embed.add_field(name="Usage", value="Gold is used for a lot of things\n Health potions, Market, When u die  you pay a certain amount, Donating to the guild, The shop, Soon more!".format(ctx.prefix), inline=False)
			embed.add_field(name="how to get.", value="You can get Gold by fighting monsters.\n By daily's in and voting and market\nYou can also get it with selling resources \n{}sell <wood/stone/metal> <amount>\nAnd by Fishing but you can also loose gold..".format(ctx.prefix), inline=False)
			embed.set_footer(text="Donaters and subscribers get more.")
			await ctx.send(embed=embed)
			
		elif topic == "Market" or topic == "market" or topic == "Buy" or topic == "buy"or topic == "Sell" or topic == "sell" or topic == "market buy" or topic == "market sell"or topic == "Market Buy" or topic == "Market Sell":
			embed=discord.Embed(title="**Market**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/560809141766193152.png?v=1")
			embed.add_field(name="Usage", value="Type {}market For the market list.\n Type {}market sell <number (item number in inventory)> <Price>\n To buy type {}market buy <id listed>".format(ctx.prefix, ctx.prefix, ctx.prefix), inline=False)
			embed.add_field(name="Emotes And Price limits", value="<:Basic:641362343338442762> = Basic,     `1.000` - `5.000`\n<:Uncommon:641361853817159685> = Common,     `1.000` - `10.000`\n<:Rare:573784880815538186> = Rare,     `5.000` - `50.000`\n<:Legendary:639425368167809065> = Legendary,     `10.000` - `500.000`\n<:Mythical:573784881386225694> = Mythical,      `500.000`+".format(ctx.prefix), inline=False)
			embed.add_field(name="Rules", value="Only 1 item per users can be sold on the market.\nIf you try to sell 2 the first item will be removed.".format(ctx.prefix), inline=False)
			embed.set_footer(text="Donaters and subscribers get more. Also easy way to clean ur inventory :D")
			await ctx.send(embed=embed)

		elif topic == "Rachi" or topic == "rachi":
			embed=discord.Embed(title="**Rachi**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Golden Temple", inline=False)
			embed.add_field(name="**Health**", value="10Hp - 30Hp", inline=False)
			embed.add_field(name="**Damage**", value="2Dmg - 10Dmg", inline=False)
			embed.add_field(name="**Gold**", value="10G - 15G", inline=False)
			embed.add_field(name="**Experience**", value="5Exp - 20Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Debin" or topic == "debin":
			embed=discord.Embed(title="**Debin**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Golden Temple", inline=False)
			embed.add_field(name="**Health**", value="20Hp - 40Hp", inline=False)
			embed.add_field(name="**Damage**", value="5Dmg - 10Dmg", inline=False)
			embed.add_field(name="**Gold**", value="15G - 20G", inline=False)
			embed.add_field(name="**Experience**", value="10Exp - 25Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Oofer" or topic == "oofer":
			embed=discord.Embed(title="**Oofer**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Golden Temple", inline=False)
			embed.add_field(name="**Health**", value="40Hp - 60Hp", inline=False)
			embed.add_field(name="**Damage**", value="5Dmg - 15Dmg", inline=False)
			embed.add_field(name="**Gold**", value="20G - 25G", inline=False)
			embed.add_field(name="**Experience**", value="15Exp - 25Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Wyvern" or topic == "wyvern":
			embed=discord.Embed(title="**Wyvern**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Golden Temple", inline=False)
			embed.add_field(name="**Health**", value="30Hp - 50Hp", inline=False)
			embed.add_field(name="**Damage**", value="5Dmg - 15Dmg", inline=False)
			embed.add_field(name="**Gold**", value="20G - 25G", inline=False)
			embed.add_field(name="**Experience**", value="15Exp - 25Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Wolf" or topic == "wolf":
			embed=discord.Embed(title="**Wolf**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="The Forest", inline=False)
			embed.add_field(name="**Health**", value="50Hp - 70Hp", inline=False)
			embed.add_field(name="**Damage**", value="10Dmg - 15Dmg", inline=False)
			embed.add_field(name="**Gold**", value="20G - 30G", inline=False)
			embed.add_field(name="**Experience**", value="15Exp - 30Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Goblin" or topic == "goblin":
			embed=discord.Embed(title="**Goblin**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="The Forest", inline=False)
			embed.add_field(name="**Health**", value="50Hp - 70Hp", inline=False)
			embed.add_field(name="**Damage**", value="10Dmg - 20Dmg", inline=False)
			embed.add_field(name="**Gold**", value="25G - 35G", inline=False)
			embed.add_field(name="**Experience**", value="20Exp - 35Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Zombie" or topic == "zombie":
			embed=discord.Embed(title="**Zombie**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="The Forest", inline=False)
			embed.add_field(name="**Health**", value="60Hp - 80Hp", inline=False)
			embed.add_field(name="**Damage**", value="15Dmg - 20Dmg", inline=False)
			embed.add_field(name="**Gold**", value="25G - 40G", inline=False)
			embed.add_field(name="**Experience**", value="25Exp - 35Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Draugr" or topic == "draugr":
			embed=discord.Embed(title="**Draugr**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Saker Keep", inline=False)
			embed.add_field(name="**Health**", value="10Hp - 30Hp", inline=False)
			embed.add_field(name="**Damage**", value="2Dmg - 10Dmg", inline=False)
			embed.add_field(name="**Gold**", value="10G - 15G", inline=False)
			embed.add_field(name="**Experience**", value="7Exp - 20Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Stalker" or topic == "stalker":
			embed=discord.Embed(title="**Stalker**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Saker Keep", inline=False)
			embed.add_field(name="**Health**", value="20Hp - 40Hp", inline=False)
			embed.add_field(name="**Damage**", value="5Dmg - 10Dmg", inline=False)
			embed.add_field(name="**Gold**", value="15G - 20G", inline=False)
			embed.add_field(name="**Experience**", value="10Exp - 25Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Souleater" or topic == "souleater":
			embed=discord.Embed(title="**Souleater**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Saker Keep", inline=False)
			embed.add_field(name="**Health**", value="40Hp - 60Hp", inline=False)
			embed.add_field(name="**Damage**", value="5Dmg - 15Dmg", inline=False)
			embed.add_field(name="**Gold**", value="20G - 25G", inline=False)
			embed.add_field(name="**Experience**", value="15Exp - 25Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Elder Dragon" or topic == "elder dragon":
			embed=discord.Embed(title="**Souleater**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Ebony Mountains", inline=False)
			embed.add_field(name="**Health**", value="70Hp - 90Hp", inline=False)
			embed.add_field(name="**Damage**", value="20Dmg - 30Dmg", inline=False)
			embed.add_field(name="**Gold**", value="35G - 55G", inline=False)
			embed.add_field(name="**Experience**", value="35Exp - 45Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Hades" or topic == "hades":
			embed=discord.Embed(title="**Hades**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Ebony Mountains", inline=False)
			embed.add_field(name="**Health**", value="80Hp - 100Hp", inline=False)
			embed.add_field(name="**Damage**", value="20Dmg - 30Dmg", inline=False)
			embed.add_field(name="**Gold**", value="35G - 55G", inline=False)
			embed.add_field(name="**Experience**", value="35Exp - 45Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Ebony Guardian" or topic == "ebony guardian":
			embed=discord.Embed(title="**Ebony Guardian**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Ebony Mountains", inline=False)
			embed.add_field(name="**Health**", value="80Hp - 100Hp", inline=False)
			embed.add_field(name="**Damage**", value="20Dmg - 30Dmg", inline=False)
			embed.add_field(name="**Gold**", value="35G  - 55G", inline=False)
			embed.add_field(name="**Experience**", value="35Exp - 45Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Harpy" or topic == "harpy":
			embed=discord.Embed(title="**Harpy**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Ebony Mountains", inline=False)
			embed.add_field(name="**Health**", value="80Hp - 100Hp", inline=False)
			embed.add_field(name="**Damage**", value="20Dmg - 40Dmg", inline=False)
			embed.add_field(name="**Gold**", value="40G - 55G", inline=False)
			embed.add_field(name="**Experience**", value="35Exp - 55Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
						
		elif topic == "Dormammu" or topic == "dormammu":
			embed=discord.Embed(title="**Dormammu**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Township of Arkina", inline=False)
			embed.add_field(name="**Health**", value="90Hp - 110Hp", inline=False)
			embed.add_field(name="**Damage**", value="20Dmg - 40Dmg", inline=False)
			embed.add_field(name="**Gold**", value="40G - 55G", inline=False)
			embed.add_field(name="**Experience**", value="35Exp - 45Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Ettin" or topic == "ettin":
			embed=discord.Embed(title="**Ettin**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Township of Arkina", inline=False)
			embed.add_field(name="**Health**", value="90Hp - 110Hp", inline=False)
			embed.add_field(name="**Damage**", value="20Dmg - 40Dmg", inline=False)
			embed.add_field(name="**Gold**", value="40G - 55G", inline=False)
			embed.add_field(name="**Experience**", value="35Exp - 45Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)	
			
		elif topic == "Largos" or topic == "largos":
			embed=discord.Embed(title="**Largos**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Zulanthu", inline=False)
			embed.add_field(name="**Health**", value="100Hp - 120Hp", inline=False)
			embed.add_field(name="**Damage**", value="25Dmg - 50Dmg", inline=False)
			embed.add_field(name="**Gold**", value="45G - 65G", inline=False)
			embed.add_field(name="**Experience**", value="40Exp - 55Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Deathclaw" or topic == "deathclaw":
			embed=discord.Embed(title="**Deathclaw**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Zulanthu", inline=False)
			embed.add_field(name="**Health**", value="100Hp - 120Hp", inline=False)
			embed.add_field(name="**Damage**", value="25Dmg - 40Dmg", inline=False)
			embed.add_field(name="**Gold**", value="45G - 60G", inline=False)
			embed.add_field(name="**Experience**", value="40Exp - 60Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Saurian" or topic == "saurian":
			embed=discord.Embed(title="**Saurian**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Zulanthu", inline=False)
			embed.add_field(name="**Health**", value="110Hp - 130Hp", inline=False)
			embed.add_field(name="**Damage**", value="45Dmg - 60Dmg", inline=False)
			embed.add_field(name="**Gold**", value="28G  - 31G", inline=False)
			embed.add_field(name="**Experience**", value="40Exp - 50Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Skeleton" or topic == "skeleton":
			embed=discord.Embed(title="**Skeleton**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Lost city", inline=False)
			embed.add_field(name="**Health**", value="90Hp - 110Hp", inline=False)
			embed.add_field(name="**Damage**", value="20Dmg - 30Dmg", inline=False)
			embed.add_field(name="**Gold**", value="35G - 55G", inline=False)
			embed.add_field(name="**Experience**", value="35Exp - 45Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Lizardmen" or topic == "lizardmen":
			embed=discord.Embed(title="**Lizardmen**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Lost City", inline=False)
			embed.add_field(name="**Health**", value="100Hp - 120Hp", inline=False)
			embed.add_field(name="**Damage**", value="25Dmg - 40Dmg", inline=False)
			embed.add_field(name="**Gold**", value="45G  - 60G", inline=False)
			embed.add_field(name="**Experience**", value="40Exp - 50Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Giant" or topic == "giant":
			embed=discord.Embed(title="**Giant**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Lost City", inline=False)
			embed.add_field(name="**Health**", value="110Hp - 130Hp", inline=False)
			embed.add_field(name="**Damage**", value="25Dmg - 50Dmg", inline=False)
			embed.add_field(name="**Gold**", value="45G - 65G", inline=False)
			embed.add_field(name="**Experience**", value="40Exp - 55Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Ice Wolves" or topic == "ice wolves":
			embed=discord.Embed(title="**Ice Wolves**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Drenheim", inline=False)
			embed.add_field(name="**Health**", value="110Hp - 130Hp", inline=False)
			embed.add_field(name="**Damage**", value="25Dmg - 50Dmg", inline=False)
			embed.add_field(name="**Gold**", value="45G - 65G", inline=False)
			embed.add_field(name="**Experience**", value="40Exp - 55Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Frost Orc" or topic == "frost orc":
			embed=discord.Embed(title="**frost Orc**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Drenheim", inline=False)
			embed.add_field(name="**Health**", value="120Hp - 140Hp", inline=False)
			embed.add_field(name="**Damage**", value="30Dmg - 55Dmg", inline=False)
			embed.add_field(name="**Gold**", value="50G - 65G", inline=False)
			embed.add_field(name="**Experience**", value="45Exp - 60Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Frost Goblin" or topic == "frost goblin":
			embed=discord.Embed(title="**frost Goblin**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="")
			embed.add_field(name="**Type**", value="Monster", inline=False)
			embed.add_field(name="**Place**", value="Drenheim", inline=False)
			embed.add_field(name="**Health**", value="120Hp - 140Hp", inline=False)
			embed.add_field(name="**Damage**", value="30Dmg - 55Dmg", inline=False)
			embed.add_field(name="**Gold**", value="50G - 65G", inline=False)
			embed.add_field(name="**Experience**", value="45Exp - 60Exp", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)


		
		elif topic == "Orc" or topic == "orc":
			embed=discord.Embed(title="**Orc**", description="**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/639474558109483028.png?v=1")
			embed.add_field(name="**Type**", value="Character Race", inline=False)
			embed.add_field(name="**Traits**", value="None yet!", inline=False)
			embed.add_field(name="**Backstory**", value="To the far west of Solyx, deep into the cold and dangerous mountain ranges, lies the kingdom of the orc. This grand and heavily fortified city is home to the orcs. To survive the cold and harsh lands they live in, the orcs have to go through hellish training, starting from the day they can walk. Once they become of age, these fierce creatures will have been shaped up to be the pinnacle of raw physical strength, and combat prowess.", inline=False)
			embed.set_footer(text="Submitted by Rideric#4935\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Human" or topic == "human":
			embed=discord.Embed(title="**Human**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/639474561355874304.png?v=1")
			embed.add_field(name="**Type**", value="Character Race", inline=False)
			embed.add_field(name="**Traits**", value="None yet!", inline=False)
			embed.add_field(name="**Backstory**", value="None yet!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "elf" or topic == "Elf":
			embed=discord.Embed(title="**Elf**", description="**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/639474564023189554.png?v=1")
			embed.add_field(name="**Type**", value="Character Race", inline=False)
			embed.add_field(name="**Traits**", value="None yet!", inline=False)
			embed.add_field(name="**Backstory**", value="In the lush forested areas of east Solyx, the elves thrive. While their bodies are naturally slim, they are surprisingly strong and can easily hold their own in a fight. However, elves do not prioritize physical strength; instead favoring the charismatic members of society. While many things can be seen as status symbols to individual elf communities, the pointiness of their ears is the most common way an elf shows off their looks.", inline=False)
			embed.set_footer(text="Submitted by (8ᘌꇤ⁐ꃳ 三#2369\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Demon" or topic == "demon":
			embed=discord.Embed(title="**Demon**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/639474562463170590.png?v=1")
			embed.add_field(name="**Type**", value="Character Race", inline=False)
			embed.add_field(name="**Traits**", value="None yet!", inline=False)
			embed.add_field(name="**Backstory**", value="Noneyet!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Users" or topic == "users":
			embed=discord.Embed(title="**Ranking users**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=user.avatar_url)
			embed.add_field(name="**Stats**", value="to show detailed info type {}stats or {}status".format(ctx.prefix, ctx.prefix), inline=False)
			embed.add_field(name="**Profile**", value="To show basic info and profile type {}profile ".format(ctx.prefix), inline=False)
			embed.add_field(name="**Rank**", value="To check level progression and rank type {}rank".format(ctx.prefix), inline=False)
			embed.add_field(name="**Global Rank**", value="To check global level rank type {}top users".format(ctx.prefix), inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
	
		elif topic == "Guilds" or topic == "guilds":
			embed=discord.Embed(title="**Ranking Guilds**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="**Stats**", value="to show detailed info type {}guild info".format(ctx.prefix), inline=False)
			embed.add_field(name="**Global Rank**", value="To check global guild rank type {}top guilds".format(ctx.prefix), inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
		
		elif topic == "Swing" or topic == "swing":
			embed=discord.Embed(title="**Swing skill**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="**For**", value="Knight, samurai, Paladin", inline=False)
			embed.add_field(name="**Skill**", value="The wielder brings the weapon up to just about shoulder height and swings it down with immense strength onto it's foe", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Stab" or topic == "stab":
			embed=discord.Embed(title="**Stab skill**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="**For**", value="None", inline=False)
			embed.add_field(name="**Skill**", value="None", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Shoot" or topic == "shoot":	
			embed=discord.Embed(title="**Shoot skill**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="**For**", value="None", inline=False)
			embed.add_field(name="**Skill**", value="None", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Cast" or topic == "cast":
			embed=discord.Embed(title="**Cast skill**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="**For**", value="None", inline=False)
			embed.add_field(name="**Skill**", value="None", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Parry" or topic == "parry":
			embed=discord.Embed(title="**Parry skill**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="**For**", value="None", inline=False)
			embed.add_field(name="**Skill**", value="None", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Distort" or topic == "distort":
			embed=discord.Embed(title="**Distort skill**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="**For**", value="None", inline=False)
			embed.add_field(name="**Skill**", value="None", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Reap" or topic == "reap":
			embed=discord.Embed(title="**Reap skill**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="**For**", value="None", inline=False)
			embed.add_field(name="**Skill**", value="None", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Overload" or topic == "overload":
			embed=discord.Embed(title="**Overload skill**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="**For**", value="None", inline=False)
			embed.add_field(name="**Skill**", value="None", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Fusillade" or topic == "fusillade":
			embed=discord.Embed(title="**Fusillade skill**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="**For**", value="None", inline=False)
			embed.add_field(name="**Skill**", value="None", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Protude" or topic == "protude":
			embed=discord.Embed(title="**Protude skill**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="**For**", value="None", inline=False)
			embed.add_field(name="**Skill**", value="None", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Strike" or topic == "strike":
			embed=discord.Embed(title="**Strike skill**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="**For**", value="None", inline=False)
			embed.add_field(name="**Skill**", value="None", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Corrupt" or topic == "corrupt":
			embed=discord.Embed(title="**Corrupt skill**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="**For**", value="None", inline=False)
			embed.add_field(name="**Skill**", value="None", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Titles Guilds" or topic == "titles guilds":
			embed=discord.Embed(title="**Titles Guilds**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="**Titles**", value="1. Big Boys\n2. Achievers\n3. Real Deal".format(ctx.prefix), inline=False)
			embed.add_field(name="**How to obtain**", value="The guild titles refer to a guild level.\nLevel 1 = Big boys\nLevel 2 = Achievers\nLevel 3 = Real Deal".format(ctx.prefix), inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Titles Users" or topic == "titles users":
			embed=discord.Embed(title="**Titles Users**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=user.avatar_url)
			embed.add_field(name="**How to obtain**", value="The Users titles Can be obtained by random actions or achievements.".format(ctx.prefix), inline=False)
			embed.add_field(name="**Titles**", value="Level titles.\nAchievement titles".format(ctx.prefix), inline=False)
			embed.add_field(name="Level titles", value="{}wiki Level titles".format(ctx.prefix), inline=False)
			embed.add_field(name="Achievement titles", value="{}wiki achievement titles".format(ctx.prefix), inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "achievement titles" or topic == "Achievement Titles":
			embed=discord.Embed(title="**Achievement Titles**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=user.avatar_url)
			embed.add_field(name="Achievement titles", value="1. Legendary - obtained at first legendary item.\n2. Twice Told Legend - obtained at second legendary item.\n3. Uncoordinated - Get 15 deaths...\n4. Unhandy - Get 30 deaths...\n5 Clumsy - Get 60 deaths...\n6. Unskillful - Get 90 deaths...\n7. Inexpert - Get 120 deaths...\n8. I'm playing the game wrong... - ???\n9. Broke - Have 0 gold!\n10. Poor - have 500+ gold.\n11. Rich - have 10.000+ gold.\n12. Wealthy - Have 100.000+ gold.\n12. Millionaire - Have 1.000.000+ gold!".format(ctx.prefix), inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Monster Titles" or topic == "monster titles ":
			embed=discord.Embed(title="**Monster Titles 1**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=user.avatar_url)
			embed.add_field(name="Monster titles", value="1. Rachi Killer - Kill 100 Rachi's\n2. Draugr Killer - Kill 100 Draugr's\n3. Debin Killer - Kill 100 Debin's\n4. Stalker Killer - Kill 100 Stalker's\n5. Fire Golem Killer - Kill 100 Fire Golem's\n6. Wyvern Killer - Kill 100 Wyvern's\n7. Oofer Killer - Kill 100  Oofer's\n8. Souleater Killer - Kill 100  Souleater's\n9. Wolf Killer - Kill 100 Wolf's\n10. Goblin Killer - Kill 100  Goblin's\n11. Zombie Killer - Kill 100  Zombie's\n12. Phantasm Killer - Kill 100 Phantasm's\n13. The Corrupted Killer - Kill 100 Corrupted\n14. The Accursed Killer - Kill 100 Accursed\n15. Elder Dragon Killer - Kill 100 Elder Dragon's\n16. Hades Killer - Kill 100 Hades\n17. Harpy Killer - Kill 100  Harpy's\n18. Dormammu Killer - Kill 100 Dormammu's\n19. Ettin Killer - Kill 100 Ettin's\n20. The Nameless King Killer - Kill 100 Nameless Kings ".format(ctx.prefix), inline=False)
			embed.set_footer(text="Type -wiki monster titles 2 for page 2\nSubmitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Monster titles 2" or topic == "monster titles 2":
			embed=discord.Embed(title="**Monster Titles 2**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=user.avatar_url)
			embed.add_field(name="Monster titles", value="21. Largos Killer - Kill 100 Largo's\n22. Saurian Killer - Kill 100 Saurian's\n23. The Venomous Killer - Kill 100 Venomous\n24. Ebony Guardian Killer - Kill 100  Ebony Guardians\n25. Skeleton Killer - kill 100 Skeletons\n26. Lizardmen Killer - Kill 100 Lizardmen\n27. Giant Killer - Kill 100 Giants\n28. Death Knight Killer - Kill 100 Death Knights\n29. Ice Wolves Killer - kill 100 Ice Wolves\n30. Frost Orc Killer - kill 100 Frost Orcs\n31. Frost Goblin Killer - Kill 100 Frost Goblins\32. Frost Dragon Killer - Kill 100 Frost Dragons".format(ctx.prefix), inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "level titles" or topic == "Level Titles":
			embed=discord.Embed(title="**Level Titles**", description="<:ShieldCheck:560804135545602078>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url=user.avatar_url)
			embed.add_field(name="Level titles", value="Beginner - Level 10\nAmateur - Level 20\nNovice - Level 30\nApprentice - Level 40\nRespected - Level 50\nRenowned - Level 75\nProfessional - Level 100\nMaster - Level 125\nGrand-Master - Level 150\nEnlightened - Level 200\nMighty - Level 250\nEmpowered - Level 300\nGolden - Level 350\nRadiant - Level 400\nArcane - Level 450\nIridescent - Level 500\nLuminescent - Level 600\nCelestial - Level 700\nunbelievable - Level 800\nUnreal - Level 900\nGodlike - Level 1000".format(ctx.prefix), inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Golden Temple" or topic == "golden temple":
			embed=discord.Embed(title="**Golden Temple**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="https://i.imgur.com/6u83Sy9.jpg")
			embed.add_field(name="**Monsters**", value="Rachi, Debin, Oofer, Wyvern", inline=False)
			embed.add_field(name="**Boss**", value="Fire Golem", inline=False)
			embed.add_field(name="**Unlock**", value="Level 0", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Saker Keep" or topic == "saker keep":
			embed=discord.Embed(title="**Saker Keep**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="https://i.imgur.com/xyrgOth.jpg")
			embed.add_field(name="**Monsters**", value="Draugr, Stalker, Souleater",inline=False)
			embed.add_field(name="**Boss**", value="The Corrupted", inline=False)
			embed.add_field(name="**Unlock**", value="Level 5", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "The Forest" or topic == "the forest":
			embed=discord.Embed(title="**The Forest**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="https://i.imgur.com/FAHXOLl.jpg")
			embed.add_field(name="**Monsters**", value="Wolf, Goblin, Zombie",inline=False)
			embed.add_field(name="**Boss**", value="Phantasm", inline=False)
			embed.add_field(name="**Unlock**", value="Level 10", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Ebony Mountains" or topic == "ebony mountains":
			embed=discord.Embed(title="**Ebony Mountains**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="https://i.imgur.com/pPd5s9r.jpg")
			embed.add_field(name="**Monsters**", value="Elder Dragon, Hades, Ebony Guardian",inline=False)
			embed.add_field(name="**Boss**", value="The Accursed", inline=False)
			embed.add_field(name="**Unlock**", value="Level 20", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Township of Arkina" or topic == "township of arkina":
			embed=discord.Embed(title="**Township of Arkina**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="https://i.imgur.com/lypzFbu.jpg")
			embed.add_field(name="**Monsters**", value="Harpy, Dormammu, Ettin",inline=False)
			embed.add_field(name="**Boss**", value="The Nameless King", inline=False)
			embed.add_field(name="**Unlock**", value="Level 40", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Zulanthu" or topic == "zulanthu":
			embed=discord.Embed(title="**Zulanthu**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="https://i.imgur.com/GEvABaS.jpg")
			embed.add_field(name="**Monsters**", value="Largos, Deathclaw, Saurian",inline=False)
			embed.add_field(name="**Boss**", value="The Venomous", inline=False)
			embed.add_field(name="**Unlock**", value="Level 60", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Lost City" or topic == "lost city":
			embed=discord.Embed(title="**Lost City**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="https://i.imgur.com/cBo113x.jpg")
			embed.add_field(name="**Monsters**", value="Skeleton, Lizardmen, Giant", inline=False)
			embed.add_field(name="**Boss**", value="Death Knight!", inline=False)
			embed.add_field(name="**Unlock**", value="Level 90", inline=False)
			embed.add_field(name="Back Story", value="There was war raging between humans and dragons and it ended up with humans losing.\nThis place has been forgotten for a century!\nUntil one archaeologist found it during the research of finding an ancient city.", inline=False)
			embed.set_footer(text="Submitted by Khael#6854 \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Drenheim" or topic == "drenheim":
			embed=discord.Embed(title="**Drenheim [Coming Soon]**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="https://i.imgur.com/AVBSEfQ.jpg")
			embed.add_field(name="**Monsters**", value="Ice Wolves, Frost Orc, Frost Goblin", inline=False)
			embed.add_field(name="**Boss**", value="Frost Dragon", inline=False)
			embed.add_field(name="**Unlock**", value="Level 120", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Havelow" or topic == "havelow":
			embed=discord.Embed(title="**Havelow [Coming Soon]**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="https://i.imgur.com/A5pbtEB.jpg")
			embed.add_field(name="**Monsters**", value="Cleared out!", inline=False)
			embed.add_field(name="**Boss**", value="Beaten!", inline=False)
			embed.add_field(name="**Unlock**", value="Level 150", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Sacred Cave" or topic == "sacred cave":
			embed=discord.Embed(title="**Sacred Cave [Coming Soon]**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="https://i.imgur.com/BwKaOW9.jpg")
			embed.add_field(name="**Monsters**", value="Cleared Out!",inline=False)
			embed.add_field(name="**Boss**", value="Beaten!", inline=False)
			embed.add_field(name="**Unlock**", value="Level 200", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "The Haunted Tomb" or topic == "the haunted tomb":
			embed=discord.Embed(title="**The Haunted Tomb [Coming Soon]**", description="<:ShieldBug:649157223905492992>**Wiki**", color=discord.Colour(0xffffff))
			embed.set_image(url="https://i.imgur.com/duqlXae.jpg")
			embed.add_field(name="**Monsters**", value="Cleared Out!",inline=False)
			embed.add_field(name="**Boss**", value="Beaten!", inline=False)
			embed.add_field(name="**Unlock**", value="Level 250", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by \nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "4" or topic =="page 4/4":
			embed=discord.Embed(color=discord.Colour(0xffffff))
			embed.add_field(name="**Wiki topics**", value="Page 4".format(ctx.prefix, ctx.prefix), inline=False)
			embed.add_field(name="<:ShieldCheck:560804135545602078>Weapons", value="Starter Bow, Starter Sword, Starter Staff, Starter Dagger,Iron Claws, Iron Mace, Curved Dagger, Tomb of Water, Spiked Mace, Mithril Sword, Etched Longbow, Verdant Bow, Excalibur, Twilight, Devil's Kiss, Hawkeye, Solarflare, Thunderguard, Doomblade, Deathraze, Soulreaper", inline=True)
			embed.set_footer(text="submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)


		elif topic == "Starter Bow" or topic == "starter bow":
			embed=discord.Embed(title="**Starter Bow**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://i.imgur.com/JSHWiSK.png")
			embed.add_field(name="**Type**", value="Weapon, ", inline=False)
			embed.add_field(name="**For**", value="Archer, Ranger, Assassin", inline=False)
			embed.add_field(name="**Rarity**", value="Basic", inline=False)
			embed.add_field(name="**Damage**", value="5 - 12", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
	
		elif topic == "Starter Sword" or topic == "starter sword":
			embed=discord.Embed(title="**Starter Sword**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://i.imgur.com/oW8roUp.png")
			embed.add_field(name="**Type**", value="Weapon", inline=False)
			embed.add_field(name="**For**", value="Knight, Paladin, Samurai", inline=False)
			embed.add_field(name="**Rarity**", value="Basic", inline=False)
			embed.add_field(name="**Damage**", value="5 - 12", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Starter Staff" or topic == "starter staff":
			embed=discord.Embed(title="**Starter Staff**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://i.imgur.com/S7eGyqy.png")
			embed.add_field(name="**Type**", value="Weapon", inline=False)
			embed.add_field(name="**For**", value="Mage, Elementalist, Necromancer, Mesmer", inline=False)
			embed.add_field(name="**Rarity**", value="Basic", inline=False)
			embed.add_field(name="**Damage**", value="5 - 12", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Starter Dagger" or topic == "starter dagger":
			embed=discord.Embed(title="**Starter Dagger**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://i.imgur.com/WGaqfei.png")
			embed.add_field(name="**Type**", value="Weapon", inline=False)
			embed.add_field(name="**For**", value="Thief, Mesmer, Rogue", inline=False)
			embed.add_field(name="**Rarity**", value="Basic", inline=False)
			embed.add_field(name="**Damage**", value="5 - 12", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Iron Claws" or topic == "iron claws":
			embed=discord.Embed(title="**Iron Claws**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://i.imgur.com/lrk0y5p.png")
			embed.add_field(name="**Type**", value="Weapon", inline=False)
			embed.add_field(name="**For**", value="Thief, Mesmer, Rogue", inline=False)
			embed.add_field(name="**Rarity**", value="Rare", inline=False)
			embed.add_field(name="**Damage**", value="24 - 28", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Iron Mace" or topic == "iron mace":
			embed=discord.Embed(title="**Iron Mace**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://i.imgur.com/eMGSaS5.png")
			embed.add_field(name="**Type**", value="Weapon", inline=False)
			embed.add_field(name="**For**", value="Paladin, Rogue, Samurai", inline=False)
			embed.add_field(name="**Rarity**", value="Rare", inline=False)
			embed.add_field(name="**Damage**", value="20 - 30", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Curved Dagger" or topic == "curved dagger":
			embed=discord.Embed(title="**Curved Dagger**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://i.imgur.com/31mYMgk.png")
			embed.add_field(name="**Type**", value="Weapon", inline=False)
			embed.add_field(name="**For**", value="Thief, Mesmer, Rogue", inline=False)
			embed.add_field(name="**Rarity**", value="Rare", inline=False)
			embed.add_field(name="**Damage**", value="5 - 25", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Tomb of water" or topic == "tomb of water":
			embed=discord.Embed(title="**Tomb of water**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://i.imgur.com/H7Umwgs.png")
			embed.add_field(name="**Type**", value="Weapon", inline=False)
			embed.add_field(name="**For**", value="Mage, Elementalist, Necromancer, Mesmer", inline=False)
			embed.add_field(name="**Rarity**", value="Rare", inline=False)
			embed.add_field(name="**Damage**", value="5 - 25", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Spiked Mace" or topic == "spiked mace":
			embed=discord.Embed(title="**Spiked Mace**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://i.imgur.com/3PZfnkC.png")
			embed.add_field(name="**Type**", value="Weapon", inline=False)
			embed.add_field(name="**For**", value="Paladin, Rogue, Samurai", inline=False)
			embed.add_field(name="**Rarity**", value="Rare", inline=False)
			embed.add_field(name="**Damage**", value="5 - 25", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Mithril Sword" or topic == "mithril sword":
			embed=discord.Embed(title="**Mithril Sword**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://i.imgur.com/UNc4JeO.png")
			embed.add_field(name="**Type**", value="Weapon", inline=False)
			embed.add_field(name="**For**", value="Knight, Paladin, Samurai", inline=False)
			embed.add_field(name="**Rarity**", value="Rare", inline=False)
			embed.add_field(name="**Damage**", value="2 - 25", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)

		elif topic == "Etched Longbow" or topic == "etched longbow":
			embed=discord.Embed(title="**Etched  Longbow**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://i.imgur.com/VvYc9zY.png")
			embed.add_field(name="**Type**", value="Weapon", inline=False)
			embed.add_field(name="**For**", value="Archer, Ranger, Assassin", inline=False)
			embed.add_field(name="**Rarity**", value="Rare", inline=False)
			embed.add_field(name="**Damage**", value="2 - 25", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Verdant Bow" or topic == "verdant bow":
			embed=discord.Embed(title="**Verdant bow**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://i.imgur.com/3EyPeH2.png")
			embed.add_field(name="**Type**", value="Weapon", inline=False)
			embed.add_field(name="**For**", value="Archer, Ranger, Assassin", inline=False)
			embed.add_field(name="**Rarity**", value="Rare", inline=False)
			embed.add_field(name="**Damage**", value="2 - 25", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Excalibur" or topic == "excalibur":
			embed=discord.Embed(title="**Excalibur**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://i.imgur.com/mnQAA1X.png")
			embed.add_field(name="**Type**", value="Weapon", inline=False)
			embed.add_field(name="**For**", value="Knight, Paladin, Samurai", inline=False)
			embed.add_field(name="**Rarity**", value="Legendary", inline=False)
			embed.add_field(name="**Damage**", value="25 - 41", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Twilight" or topic == "twilight":
			embed=discord.Embed(title="**Twilight**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://i.imgur.com/HFH7ugZ.png")
			embed.add_field(name="**Type**", value="Weapon", inline=False)
			embed.add_field(name="**For**", value="Knight, Paladin, Samurai", inline=False)
			embed.add_field(name="**Rarity**", value="Legendary", inline=False)
			embed.add_field(name="**Damage**", value="31 - 40", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Devil's Kiss" or topic == "devil's kiss" or topic == "Devils Kiss" or topic == "devils kiss":
			embed=discord.Embed(title="**Devil's Kiss**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://i.imgur.com/59tnHA8.png")
			embed.add_field(name="**Type**", value="Weapon", inline=False)
			embed.add_field(name="**For**", value="Archer, Ranger, Assassin", inline=False)
			embed.add_field(name="**Rarity**", value="Legendary", inline=False)
			embed.add_field(name="**Damage**", value="25 - 37", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Hawkeye" or topic == "hawkeye":
			embed=discord.Embed(title="**Hawkeye**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://i.imgur.com/dnkLTAj.png")
			embed.add_field(name="**Type**", value="Weapon", inline=False)
			embed.add_field(name="**For**", value="Archer, Ranger, Assassin", inline=False)
			embed.add_field(name="**Rarity**", value="Legendary", inline=False)
			embed.add_field(name="**Damage**", value="32 - 44", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Solarflare" or topic == "solarflare":
			embed=discord.Embed(title="**Solarflare**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://i.imgur.com/ZP2KxJl.png")
			embed.add_field(name="**Type**", value="Weapon", inline=False)
			embed.add_field(name="**For**", value="Mage, Elementalist, Necromancer, Mesmer", inline=False)
			embed.add_field(name="**Rarity**", value="Legendary", inline=False)
			embed.add_field(name="**Damage**", value="27 - 51", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Thunderguard" or topic == "thunderguard":
			embed=discord.Embed(title="**Thunderguard**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://i.imgur.com/XXSZylz.png")
			embed.add_field(name="**Type**", value="Weapon", inline=False)
			embed.add_field(name="**For**", value="Mage, Elementalist, Necromancer, Mesmer", inline=False)
			embed.add_field(name="**Rarity**", value="Legendary", inline=False)
			embed.add_field(name="**Damage**", value="29 - 39", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Doomblade" or topic == "doomblade":
			embed=discord.Embed(title="**Doomblade**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://i.imgur.com/kFHHkyu.png")
			embed.add_field(name="**Type**", value="Weapon", inline=False)
			embed.add_field(name="**For**", value="Thief, Mesmer, Rogue", inline=False)
			embed.add_field(name="**Rarity**", value="Legendary", inline=False)
			embed.add_field(name="**Damage**", value="31 - 48", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Deathraze" or topic == "deathraze":
			embed=discord.Embed(title="**Deathraze**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://i.imgur.com/2jRAyud.png")
			embed.add_field(name="**Type**", value="Weapon", inline=False)
			embed.add_field(name="**For**", value="Thief, Mesmer, Rogue", inline=False)
			embed.add_field(name="**Rarity**", value="Legendary", inline=False)
			embed.add_field(name="**Damage**", value="32 - 52", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)
			
		elif topic == "Soulreaper" or topic == "soulreaper":
			embed=discord.Embed(title="**Soulreaper**", description=":book:**Wiki**", color=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://i.imgur.com/xpmTArc.png")
			embed.add_field(name="**Type**", value="Weapon", inline=False)
			embed.add_field(name="**For**", value="Thief, Mesmer, Rogue", inline=False)
			embed.add_field(name="**Rarity**", value="Legendary", inline=False)
			embed.add_field(name="**Damage**", value="27 - 46", inline=False)
			embed.add_field(name="Back Story", value="Write and submit your own backstory! The best will be featured!", inline=False)
			embed.set_footer(text="Submitted by ...\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.")
			await ctx.send(embed=embed)



		elif topic == "test" or topic == "testing":
			title="<:ShieldBug:649157223905492992>Test123"
			description="**\u27a4 Health** - 1 \n**\u27a4 Damage** - 2 \n**\u27a4 Gold** - 3 \n**\u27a4 Exp** - 4 \n \n  yes sum text blabla big monster RAWR big mad long story \n"
			footer="Submitted by your mom **>:c**\nSubmit your wiki article by sending a dm/message to @TheMaksoo#1212.".format(ctx.prefix)
			icon = ('https://cdn.discordapp.com/attachments/750681506262810624/751520899848601620/unknown.png')

		elif topic == "guild bonus" or topic == "guildbonus":
			title= "<:ShieldBug:649157223905492992>Guild Bonus"
			description="The guild bonus adds a percentage of gold-gain on top of the regular gold income from an enemy kill.\n\nIt works through an equation which we shall not bore you with here. Simply put, the higher the bonus, the higher the chance of more bonus gold.\n\nThe bonus applies to all those who represent the guild\nThe bonus starts at 0 can be increased by donating gold to the guild"
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