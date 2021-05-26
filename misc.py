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
		em = discord.Embed(title="\n", description="🎉Thank you so much for 470K USERS OML🎉",color=discord.Colour(0xffffff))	
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
		userinfo["health"] = userinfo["MaxHealth"]
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
	async def staff(self, ctx):
		
		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild
		
		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to set something in the database")
		
		


		em = discord.Embed(title="Solyx staff list.", description="AceTheBearg223#4562\nTheMaksoo#1212\n\nTwannie#8493\nFailed#4444",color=discord.Colour(0xffffff))	
		await ctx.send(embed=em)


	@commands.command(pass_context=True, no_pm=True)	
	@commands.cooldown(1, 4, commands.BucketType.user)
	@commands.check(developer)
	async def test(self, ctx):
		monstercolor = discord.Colour(0xffffff)
		fight_msg = "Test\nuwuwu"
		name_msg = ""
		em = discord.Embed(color=monstercolor)
		em.add_field(name=name_msg, value=fight_msg, inline=False)
		await ctx.send(embed=em)

def setup(bot):
	n = misc(bot)
	bot.add_cog(n)




	
