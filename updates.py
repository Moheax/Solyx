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
		em.add_field(name="\n_ _\n**\u27a4** 29 Jan by TheMaksoo".format(ctx.prefix), value="Friend list capacity now updates!.",inline=False)	
		em.add_field(name="\n_ _\n**\u27a4** 29 Jan by TheMaksoo".format(ctx.prefix), value="We added Friends to solyx. [-f].",inline=False)	
		em.add_field(name="\n_ _\n**\u27a4** 29 Jan by TheMaksoo".format(ctx.prefix), value="Fixed wrong amount in fire golem kill quest.",inline=False)	
		em.add_field(name="\n_ _\n**\u27a4** 29 Jan by TheMaksoo".format(ctx.prefix), value="Trap kills now have their own statistic.",inline=False)	
		em.add_field(name="\n_ _\n**\u27a4** 29 Jan by TheMaksoo".format(ctx.prefix), value="Fixed Traps status finnaly.",inline=False)	
		em.add_field(name="\n_ _\n**\u27a4** 29 Jan by TheMaksoo".format(ctx.prefix), value="Fixed wrong amount in fire golem kill quest.",inline=False)	
		em.add_field(name="\n_ _\n**\u27a4** 29 Jan by TheMaksoo".format(ctx.prefix), value="Finnaly fixed leaderboard.",inline=False)	
		

		await ctx.send(embed=em)





def setup(bot):
	n = updates(bot)
	bot.add_cog(n)