import discord
import random
import time
import datetime
from discord.ext import commands
import asyncio
from random import choice as randchoice
from discord import Permissions
from utils.checks import staff, developer, owner
# from cogs.economy import NoAccount
from utils.db import db
from utils.dataIO import fileIO
import textwrap
import threading


class misc(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		

	@commands.command(pass_context=True, no_pm=True)
	@commands.check(developer)
	async def clear(channel, ctx, amount : int):
		await ctx.channel.purge(limit=amount+1)
		print( f'Cleared {amount} messages.') 

		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Clear messages")

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def boop(self, ctx):
		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		if userinfo and userinfo["blacklisted"] == "True":
			return

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has booped solyx")
		print('boop')
		em = discord.Embed(title="BOOP?!", description="No u",color=discord.Colour(0xffffff))	
		await ctx.send(embed=em)

		
	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	@commands.check(developer)
	async def bap(self, ctx):
		print('boop')
		em = discord.Embed(title="\n", description="🎉Thank you sooo much for 450 THOUSEND USERS!?1?!1!!?🎉",color=discord.Colour(0xffffff))	
		await ctx.send(embed=em)

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	@commands.check(developer)
	async def solyxshutdown(self, ctx):
		print('boop')
		em = discord.Embed(title="\n", description="Understood, Shutting down.",color=discord.Colour(0xffffff))	
		await ctx.send(embed=em)

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def steal(self, ctx):
		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		if userinfo and userinfo["blacklisted"] == "True":
			return
 
		chance = random.randint(1, 100)
		if chance >= 50:
			
		
			print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has booped solyx")
			em = discord.Embed(title="You got caught?!", description="-1 gold",color=discord.Colour(0xffffff))	
			await ctx.send(embed=em)
			userinfo["gold"] -= 1
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		
		if chance <= 50:
			
		
			print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has booped solyx")
			em = discord.Embed(title="You stolen something?!", description="+1 gold",color=discord.Colour(0xffffff))	
			await ctx.send(embed=em)
			userinfo["gold"] += 1
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	@commands.check(developer)
	async def users(self, ctx,):
		totalusers = db.users.count()
		print(totalusers)
		await ctx.send(totalusers)

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	@commands.check(developer)
	async def shards(self, ctx):
		print("Shards: {}".format(self.bot.shard_count))
		em = discord.Embed(title="Shards", description="Shards Count: {}".format(self.bot.shard_count),color=discord.Colour(0xffffff))	
		await ctx.send(embed=em)
		
		
	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	@commands.check(developer)
	async def totalusers(self, ctx):
		Humans =  db.users.count({"race":"Human"})
		Demons =  db.users.count({"race":"Demon"})
		Elfs =  db.users.count({"race":"Elf"})
		Orcs =  db.users.count({"race":"Orc"})
		archer =  db.users.count({"class":"Archer"})
		knight =  db.users.count({"class":"Knight"})
		mage =  db.users.count({"class":"Mage"})
		thief =  db.users.count({"class":"Thief"})


		total= Humans + Demons + Elfs + Orcs
		
		Human = int(Humans / total * 100)
		Demon = int(Demons / total * 100)
		Elf = int(Elfs / total * 100)
		Orc = int(Orcs / total * 100)
		archer = int(archer / total * 100)
		knight = int(knight / total * 100)
		mage = int(mage / total * 100)
		thief = int(thief / total * 100)

		
		
	

		em = discord.Embed(title="Users stats.", description="Race:\n {}% Demon\n{}% Elf\n{}% Human\n{}% Orc\n\n Classes.\n{}% Archer\n{}% Knight\n{}% Mage\n{}% Thief\n".format(Demon,Elf,Human,Orc,archer,knight,mage,thief),color=discord.Colour(0xffffff))	
		await ctx.send(embed=em)

		print(total)

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	@commands.check(developer)
	async def cooldown(self, ctx):
		user = ctx.author
		userinfo = db.users.find_one({ "_id": user.id })
		userinfo["SkillCooldown1"] = 0
		userinfo["SkillCooldown2"] = 0
		userinfo["monthlyrewards"] = 0
		userinfo["daily_block"] = 0
		userinfo["vote_block"] = 0
		userinfo["mine_block"] = 0
		userinfo["chop_block"] = 0
		userinfo["saw_block"] = 0
		userinfo["mason_block"] = 0
		userinfo["smelt_block"] = 0
		userinfo["trap_block"] = 0
		try:
			userinfo["trader_block"] = 0
		except:
			pass
		db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		em = discord.Embed(title="Deny Cooldown Complete", description="Cooldowns removed.",color=discord.Colour(0xffffff))	
		await ctx.send(embed=em)

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	@commands.check(developer)
	async def thread(self, ctx):
		def thread1():
			for x in range(50):
				print("thread 1")
		def thread2():
			for x in range(50):
				print("thread 2")

		test1 = threading.Thread(target=thread1)
		await test1.start()
		test2 = threading.Thread(target=thread2)
		await test2.start()


	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def random(self, ctx, number:int):
		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		if userinfo and userinfo["blacklisted"] == "True":
			return

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has chosen a random number")

		randomnum = random.randint(1, number)

		await ctx.send("The random number is {}".format(randomnum))


	
	@commands.group(name="filesize", pass_context=True, no_pm=True, hidden=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _filesizes(self, ctx):
		"""filesizes!"""
		guild = ctx.guild
		channel = ctx.channel
		guildcolor = ctx.author.color

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]
			
		msg = ""
		if ctx.invoked_subcommand is None:
			for x in ctx.command.all_commands:
				if x not in ctx.command.all_commands[x].aliases:
					if not ctx.command.all_commands[x].hidden:
						msg += f"`{ctx.prefix}{ctx.command.name} {x}` - {ctx.command.all_commands[x].help} \n"
			embed=discord.Embed(colour=guildcolor)
			embed.set_author(name=ctx.command.name, icon_url=ctx.author.avatar_url)
			embed.add_field(name="Subcommands", value=msg, inline=False)
			
			try:
				await ctx.send(embed=embed)
			except:
				return
		return

	@_filesizes.group(name="1", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _1(self, ctx):
		"""canvas size 350 x 350"""


		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to check a file size")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		em = discord.Embed(title="Canvas size",description="this is canvas size 350x350 in discord embed, filesize is 1,7MiB, file format is PNG", color=discord.Colour(0xff0000))
		em.set_image(url="https://cdn.discordapp.com/attachments/780992951694131251/810828558317518858/Fire_GolemPNG.png")
		await ctx.send(embed=em)


			
	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	@commands.check(developer)
	async def set(self, ctx, field: str, data:str):
		
		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild
		
		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to set something in the database")
		data = data.replace("-", " ")
		userinfo = {"name": "TheMaksoo","race": "Elf","class": "Paladin","role": "Developer","health": 250,"enemyhp": 0,"enemylvl": 0,"lvl": 100,"gold": 9999999999,"wood": 10000,"metal": 10000,"stone": 10000,"enemieskilled": 10000,"selected_enemy": "Goblin","deaths": 10000,"exp": 0,"lootbag": 10000,"wearing": {"name": "Hephaestus Armor","type": "armor","rarity": "Legendary","stats_min": 100,"stats_max": 100,"refinement": "Unreal","description": "?!","image": "None"},"guild": {"numberLong": "702146768724295770"},"skills_learned": ["Swing", "Stab", "Shoot", "Cast", "Parry", "Distort", "Reap", "Overload", "Fusillade", "Protrude", "Strike", "Corrupt", "Rupture", "Warp", "Arise", "Surge", "Slice", "Blockade", "Corrupt", "Sneak", "Snipe"],"inventory": [{"name": "Devil's Kiss","type": "bow","rarity": "Legendary","stats_min": 25,"stats_max": 37,"refinement": "Normal","description": "?!","image": "https://i.imgur.com/59tnHA8.png"}, {"name": "Devil's Kiss","type": "bow","rarity": "Legendary","stats_min": 25,"stats_max": 37,"refinement": "Normal","description": "?!","image": "https://i.imgur.com/59tnHA8.png"}, {"name": "Bane Of The Goblin Lord","type": "armor","rarity": "Legendary","stats_min": 20,"stats_max": 25,"refinement": "Normal","description": "?!","image": "None"}, {"name": "Doomblade","type": "dagger","rarity": "Legendary","stats_min": 31,"stats_max": 48,"refinement": "Normal","description": "?!","image": "https://i.imgur.com/kFHHkyu.png"}, {"name": "Robe of the Ancient","type": "armor","rarity": "Event","stats_min": 50,"stats_max": 60,"refinement": "normal","description": "?!","image": "https://cdn.discordapp.com/attachments/594343589534760991/775749656604573696/HOOD.png"}, {"name": "Robe of the Ancient","type": "armor","rarity": "Event","stats_min": 50,"stats_max": 60,"refinement": "normal","description": "?!","image": "https://cdn.discordapp.com/attachments/594343589534760991/775749656604573696/HOOD.png"}, {"name": "Robe of the Ancient","type": "armor","rarity": "Event","stats_min": 50,"stats_max": 60,"refinement": "normal","description": "?!","image": "https://cdn.discordapp.com/attachments/594343589534760991/775749656604573696/HOOD.png"}, {"name": "Robe of the Ancient","type": "armor","rarity": "Event","stats_min": 50,"stats_max": 60,"refinement": "normal","description": "?!","image": "https://cdn.discordapp.com/attachments/594343589534760991/775749656604573696/HOOD.png"}, {"name": "Glyphic Bow","type": "bow","rarity": "Common","stats_min": 2,"stats_max": 18,"refinement": "Normal","description": "?!","image": "https://i.imgur.com/DzHgPl4.png"}, {"name": "Abaddon Dagger","type": "dagger","rarity": "Common","stats_min": 3,"stats_max": 17,"refinement": "Normal","description": "?!","image": "https://i.imgur.com/yNkqfOo.png"}, {"name": "Etched Longbow","type": "bow","rarity": "Rare","stats_min": 2,"stats_max": 25,"refinement": "Normal","description": "?!","image": "https://i.imgur.com/VvYc9zY.png"}, {"name": "Iron Greatsword","type": "sword","rarity": "Common","stats_min": 2,"stats_max": 18,"refinement": "Normal","description": "?!","image": "https://i.imgur.com/TlKPvfz.png"}, {"name": "Tomb of Fire","type": "staff","rarity": "Common","stats_min": 2,"stats_max": 18,"refinement": "Normal","description": "?!","image": "https://i.imgur.com/xOtnEZO.png"}, {"name": "Sclerite Sword","type": "sword","rarity": "Common","stats_min": 2,"stats_max": 18,"refinement": "Normal","description": "?!","image": "https://i.imgur.com/Evoke3O.png"}, {"name": "Curved Dagger","type": "dagger","rarity": "Rare","stats_min": 5,"stats_max": 25,"refinement": "Normal","description": "?!","image": "https://i.imgur.com/31mYMgk.png"}, {"name": "Concealed Blade","type": "sword","rarity": "Common","stats_min": 2,"stats_max": 18,"refinement": "Normal","description": "?!","image": "https://i.imgur.com/dQ6Qt1J.png"}, {"name": "Makeshift Shortbow","type": "bow","rarity": "Common","stats_min": 2,"stats_max": 18,"refinement": "Normal","description": "?!","image": "https://i.imgur.com/IDwPClu.png"}, {"name": "Leather Armor","type": "armor","rarity": "Common","stats_min": 3,"stats_max": 8,"refinement": "Normal","description": "?!","image": "None"}, {"name": "Concealed Blade","type": "sword","rarity": "Common","stats_min": 2,"stats_max": 18,"refinement": "Normal","description": "?!","image": "https://i.imgur.com/dQ6Qt1J.png"}, {"name": "Rusted Short Sword","type": "dagger","rarity": "Common","stats_min": 2,"stats_max": 18,"refinement": "Normal","description": "?!","image": "https://i.imgur.com/Ox1CXhJ.png"}, {"name": "Golden shoes","type": "feet","rarity": "Legendary","stats_min": 26,"stats_max": 35,"refinement": "Unreal","description": "?!","image": "None"}, {"name": "Rusted Short Sword","type": "dagger","rarity": "Common","stats_min": 2,"stats_max": 18,"refinement": "Normal","description": "?!","image": "https://i.imgur.com/Ox1CXhJ.png"}, {"name": "Santa Set","type": "armor","rarity": "Event","stats_min": 22,"stats_max": 32,"refinement": "normal","description": "?!","image": "https://cdn.discordapp.com/attachments/767002369136525322/791688494522564638/SolyxXmasSETcleanPNG.png"}, {"name": "klompen","type": "armor","rarity": "Legendary","stats_min": 26,"stats_max": 35,"refinement": "Unreal","description": "?!","image": "None"}],"equip": {"name": "Solarflare","type": "staff","rarity": "Legendary","stats_min": 74,"stats_max": 74,"refinement": "Unreal","description": "?!","image": "https://i.imgur.com/ZP2KxJl.png"},"title": "breaker of solyx","location": "Golden Temple","daily_block": 0,"vote_block": 0,"voted": "False","hp_potions": 10000,"keys": 10000,"mine_block": 0,"chop_block": 0,"background": "https://i.imgur.com/L6JFu3m.jpg","online": 1614211938.7680876,"blacklisted": "False","Rachikilled": 10000,"Draugrkilled": 10000,"Debinkilled": 10000,"Stalkerkilled": 10000,"FireGolemkilled": 10000,"Wyvernkilled": 1413,"Ooferkilled": 10000,"Souleaterkilled": 10000,"Wolfkilled": 10000,"Goblinkilled": 10000,"Zombiekilled": 10000,"Phantasmkilled": 10000,"TheCorruptedkilled": 10000,"TheAccursedkilled": 10000,"ElderDragonkilled": 10000,"Hadeskilled": 10000,"EbonyGuardiankilled": 10000,"Harpykilled": 10000,"Dormammukilled": 10000,"Ettinkilled": 10000,"TheNamelessKingkilled": 10000,"Largoskilled": 45,"Deathclawkilled": 10000,"Sauriankilled": 10000,"TheVenomouskilled": 10000,"Skeletonkilled": 10000,"Lizardmenkilled": 10000,"Giantkilled": 10000,"DeathKnightkilled": 10000,"IceWolveskilled": 10000,"FrostOrckilled": 10000,"FrostGoblinkilled": 10000,"FrostDragonkilled": 10000,"exp_potions": 10000,"questname": "Claim your loot!","questprogress": 0,"questscompleted": ["Basic A", "Basic B", "Basic C", "Gathering Wood I", "Gathering Stone I", "Gathering Metal I", "Gathering Fish I", "Wood Trader I", "Stone Trader I", "Metal Trader I", "Health acquisition", "Unboxing I", "Daily I", "Equip", "VoteI","FightI","WikiCheck","ShopI","CheckProfile","Leaderboard", "Guild I", "Shop II", "Market I", "Guild II", "Rachi I", "Debin I", "Oofer I", "Wyvern I", "Fire Golem I", "Travel I", "Draugr I", "Stalker I", "Souleater I", "The Corrupted I", "Reforge I", "Support Server", "On the hunt!"],"questpart": 0,"enemydifficulty": "Common","MaxHealth": 250,"EnemyStun": 0,"SkillCooldown1": 0,"SkillCooldown2": 0,"Buff1": "None","Buff1Time": 0,"cooldown_infraction": 0,"monthlyrewards": 0,"sawmill": "True","masonry": "True","smeltery": "True","planks": 10000,"bricks": 10000,"iron_plates": 10000,"saw_block": 0,"mason_block": 0,"smelt_block": 0,"camp": "True","trap": 7,"trap1": 9,"trap2": 6,"trap3": 10,"trap4": 8,"trap5": 3,"trap6": 10,"trap7": 10,"trap8": 0,"trap9": 0,"trap10": 0,"trap11": 0,"trap12": 0,"trap13": 0,"trap_block": 0,"axelvl": 10,"pickaxelvl": 10,"sawlvl": 10,"chisellvl": 10,"hammerlvl": 10,"trader_time": 0,"trader_rarity": "Uncommon","trader_block": 0,"trader_wood": 0,"trader_stone": 0,"trader_metal": 0,"trader_planks": 0,"trader_bricks": 0,"trader_iron_plates": 0,"trader_profit": 10000,"Stunned": 0,"Debuff1": "False","DebuffTime1": 0,"pvpcooldown1": 0,"pvpcooldown2": 0,"TrapKills": 10000,"neck": {"name": "Necklace","type": "armor","rarity": "Legendary","stats_min": 38,"stats_max": 49,"refinement": "Unreal","description": "?!","image": "None"},"head": {"name": "Helmet","type": "armor","rarity": "Legendary","stats_min": 16,"stats_max": 29,"refinement": "Unreal","description": "?!","image": "None"},"body": {"name": "Chestplate","type": "armor","rarity": "Legendary","stats_min": 46,"stats_max": 63,"refinement": "Unreal","description": "?!","image": "None"},"finger": {"name": "married ring","type": "armor","rarity": "Legendary","stats_min": 13,"stats_max": 16,"refinement": "Unreal","description": "?!","image": "None"},"legs": {"name": "diamond pants","type": "armor","rarity": "Legendary","stats_min": 38,"stats_max": 49,"refinement": "Unreal","description": "?!","image": "None"},"feet": {"name": "Iron Boots","type": "feet","rarity": "Legendary","stats_min": 26,"stats_max": 35,"refinement": "Unreal","description": "?!","image": "None"},"friend_list": [],"friend_amount": 0,"friend_max_amount": 50,"party": {"oid": "6026ca0d8a47841d4ced8394"},"pet_find": "None","pet_list": [],"equipped_pet": [],"pet_stage": "Golden Goose","solyxvotes": {"numberLong": "3313"}}
		db.users.update({ "_id": user.id }, userinfo, upsert=True)
		print(db.users.update({ "_id": user.id }, {field: data}, upsert=True))
		print(data)
def setup(bot):
	n = misc(bot)
	bot.add_cog(n)




	
