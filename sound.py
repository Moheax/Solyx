import discord
from discord.ext import commands

from random import choice as randchoice
import os, re, aiohttp
import random
import time
import asyncio
import io
import subprocess
import nacl
import logging

from utils.dataIO import fileIO
from utils.db import db
from utils.defaults import userdata, titledata, raiddata, battledata, guilddata

class sound(commands.Cog): # Make sure you have the sound stuff installed! pip install -U discord.py[voice]
	def __init__(self, bot):
		super().__init__()
		self.bot = bot

	@commands.command()
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def discordo(self, ctx):

		vc = ctx.voice_client
		user = ctx.author
		userinfo = db.users.find_one({ "_id": user.id })
		# Account check
		#if userinfo["class"] == "None" and userinfo["race"] == "None":
		#	await ctx.send("Start playing using {} kthx".format(ctx.prefix))
		#	return
		sound = 'data/sound/discordo.mp3'
		await self.play_sound(ctx, sound)

	@commands.command()
	@commands.cooldown(1, 20, commands.BucketType.user)
	async def radio(self, ctx):


		user = ctx.author
		userinfo = db.users.find_one({ "_id": user.id })
		# Account check
		#if userinfo["class"] == "None" and userinfo["race"] == "None":
		#	await ctx.send("Start playing using {} kthx".format(ctx.prefix))
		#	return
		await self.radioplayer(ctx)

	async def play_sound(self, ctx, sound):
		guild = ctx.guild
		if ctx.author.voice and ctx.author.voice.channel:
			authorvc = ctx.author.voice.channel
			if ctx.voice_client:
				vc = ctx.voice_client
				if vc.is_connected():
					botvc = ctx.voice_client.channel
					if not botvc == authorvc:
						if len(botvc.members) >= 2:
							try:
								await ctx.send("<:Solyx:560809141766193152> | I'm already connected to a VC!")
							except:
								return
							return
						else:
							try:
								await vc.move_to(authorvc)
							except:
								return
			else:
				try:
					vc = await authorvc.connect()
				except:
					return
			if not vc.is_playing():
				try:
					vc.play(discord.FFmpegPCMAudio(sound))
				except:
					return
			#await asyncio.sleep(5) -- Wait 5 sec to be sure the sound played
			#await vc.disconnect() -- Disconnect once done playing
		else:
			if ctx.voice_client:
				vc = ctx.voice_client
				if vc.is_connected():
					botvc = ctx.voice_client.channel
					if len(botvc.members) == 1:
						try:
							await vc.disconnect()
						except:
							return

	async def radioplayer(self, ctx):
		sound = randchoice(["data/music/BarovianCastle.mp3", "data/music/BeforeTheStorm.mp3", "data/music/CountryVillage.mp3", "data/music/CryHavoc.mp3", "data/music/MedievalFair.mp3", "data/music/MillTown.mp3", "data/music/RiverTown.mp3", "data/music/RoyalCourt.mp3", "data/music/Waterkeep.mp3", "data/music/WizardsTower.mp3"])
		guild = ctx.guild
		if ctx.author.voice and ctx.author.voice.channel:
			authorvc = ctx.author.voice.channel
			if ctx.voice_client:
				vc = ctx.voice_client
				if vc.is_connected():
					botvc = ctx.voice_client.channel
					if not botvc == authorvc:
						if len(botvc.members) >= 2:
							try:
								await ctx.send("<:Solyx:560809141766193152> | I'm already connected to a VC!")
							except:
								return
							return
						else:
							try:
								await vc.move_to(authorvc)
							except:
								return
			else:
				try:
					vc = await authorvc.connect()
				except:
					return
			if not vc.is_playing():
				try:
					vc.play(discord.FFmpegPCMAudio(sound))
					await asyncio.sleep(600)
					vc.stop()
					await self.radioplayer(ctx)
				except:
					return
			#await asyncio.sleep(5) -- Wait 5 sec to be sure the sound played
			#await vc.disconnect() -- Disconnect once done playing
		else:
			if ctx.voice_client:
				vc = ctx.voice_client
				if vc.is_connected():
					botvc = ctx.voice_client.channel
					if len(botvc.members) == 1:
						try:
							await vc.disconnect()
						except:
							return

def setup(bot):
	n = sound(bot)
	bot.add_cog(n)