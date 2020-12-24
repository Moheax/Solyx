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

intents = discord.Intents.default()
intents.reactions = True

class giveaway(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group(name="giveaway", pass_context=True, no_pm=True)
	@commands.cooldown(1, 1, commands.BucketType.user)
	@commands.check(developer)
	async def giveaway(self, ctx):
		guild = ctx.guild
		channel = ctx.channel
		guildcolor = ctx.author.color
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
	

	@giveaway.command(name="create", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def create(self, ctx, channelid, gtime, prizeamount:int, prize:str, winners:int):
		"""Create a give away"""
		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		tamount = 0
		try:

			pos = ["s","m","h","d"]

			time_dict = {"s" * 1, "m" * 60, "h" * 3600, "d" * 3600*24}

			unit = gtime[-1]
			tamount = int(gtime[:-1])

			if unit == "s":
				tamount = tamount * 1

			if unit == "m":
				tamount = tamount * 60

			if unit == "h":
				tamount = tamount * 3600

			if unit == "d":
				tamount = tamount * 3600 * 24

			try:
				val = int(gtime[:-1])
				val * time_dict[unit]
			except Exception as e:
				print(e)
		except Exception as e:
				print(e)

		c_id = channelid[2:-1]

		data = (c_id, tamount, winners, prizeamount, prize)


		gchannel = self.bot.get_channel(int(c_id))

		
		await ctx.send("The Giveaway will be in {} and wil last {} seconds the prize will be {} {} and there will be {} winner(s) ".format(gchannel.mention, tamount, prizeamount, prize, winners))

		embed = discord.Embed(title = "Giveaway!", description = " {} {} ".format(prizeamount, prize), color=discord.Colour(0xffffff))
		embed.add_field(name = "winners", value = winners)
		embed.set_footer(text = "Ends {} seconds From now!".format(tamount))
		
		g_msg = await gchannel.send(embed=embed)

		await g_msg.add_reaction("<:Solyx:560809141766193152>")

		await asyncio.sleep(int(tamount))



		users = ""  
		reaction = "<:Solyx:560809141766193152>"

		new_msg = await gchannel.fetch_message(g_msg.id)

		for reaction in new_msg.reactions:
			async for user in reaction.users():

				users = await new_msg.reactions[0].users().flatten()
				users.pop(users.index(self.bot.user))
	
		for i in range(winners):
			if not users:
				await gchannel.send("No more winners can be choosen")
				return
			winner = random.choice(users)
			await gchannel.send("Congratulations {} you won {} {}".format(winner.mention, prizeamount, prize))
			users.pop(users.index(winner))


		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has started a giveaway")
		

	





def setup(bot):
	n = giveaway(bot)
	bot.add_cog(n)