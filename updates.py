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
		em.add_field(name="\n_ _\n**\u27a4** 27 Nov by TheMaksoo".format(ctx.prefix), value="Massive update!!!!\n\nWe have traps!\nthe only ""passive"" exp and gold income you can have.\n\nYou can make traps with -traps build\nprices go up quite \nast but they are worth it!!\n\nnormal users can have 4 traps \nlevel 100+ can have 5 traps\nLevel 200+ can have 7 traps\ncommon supporter can have 7 with out level requirement\nrare supporter can have 9 traps\nlegendary supporter can \nhave 11 traps\nmythical supporter can have 13 traps\n\nYou can ""Check"" your traps even 1 hour with -traps check\nLegendary supporters have a 20% cooldown reduction\nMythical supporters have a 50% cooldown reduction\n\nTraps get \n""placed""in the location you are at.\ntraps have 80% of catching a monster, the monster will be from that area and will have the same rewards as normal fighting, theres common uncommon rare legendary mythical monsters PART 1",inline=False)
		em2 = discord.Embed(color=discord.Colour(0xffffff))
		em2.set_author(name="Solyx latest updates!", icon_url=user.avatar_url)
		em2.add_field(name="\n_ _\n**\u27a4** 26 Nov by TheMaksoo".format(ctx.prefix), value="\ntraps havea \n15% chance of failing to catch a monster.\ntraps have a 5% chance of breaking.\ntraps break after 10 uses\n\nYou can repair your traps for 5 wood 5 stone and 2 metal and 100gold each\n\nAdded traps to inventory under buildings,\nAdded\ntraps cooldown to cooldowns\n\nI hope this makes it for the non fighting users a bit more enjoyable and a way to earn money and level!\n(big 400K update)", inline=False)
		em2.add_field(name="\n_ _\n**\u27a4** 26 Nov by TheMaksoo".format(ctx.prefix), value="Added new command -updates\nadded the command in -help and in -commands", inline=False)
		em2.add_field(name="\n_ _\n**\u27a4** 26 Nov by TheMaksoo".format(ctx.prefix), value="Rewrote and updated -commands!", inline=False)
		em2.add_field(name="\n_ _\n**\u27a4** 25 Nov by TheMaksoo".format(ctx.prefix), value="We have 4 new buildings.\nTo build something type -build\n**Camp:** a camp is required to make other buildings.\n\n**Sawmill:** a sawmill will be built inside your camp and \nyou get the option to create planks! (3 wood for 2 planks)(type -saw <amount> )\n\n**Masonry:** the masonry will also be built inside the camp, it also requires planks to be build!, once its build you  get the option to\nmake bricks( 5 stone for 4 bricks.)(type -mason <amount>)\n\n**Smeltery:** the smeltery will also be built inside the camp and requires planks and bricks, when build you can make Iron plates ( 5 metal for 4 iron plates)\n(type -smelt <amount>)\n\nSaw, mason and smelt have a 20 minute cooldown for patreon tier 3 and 4 its -20% and -50%\n\nThere are 3 new recources \nPlanks made from wood\nBricks made from stone\nIron plates made \nfrom metal\n\nThey will have more use in the future but for now gather them!\n\nAdded the buildings to inventory list\nAdded the new recources to the inventory supply list!!\n_ _\n", inline=False)
		em2.add_field(name="\n_ _\n**\u27a4** 25 Nov by TheMaksoo".format(ctx.prefix), value="Fixed that knights cant equip maces!", inline=False)
		em2.add_field(name="\n_ _\n**\u27a4** 24 Nov by TheMaksoo".format(ctx.prefix), value="Fancy update for patreons!\n\ncooldown reduction is here!\n\nLegendary has 20% cooldown reduction (for gathering)\nMythical has 50% cooldown reduction (for gathering)\n\nFor example\nnormal cooldown 10min\nlegendary cooldown 8min\nMythical cooldown 5min", inline=False)
		await ctx.send(embed=em)
		await ctx.send(embed=em2)





def setup(bot):
	n = updates(bot)
	bot.add_cog(n)