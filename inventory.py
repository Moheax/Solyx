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




class inventory(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	


	@commands.group(pass_context=True, aliases=["inventory"], no_pm=True, invoke_without_command=True)
	@commands.cooldown(1, 12, commands.BucketType.user)
	async def inv(self, ctx, *, user : discord.Member=None):
				
		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"opened their inventory")

		if user == None:
			user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if len(userinfo["inventory"]) > 12:
			extraItems = "\n"
		else:
			extraItems = userinfo["inventory"]
		em = discord.Embed(color=discord.Colour(0xffffff))
		em.add_field(name="Supplies", value="<:GoldBars:573781770709893130> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}".format(int(userinfo["gold"]), userinfo["wood"], userinfo["stone"], userinfo["metal"]), inline=True)
		em.add_field(name="Items", value="<:Key:573780034355986432> {}\n<:Crate:639425690072252426> {}\n<:HealingPotion:573577125064605706> {}\n".format(userinfo["keys"], userinfo["lootbag"], userinfo["hp_potions"]), inline=True)
		em.set_author(name="{}'s Inventory".format(userinfo["name"]), icon_url=user.avatar_url)
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return



		channel = ctx.message.channel		
	
		userinfo = db.users.find_one({'_id':user.id})
		inventory =	userinfo["inventory"]
		list1 = ""
		for i, x in enumerate(range(12)):
			try:
				item = inventory[i]
				list1 += "**{}** > **{} {}** - **{}** {} - **{}-{}**:crossed_swords:\n".format(i + 1, item["refinement"], item["name"], item["rarity"], item["type"], item["stats_min"], item["stats_max"])
			except:
				pass
			#msg += "{} >\n".format(i + 1)
		em = embed = discord.Embed(description=list1, color=discord.Colour(0xffffff))
		em = embed.set_author(name="{}'s item list:⠀⠀⠀⠀⠀⠀⠀⠀⠀".format(user.name))
		em = embed.set_footer(text="Use the reactions to scroll between pages!")
		try:
			 await ctx.channel.send(embed=em)
		except:
			try:
				await ctx.channel.send("I cound't send the message.")
			except:
				return
			return
		try:
			await msg.add_reaction(u"\u25C0")
			await msg.add_reaction(u"\u25B6")
		except:
			return
		await self.item_list_menu_check(user)
		return
	
	async def item_list_menu_check(self, user):
		while True:

			try:
				await msg.add_reaction(u"\u25C0")
				await msg.add_reaction(u"\u25B6")
			except:
				return
		
			await asyncio.sleep(.2)

			reaction = await self.bot.wait_for("reaction_add")
			await asyncio.sleep(0.1)

			userinfo = db.users.find_one({'_id':user.id})
			inventory = userinfo["inventory"]

			list1 = ""
			list2 = ""
			for i, x in enumerate(range(24)):
				try:
					item = inventory[i]

					if i <= 11:
						list1 += "**{}** > **{} {}** - **{}** {} - **{}-{}**:crossed_swords:\n".format(i + 1, item["refinement"], item["name"], item["rarity"], item["type"], item["stats_min"], item["stats_max"])

					elif i > 11:
						list2 += "**{}** > **{} {}** - **{}** {} - **{}-{}**:crossed_swords:\n".format(i + 1, item["refinement"], item["name"], item["rarity"], item["type"], item["stats_min"], item["stats_max"])

				except:
					pass
					msg += "{} >\n".format(i + 1)

			if not reaction:
				try:
					await self.bot.clear_reactions(msg)
				except:
					return
				return


			if reaction.emoji == u"\u25C0":
				if msg.content == '⠀⠀':
					em = discord.Embed(title="Page 2/2", description=list2, color=discord.Colour(0xffffff))
					em.set_author(name="{}'s item list:⠀⠀⠀⠀⠀⠀⠀⠀⠀".format(user.name), icon_url=user.avatar_url)
					em.set_thumbnail(url=user.avatar_url)
					em.set_footer(text="Use the reactions to scroll between pages!")
					await self.bot.edit_message(msg, '⠀⠀', embed=em)

				elif msg.content == '':
					em = discord.Embed(title="Page 1/2", description=list1, color=discord.Colour(0xffffff))
					em.set_author(name="{}'s item list:⠀⠀⠀⠀⠀⠀⠀⠀⠀".format(user.name), icon_url=user.avatar_url)
					em.set_thumbnail(url=user.avatar_url)
					em.set_footer(text="Use the reactions to scroll between pages!")
					await self.bot.edit_message(msg, embed=em)


			elif reaction.emoji ==  u"\u25B6":
				if msg.content == '':
					em = discord.Embed(title="Page 2/2", description=list2, color=discord.Colour(0xffffff))
					em.set_author(name="{}'s item list:⠀⠀⠀⠀⠀⠀⠀⠀⠀".format(user.name), icon_url=user.avatar_url)
					em.set_thumbnail(url=user.avatar_url)
					em.set_footer(text="Use the reactions to scroll between pages!")
					await self.bot.edit_message(msg, '⠀⠀', embed=em)

				elif msg.content == '⠀⠀':
					em = discord.Embed(title="Page 1/2", description=list1, color=discord.Colour(0xffffff))
					em.set_author(name="{}'s item list:⠀⠀⠀⠀⠀⠀⠀⠀⠀".format(user.name), icon_url=user.avatar_url)
					em.set_thumbnail(url=user.avatar_url)
					em.set_footer(text="Use the reactions to scroll between pages!")
					await self.bot.edit_message(msg, embed=em)


def setup(bot):
	n = inventory(bot)
	bot.add_cog(n)