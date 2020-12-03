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
		em = discord.Embed(title="\n", description="🎉Thank you sooo much for 400K Users!!!!!!!!!!!!!!!!!! 🎉",color=discord.Colour(0xffffff))	
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
	async def users(self, ctx):
		totalusers = db.users.count()
		print(totalusers)
		await ctx.send(totalusers)

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
def setup(bot):
	n = misc(bot)
	bot.add_cog(n)