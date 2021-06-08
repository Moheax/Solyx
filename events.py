import discord
import random
import time
import datetime
from discord.ext import commands
import asyncio
from random import choice as randchoice
from discord import Permissions
from utils.checks import developer
from utils.db import db
from utils.dataIO import fileIO

class events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group(name="event",aliases=["events"], pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def _event(self, ctx):
		author = ctx.message.author
		authorinfo = db.users.find_one({ "_id": author.id })
		server = ctx.guild
		channel = ctx.channel
		servercolor = ctx.author.color
		msg = ""
		if ctx.invoked_subcommand is None:
			for x in ctx.command.all_commands:
				if x not in ctx.command.all_commands[x].aliases:
					if not ctx.command.all_commands[x].hidden:
						msg += f"`{ctx.prefix}{ctx.command.name} {x}` - {ctx.command.all_commands[x].help} \n"
			embed=discord.Embed(colour=servercolor)
			embed.set_author(name=ctx.command.name, icon_url=ctx.author.avatar_url)
			embed.add_field(name="Subcommands", value=msg, inline=False)
			try:
				await ctx.send(embed=embed)
			except:
				return
		return

	@_event.command(name="boss", pass_context=True)
	@commands.check(developer)
	async def _boss(self, ctx, bossname:str ):
		"""Toggle a boss event\nLevel 1 = `Gortac`"""
		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to equip armor!")

		eventinfo = db.users.find_one({ "_id": 387317544228487168 })
		if eventinfo["Gortac"] == True:
			eventinfo["Gortac"] = False
			db.users.replace_one({"_id": 387317544228487168}, eventinfo, upsert=True)
			em = discord.Embed(title="Gortac toggled", description="Gortac the Indestructible. event now disabled.", color=discord.Colour(0xffffff))
			em.set_footer(text="players can't fight the event boss anymore")
			await ctx.send(embed=em)
			return

		elif eventinfo["Gortac"] == False:
			eventinfo["Gortac"] = True
			db.users.replace_one({"_id": 387317544228487168}, eventinfo, upsert=True)
			em = discord.Embed(title="Gortac toggled", description="Gortac the Indestructible. event now active.", color=discord.Colour(0xffffff))
			em.set_footer(text="players can now fight the event boss.")
			await ctx.send(embed=em)
	
def setup(bot):
	n = events(bot)
	bot.add_cog(n)