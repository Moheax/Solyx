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

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has booped solyx")
		print('boop')
		em = discord.Embed(title="BOOP?!", description="No u",color=discord.Colour(0xffffff))	
		await ctx.send(embed=em)

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	@commands.check(developer)
	async def bap(self, ctx):
		print('boop')
		em = discord.Embed(title="\n", description="🎉Thank you for 350K Users! 🎉",color=discord.Colour(0xffffff))	
		await ctx.send(embed=em)

	@commands.command(pass_context=True, no_pm=True)
	@commands.check(developer)
	async def users(self, ctx):
		totalusers = db.users.count()
		print(totalusers)
		await ctx.send(totalusers)


	
def setup(bot):
	n = misc(bot)
	bot.add_cog(n)