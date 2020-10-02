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


class status(commands.Cog):
	def __init__(self, bot):
		super().__init__()
		self.bot = bot

				
# - - - User info - - - WORKS

	@commands.command(pass_context=True, aliases=["stats"], no_pm=True)
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def status(self, ctx):

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has Checked their status")

		guild = ctx.message.guild
		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return
		maxexp = 100 + ((userinfo["lvl"] + 1) * 3.5)
		if not userinfo["guild"] == "None":
			try:
				guildid = userinfo["guild"]
				userguild = self.bot.get_guild(guildid)
			except:
				userguild = guild
		else:
			userguild = guild

		if not userinfo["equip"] == "None":
			weaponequipped = userinfo["equip"]["name"]
			item = userinfo["equip"]["stats_min"]
			item2 = userinfo["equip"]["stats_max"]
		else:
			weaponequipped = "None"
			item = ""
			item2 = ""

		if not userinfo["wearing"] == "None":
			armorequipped = userinfo["wearing"]["name"]
			item3 = userinfo["equip"]["stats_min"]
			item4 = userinfo["equip"]["stats_max"]
		else:
			armorequipped = "None"
			item3 = ""
			item4 = ""

		em = discord.Embed(description="**Name:** {}\n**Race:** {}\n**Class:** {}\n**Title:** {}\n**Guild:** {}\n\n**Level:** {}\n**Exp:** {}/{}\n**Health:** {}".format(userinfo["name"], userinfo["race"], userinfo["class"], userinfo["title"], userguild.name, userinfo["lvl"], userinfo["exp"], maxexp, userinfo["health"]), color=discord.Colour(0xffffff))
		em.add_field(name="Equipment", value="**Weapon:** {}\n**Weapon Damage:** {}-{}\n\n**Armor:** {}\n**Armor Defense:** {}-{}\n".format(weaponequipped, item, item2, armorequipped, item3, item4), inline=False)
		em.add_field(name="History", value="**Kills:** {}\n**Deaths:** {}".format(userinfo["enemieskilled"], userinfo["deaths"]), inline=False)
		em.set_author(name="{}'s Statistics".format(userinfo["name"]), icon_url=user.avatar_url)
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return

def setup(bot):
	c = status(bot)
	bot.add_cog(c)