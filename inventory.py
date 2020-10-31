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

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]
				
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

		if userinfo and userinfo["blacklisted"] == "True":
			return


		if userinfo["questname"] == "Basic B":
			userinfo["questprogress"] = userinfo["questprogress"] + 1
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			if userinfo["questprogress"] >= 1:
				await ctx.send("Quest Updated!")
			pass

		if len(userinfo["inventory"]) > 12:
			extraItems = "\n"
		else:
			extraItems = userinfo["inventory"]
		em = discord.Embed(color=discord.Colour(0xffffff))
		em.add_field(name="Supplies", value="<:GoldBars:573781770709893130> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}".format(int(userinfo["gold"]), userinfo["wood"], userinfo["stone"], userinfo["metal"]), inline=True)
		em.add_field(name="Items", value="<:Key:573780034355986432> {}\n<:Crate:639425690072252426> {}\n<:HealingPotion:573577125064605706> {}\n<:ExpBottle:770044187348566046> {}\n".format(userinfo["keys"], userinfo["lootbag"], userinfo["hp_potions"], userinfo["exp_potions"]), inline=True)
		em.set_author(name="{}'s Inventory".format(userinfo["name"]), icon_url=user.avatar_url)
		em.set_footer(text="Type | -vote | and vote for extra rewards!")
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
		list2 = ""

		for i, x in enumerate(range(0, 26)):
			try:
				item = inventory[i]
				type = item["type"]
				if i <= 12 and i >= 0:			
					if type == "sword":
						list1 += "**{}** - {} - **{}** - **{}** {} - **{}-{}**<:Sword:573576884688781345>\n".format(i + 1, item["refinement"], item["name"], item["rarity"], item["type"], item["stats_min"], item["stats_max"])

					if type == "bow":
						list1 += "**{}** - {} - **{}** - **{}** {} - **{}-{}**<:Bow:573576981791113218>\n".format(i + 1, item["refinement"], item["name"], item["rarity"], item["type"], item["stats_min"], item["stats_max"])

					if type == "staff":
						list1 += "**{}** - {} - **{}** - **{}** {} - **{}-{}**<:Staff:573578258419810335>\n".format(i + 1, item["refinement"], item["name"], item["rarity"], item["type"], item["stats_min"], item["stats_max"])

					if type == "mace":
						list1 += "**{}** - {} - **{}** - **{}** {} - **{}-{}**<:Mace:761025040145186846>\n".format(i + 1, item["refinement"], item["name"], item["rarity"], item["type"], item["stats_min"], item["stats_max"])

					if type == "dagger":
						list1 += "**{}** - {} - **{}** - **{}** {} - **{}-{}**<:Dagger:761025864422916096>\n".format(i + 1, item["refinement"], item["name"], item["rarity"], item["type"], item["stats_min"], item["stats_max"])

					if type == "gun":
						list1 += "**{}** - {} - **{}** - **{}** {} - **{}-{}**<:Gun:573578066853494830>\n".format(i + 1, item["refinement"], item["name"], item["rarity"], item["type"], item["stats_min"], item["stats_max"])

					if type == "armor":
						list1 += "**{}** - {} -  **{}** - **{}** {} - **{}-{}**<:Shield:573576333863682064>\n".format(i + 1, item["refinement"], item["name"], item["rarity"], item["type"], item["stats_min"], item["stats_max"])

				if i >= 13:			
					if type == "sword":
						list2 += "**{}** - {} - **{}** - **{}** {} - **{}-{}**<:Sword:573576884688781345>\n".format(i + 1, item["refinement"], item["name"], item["rarity"], item["type"], item["stats_min"], item["stats_max"])

					if type == "bow":
						list2 += "**{}** - {} - **{}** - **{}** {} - **{}-{}**<:Bow:573576981791113218>\n".format(i + 1, item["refinement"], item["name"], item["rarity"], item["type"], item["stats_min"], item["stats_max"])

					if type == "staff":
						list2 += "**{}** - {} - **{}** - **{}** {} - **{}-{}**<:Staff:573578258419810335>\n".format(i + 1, item["refinement"], item["name"], item["rarity"], item["type"], item["stats_min"], item["stats_max"])

					if type == "mace":
						list2 += "**{}** - {} - **{}** - **{}** {} - **{}-{}**<:Mace:761025040145186846>\n".format(i + 1, item["refinement"], item["name"], item["rarity"], item["type"], item["stats_min"], item["stats_max"])

					if type == "dagger":
						list2 += "**{}** - {} - **{}** - **{}** {} - **{}-{}**<:Dagger:761025864422916096>\n".format(i + 1, item["refinement"], item["name"], item["rarity"], item["type"], item["stats_min"], item["stats_max"])

					if type == "gun":
						list2 += "**{}** - {} - **{}** - **{}** {} - **{}-{}**<:Gun:573578066853494830>\n".format(i + 1, item["refinement"], item["name"], item["rarity"], item["type"], item["stats_min"], item["stats_max"])

					if type == "armor":
						list2 += "**{}** - {} -  **{}** - **{}** {} - **{}-{}**<:Shield:573576333863682064>\n".format(i + 1, item["refinement"], item["name"], item["rarity"], item["type"], item["stats_min"], item["stats_max"])
			except:
				pass
			#msg += "{} >\n".format(i)
		em = embed = discord.Embed(color=discord.Colour(0xffffff))
		em = embed.description = list1
		em = embed.set_author(name="{}'s item list 1:⠀⠀⠀⠀⠀⠀⠀⠀⠀".format(user.name))

		em2 = embed = discord.Embed(color=discord.Colour(0xffffff))
		em2 = embed.description = list2
		em2 = embed.set_author(name="{}'s item list 2:⠀⠀⠀⠀⠀⠀⠀⠀⠀".format(user.name))
		try:
			 msg = await ctx.channel.send(embed=em)
			 await ctx.channel.send(embed=em2)
		except:
			try:
				await ctx.channel.send("I cound't send the message.")
			except:
				return
			return

		#await msg.add_reaction('\u25C0')
		#await msg.add_reaction('\u25B6')
		#print("hi")
		"""
		await self.item_list_menu_check(user)
		return
	
	async def item_list_menu_check(self, user):
		while True:
		
			await asyncio.sleep(.2)

			try:
				reaction, user = await self.bot.wait_for("reaction_add")
			except Exception as e:
				print(e)
			return

			userinfo = db.users.find_one({'_id':user.id})
			inventory = userinfo["inventory"]
				
			list1 = ""
			list2 = ""
			for i, x in enumerate(range(1, 25)):
				try:
					item = inventory[i]

					if i <= 24:
						list1 += "**{}** > **{} {}** - **{}** {} - **{}-{}**:crossed_swords:\n".format(i, item["refinement"], item["name"], item["rarity"], item["type"], item["stats_min"], item["stats_max"])

					elif i > 11:
						list2 += "**{}** > **{} {}** - **{}** {} - **{}-{}**:crossed_swords:\n".format(i, item["refinement"], item["name"], item["rarity"], item["type"], item["stats_min"], item["stats_max"])

				except:
					pass
					msg += "{} >\n".format(i)

			if not reaction:
				try:
					await self.bot.clear_reactions(msg)
				except:
					return
				return


			if reaction.emoji == '\u25C0':
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


			elif reaction.emoji == '\u25B6':
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
				"""

def setup(bot):
	n = inventory(bot)
	bot.add_cog(n)