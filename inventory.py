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
from cogs.quests import _quest_check


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
			userinfo["questprogress"] += 1
			if userinfo["questprogress"] >= 1:
				await _quest_check(self, ctx, user, userinfo)
			pass
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 

		if userinfo["role"] == "Developer":
		
			if len(userinfo["inventory"]) > 12:
				extraItems = "\n"
			else:
				extraItems = userinfo["inventory"]
			if userinfo["camp"] == "False":
				camp = "Not built yet"
			else:
				camp = "built!"
			if userinfo["sawmill"] == "False":
				sawmill = "Not built yet"
			else:
				sawmill = "built!"
			if userinfo["masonry"] == "False":
				masonry = "Not built yet"
			else:
				masonry = "built!"
			if userinfo["smeltery"] == "False":
				smeltery = "Not built yet"
			else:
				smeltery = "built!"
			em = discord.Embed(color=discord.Colour(0xffffff))
			em.add_field(name="Supplies", value="<:GoldBars:573781770709893130> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n".format(int(userinfo["gold"]), userinfo["wood"], userinfo["stone"], userinfo["metal"], userinfo["planks"], userinfo["bricks"], userinfo["iron_plates"]), inline=True)
			em.add_field(name="Items", value="<:Key:573780034355986432> {}\n<:Crate:639425690072252426> {}\n<:HealingPotion:573577125064605706> {}\n<:ExpBottle:770044187348566046> {}\n<:petfood:849024713995845723> {}\n".format(userinfo["keys"], userinfo["lootbag"], userinfo["hp_potions"], userinfo["exp_potions"], int(userinfo["pet_food"])), inline=True)
			em.add_field(name="Buildings", value="**Camp:** {}\n **Sawmill:** {}\n **Masonry:** {}\n **Smeltery:** {}\n **Traps:** {}".format(camp, sawmill, masonry, smeltery,userinfo["trap"]), inline=True)
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

			list = ""

			for i, x in enumerate(range(0, 26)):
				try:
					item = inventory[i]
					type = item["type"]			
					if type == "sword":
						list += "**{}.** - **{}** - {} - **{}-{}**<:Sword:573576884688781345>\n".format(i + 1, item["name"], item["type"], item["stats_min"], item["stats_max"])

					if type == "bow":
						list += "**{}.** - **{}** - {} - **{}-{}**<:Bow:573576981791113218>\n".format(i + 1, item["name"], item["type"], item["stats_min"], item["stats_max"])

					if type == "staff":
						list += "**{}.** - **{}** - {} - **{}-{}**<:Staff:573578258419810335>\n".format(i + 1, item["name"], item["type"], item["stats_min"], item["stats_max"])

					if type == "mace":
						list += "**{}.** - **{}** - {} - **{}-{}**<:Mace:761025040145186846>\n".format(i + 1, item["name"], item["type"], item["stats_min"], item["stats_max"])

					if type == "dagger":
						list += "**{}.** - **{}** - {} - **{}-{}**<:Dagger:761025864422916096>\n".format(i + 1, item["name"], item["type"], item["stats_min"], item["stats_max"])

					if type == "gun":
						list += "**{}.** - **{}** - {} - **{}-{}**<:Gun:573578066853494830>\n".format(i + 1, item["name"], item["type"], item["stats_min"], item["stats_max"])

					if type == "armor":
						list += "**{}.** - **{}** - {} - **{}-{}**<:Shield:573576333863682064>\n".format(i + 1, item["name"], item["type"], item["stats_min"], item["stats_max"])

					if type == "head":
						list += "**{}.** - **{}** - {} - **{}-{}**:military_helmet:\n".format(i + 1, item["name"], item["type"], item["stats_min"], item["stats_max"])

					if type == "neck":
						list += "**{}.** - **{}** - {} - **{}-{}**:prayer_beads:\n".format(i + 1, item["name"], item["type"], item["stats_min"], item["stats_max"])

					if type == "body":
						list += "**{}.** - **{}** - {} - **{}-{}**:shirt:\n".format(i + 1, item["name"], item["type"], item["stats_min"], item["stats_max"])

					if type == "finger":
						list += "**{}.** - **{}** - {} - **{}-{}**:ring:\n".format(i + 1, item["name"], item["type"], item["stats_min"], item["stats_max"])

					if type == "legs":
						list += "**{}.** - **{}** - {} - **{}-{}**:jeans:\n".format(i + 1, item["name"], item["type"], item["stats_min"], item["stats_max"])

					if type == "feet":
						list += "**{}.** - **{}** - {} - **{}-{}**:boot:\n".format(i + 1, item["name"], item["type"], item["stats_min"], item["stats_max"])
				except:
					pass
				#msg += "{} >\n".format(i)
			em = embed = discord.Embed(color=discord.Colour(0xffffff))
			em = embed.description = list
			em = embed.set_author(name="{}'s inventory".format(user.name))

			try:
				 msg = await ctx.channel.send(embed=em)

			except:
				try:
					await ctx.channel.send("I cound't send the message.")
				except:
					return
				return
		else:

			if len(userinfo["inventory"]) > 12:
				extraItems = "\n"
			else:
				extraItems = userinfo["inventory"]
			if userinfo["camp"] == "False":
				camp = "Not built yet"
			else:
				camp = "built!"
			if userinfo["sawmill"] == "False":
				sawmill = "Not built yet"
			else:
				sawmill = "built!"
			if userinfo["masonry"] == "False":
				masonry = "Not built yet"
			else:
				masonry = "built!"
			if userinfo["smeltery"] == "False":
				smeltery = "Not built yet"
			else:
				smeltery = "built!"
			em = discord.Embed(color=discord.Colour(0xffffff))
			em.add_field(name="Supplies", value="<:GoldBars:573781770709893130> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n".format(int(userinfo["gold"]), userinfo["wood"], userinfo["stone"], userinfo["metal"], userinfo["planks"], userinfo["bricks"], userinfo["iron_plates"]), inline=True)
			em.add_field(name="Items", value="<:Key:573780034355986432> {}\n<:Crate:639425690072252426> {}\n<:HealingPotion:573577125064605706> {}\n<:ExpBottle:770044187348566046> {}\n<:petfood:849024713995845723> {}\n".format(userinfo["keys"], userinfo["lootbag"], userinfo["hp_potions"], userinfo["exp_potions"], int(userinfo["pet_food"])), inline=True)
			em.add_field(name="Buildings", value="**Camp:** {}\n **Sawmill:** {}\n **Masonry:** {}\n **Smeltery:** {}\n **Traps:** {}".format(camp, sawmill, masonry, smeltery,userinfo["trap"]), inline=True)
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

	@commands.group(name="item", aliases=["weapon"], pass_context=True, no_pm=True, hidden=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _item(self, ctx):
		"""request extra info about a item!"""
		guild = ctx.guild
		channel = ctx.channel
		guildcolor = ctx.author.color

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]
			
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

	@_item.group(name="info", pass_context=True, no_pm=True)
	@commands.cooldown(1, 12, commands.BucketType.user)
	async def _info(self, ctx, number:int):	
		"""have some extra info of an item!"""
		user = ctx.message.author

		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has requested more info!")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if number not in range(1, 26): # Max
			return await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["itemnotexist"]["translation"])


		try:
			item = userinfo["inventory"][number-1]
		except:
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["equip"]["noiteminslot"]["translation"])
			return

		
		em = discord.Embed(title="{}".format(item["name"]), description="**Rarity:** {}\n**Refinement:** {}\n**Type:** {}\n**Stats:** {}-{}\n".format(item["rarity"], item["refinement"], item["type"], item["stats_min"], item["stats_max"]), color=discord.Colour(0xffffff))
		if not item["image"] == "None":
			em.set_thumbnail(url=item["image"])
		await ctx.send(embed=em)




def setup(bot):
	n = inventory(bot)
	bot.add_cog(n)