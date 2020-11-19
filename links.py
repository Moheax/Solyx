import discord
from discord.ext import commands

import datetime
import asyncio
import random
from random import choice as randchoice
from time import time

from utils.dataIO import fileIO
from utils.db import db
from utils.defaults import userdata, titledata, raiddata, battledata, guilddata



class links(commands.Cog):
	def __init__(self, bot):
		super().__init__()
		self.bot = bot

		# LINKS WORK

	@commands.command(pass_context=True, name="Donate", aliases=["donate"])
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def _donate(self, ctx):

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has check the donation site!!!!!!")

		
		color = 0xffffff
		embed = discord.Embed(colour=color)
		embed.add_field(name="Donate to solyx!", value="You can check out the donation options by clicking [here](https://www.patreon.com/Solyx?fan_landing=true)!")
		embed.set_thumbnail(url=ctx.bot.user.avatar_url)
		try:
			await ctx.send(ctx.message.author.mention, embed=embed)
		except:
			await ctx.send(ctx.message.channel, "I cound't send the message.")


	@commands.command(pass_context=True, name="invite", aliases=["server"])
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def _invite(self, ctx):

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has asked for the invite!")

		#Invite me to your guild
		color = 0xffffff
		embed = discord.Embed(colour=color)
		embed.add_field(name="Invite Solyx to you guild!", value="You can add me by clicking [here](https://discord.com/api/oauth2/authorize?client_id=495928914045304847&permissions=378944&redirect_uri=https%3A%2F%2Fsolyxbot.webflow.io%2F&scope=bot)!")
		embed.set_thumbnail(url=ctx.bot.user.avatar_url)
		try:
			await ctx.send(ctx.message.author.mention, embed=embed)
		except:
			await ctx.send(ctx.message.channel, "I cound't send the message.")

	#@commands.command(pass_context=True, name="guild")
	#@commands.cooldown(1, 10, commands.BucketType.user)
	#async def _guild(self, ctx):
	#	"""Support guild"""
	#	color = 0xffffff
	#	embed = discord.Embed(colour=color)
	#	embed.add_field(name="Join the Solyx support guild!", value="You can join by clicking [here](https://discord.gg/CVxzCKj)!")
	#	embed.set_thumbnail(url=ctx.bot.user.avatar_url)
	#	try:
	#		await ctx.send(ctx.message.author.mention, embed=embed)
	#	except:
	#		await ctx.send(ctx.message.channel, "I cound't send the message.")

	@commands.command(pass_context=True, name="website")
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def _website(self, ctx):

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has asked for the website!")

		#Website
		color = 0xffffff
		embed = discord.Embed(colour=color)
		embed.add_field(name="Check out the Solyx website!", value="Click [here](https://solyxbot.webflow.io/) to visit the website!")
		embed.set_thumbnail(url=ctx.bot.user.avatar_url)
		try:
			await ctx.send(ctx.message.author.mention, embed=embed)
		except:
			await ctx.send(ctx.message.channel, "I cound't send the message.")

	@commands.command(pass_context=True, name="patreon")
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def _patreon(self, ctx):

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has asked for the website!")

		#Website
		color = 0xffffff
		embed = discord.Embed(colour=color)
		embed.add_field(name="Check out the Solyx patreon!", value="Click [here](https://www.patreon.com/Solyx?fan_landing=true) to visit the patreon site!")
		embed.set_thumbnail(url=ctx.bot.user.avatar_url)
		try:
			await ctx.send(ctx.message.author.mention, embed=embed)
		except:
			await ctx.send(ctx.message.channel, "I cound't send the message.")

	@commands.command(pass_context=True, name="botstatus")
	@commands.cooldown(1, 20, commands.BucketType.user)
	async def _botstatus(self, ctx):

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has asked for the botstatus")
		
		#Bot status page
		color = 0xffffff
		embed = discord.Embed(colour=color)
		embed.add_field(name="Check out the Solyx status page!", value="Click [here](https://solyxbot.webflow.io/) to visit the status page!")
		embed.set_thumbnail(url=ctx.bot.user.avatar_url)
		try:
			await ctx.send(ctx.message.author.mention, embed=embed)
		except:
			await ctx.send(ctx.message.channel, "I cound't send the message.")

	@commands.command(pass_context=True, name="support")
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def _support(self, ctx):

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has asked for support!")
		
		
		#Support
		color = 0xffffff
		embed = discord.Embed(colour=color)
		embed.add_field(name="Solyx support guild", value="Click [here](https://discord.gg/SpKUA8y) to join!")
		embed.add_field(name="  Website", value="  Click [here](https://solyxbot.webflow.io/) to visit the website!")
		embed.set_thumbnail(url=ctx.bot.user.avatar_url)
		try:
			await ctx.send(ctx.message.author.mention, embed=embed)
		except:
			await ctx.send(ctx.message.channel, "I cound't send the message.")


def setup(bot):
	c = links(bot)
	bot.add_cog(c) 