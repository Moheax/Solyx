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


class updates(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def updates(self, ctx):
		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		if userinfo and userinfo["blacklisted"] == "True":
			return

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has check the latests updates")
		
		em = discord.Embed(color=discord.Colour(0xffffff))
		em.set_author(name="Solyx latest updates!", icon_url=user.avatar_url)
		em.add_field(name="\n_ _\n**\u27a4** 30 Nov by TheMaksoo".format(ctx.prefix), value="Fixed crates now it will always open the correct amount.",inline=False)	
		em.add_field(name="\n_ _\n**\u27a4** 30 Nov by TheMaksoo".format(ctx.prefix), value="Added 5% chance for easter egg on broken trap.",inline=False)	
		em.add_field(name="\n_ _\n**\u27a4** 30 Nov by TheMaksoo".format(ctx.prefix), value="Added -trap status to see the durability of your traps.",inline=False)	
		em.add_field(name="\n_ _\n**\u27a4** 30 Nov by TheMaksoo".format(ctx.prefix), value="Fixed that broken traps now show up as broken...",inline=False)	
		em.add_field(name="\n_ _\n**\u27a4** 30 Nov by TheMaksoo".format(ctx.prefix), value="Fixed when traps fail or break recources don't get added.",inline=False)	
		em.add_field(name="\n_ _\n**\u27a4** 30 Nov by TheMaksoo".format(ctx.prefix), value="Fixed spelling mistakes in cooldown and in traps.",inline=False)	


		await ctx.send(embed=em)





def setup(bot):
	n = updates(bot)
	bot.add_cog(n)