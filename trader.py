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

class trader(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	

	@commands.group(name="trader", aliases=["merchant"], pass_context=True, no_pm=True, hidden=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _trader(self, ctx):
		"""trader stuff"""
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


	@_trader.group(name="find", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _find(self, ctx):
		"""Find a trader."""
		

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to find a trader")

		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return
	
		

		Rarity = random.randint(1, 100)

		userinfo["trader_rarity"] = "Common"
		userinfo["trader_profit"] = 0
		if Rarity >= 99:
			userinfo["trader_rarity"] = "Mythical"
			userinfo["trader_wood"] = 250
			userinfo["trader_stone"] = 250
			userinfo["trader_metal"] = 200
			userinfo["trader_planks"] = 150
			userinfo["trader_bricks"] = 150
			userinfo["trader_iron_plates"] = 100

		elif Rarity <= 99 and Rarity >= 90:
			userinfo["trader_rarity"] = "Legendary"
			userinfo["trader_wood"] = 200
			userinfo["trader_stone"] = 200
			userinfo["trader_metal"] = 150
			userinfo["trader_planks"] = 100
			userinfo["trader_bricks"] = 100
			userinfo["trader_iron_plates"] = 0

		elif Rarity <= 90 and Rarity >= 70:
			userinfo["trader_rarity"] = "Rare"
			userinfo["trader_wood"] = 150
			userinfo["trader_stone"] = 150
			userinfo["trader_metal"] = 100
			userinfo["trader_planks"] = 50
			userinfo["trader_bricks"] = 0
			userinfo["trader_iron_plates"] = 0

		elif Rarity <= 70 and Rarity >= 50:
			userinfo["trader_rarity"] = "Uncommon"
			userinfo["trader_wood"] = 100
			userinfo["trader_stone"] = 100
			userinfo["trader_metal"] = 50
			userinfo["trader_planks"] = 0
			userinfo["trader_bricks"] = 0
			userinfo["trader_iron_plates"] = 0

		elif Rarity <= 50 and Rarity >= 0:
			userinfo["trader_rarity"] = "Common"	
			userinfo["trader_wood"] = 50
			userinfo["trader_stone"] = 50
			userinfo["trader_metal"] = 25
			userinfo["trader_planks"] = 0
			userinfo["trader_bricks"] = 0
			userinfo["trader_iron_plates"] = 0

		curr_time = time.time()
		delta = float(curr_time) - float(userinfo["trader_block"])

		cooldowntime = 28800
		

		if userinfo["role"] == "patreon3":
			cooldowntime = 23040
		if userinfo["role"] == "patreon4":
			cooldowntime = 14400

		if delta >= cooldowntime and delta > 0:

			em = discord.Embed(title="Trader found!", description="You have found a {} Trader!\nThe trader stays for 10 minutes! ".format(userinfo["trader_rarity"]), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			userinfo["trader_time"] = curr_time
			userinfo["trader_block"] = curr_time

			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		else:
			# calulate time left
			seconds = cooldowntime - delta
			m, s = divmod(seconds, 60)
			h, m = divmod(m, 60)
			em = discord.Embed(title=":hourglass: trader is away!", description="for another " + str(round(h)) + " Hours, " + str(round(m)) + " Minutes and " + str(round(s)) + " Seconds", color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
				except:
					pass
				pass




	@_trader.group(name="inv", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _inv(self, ctx):
		"""Check the traders wares."""
		
		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has bought something from the trader")

		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		
		title = "trader!" 
		list1 = ""
		if userinfo["trader_rarity"] == "Mythical":
			title = "<:Mythical:573784881386225694> Mythical trader!"
			list1 += "<:Wood:573574660185260042> {}x = 70<:Gold:639484869809930251> Per piece.\n".format(userinfo["trader_wood"])
			list1 += "<:Stone:573574662525550593> {}x = 70<:Gold:639484869809930251> Per piece.\n".format(userinfo["trader_stone"])
			list1 += "<:Metal:573574661108006915> {}x = 80<:Gold:639484869809930251> Per piece. \n".format(userinfo["trader_metal"])
			list1 += "<:PlanksbyMaxie:780992714463510530> {}x = 200<:Gold:639484869809930251> Per piece.\n".format(userinfo["trader_planks"])
			list1 += "<:BricksbyMaxie:780999521249263616> {}x = 200<:Gold:639484869809930251> Per piece.\n".format(userinfo["trader_bricks"])
			list1 += "<:IronPlatebyMaxie:781003325675012146> {}x = 250<:Gold:639484869809930251> Per piece.\n".format(userinfo["trader_iron_plates"])			
				
		if userinfo["trader_rarity"] == "Legendary":
			title = "<:Legendary:639425368167809065> Legendary trader!" 
			list1 += "<:Wood:573574660185260042> {}x = 70<:Gold:639484869809930251> Per piece.\n".format(userinfo["trader_wood"])
			list1 += "<:Stone:573574662525550593> {}x = 70<:Gold:639484869809930251> Per piece.\n".format(userinfo["trader_stone"])
			list1 += "<:Metal:573574661108006915> {}x = 80<:Gold:639484869809930251> Per piece. \n".format(userinfo["trader_metal"])
			list1 += "<:PlanksbyMaxie:780992714463510530> {}x = 200<:Gold:639484869809930251> Per piece.\n".format(userinfo["trader_planks"])
			list1 += "<:BricksbyMaxie:780999521249263616> {}x = 200<:Gold:639484869809930251> Per piece.\n".format(userinfo["trader_bricks"])

		if userinfo["trader_rarity"] == "Rare":
			title = "<:Rare:573784880815538186> Rare trader!" 
			list1 += "<:Wood:573574660185260042> {}x = 70<:Gold:639484869809930251> Per piece.\n".format(userinfo["trader_wood"])
			list1 += "<:Stone:573574662525550593> {}x = 70<:Gold:639484869809930251> Per piece.\n".format(userinfo["trader_stone"])
			list1 += "<:Metal:573574661108006915> {}x = 80<:Gold:639484869809930251> Per piece. \n".format(userinfo["trader_metal"])
			list1 += "<:PlanksbyMaxie:780992714463510530> {}x = 200<:Gold:639484869809930251> Per piece.\n".format(userinfo["trader_planks"])

		if userinfo["trader_rarity"] == "Uncommon":
			title = "<:Uncommon:641361853817159685> Uncommon trader!"
			list1 += "<:Wood:573574660185260042> {}x = 70<:Gold:639484869809930251> Per piece.\n".format(userinfo["trader_wood"])
			list1 += "<:Stone:573574662525550593> {}x = 70<:Gold:639484869809930251> Per piece.\n".format(userinfo["trader_stone"])
			list1 += "<:Metal:573574661108006915> {}x = 80<:Gold:639484869809930251> Per piece. \n".format(userinfo["trader_metal"])

		if userinfo["trader_rarity"] == "Common":
			title = "<:Common:573784881012932618> Common trader!" 
			list1 += "<:Wood:573574660185260042> {}x = 70<:Gold:639484869809930251> Per piece.\n".format(userinfo["trader_wood"])
			list1 += "<:Stone:573574662525550593> {}x = 70<:Gold:639484869809930251> Per piece.\n".format(userinfo["trader_stone"])
			list1 += "<:Metal:573574661108006915> {}x = 80<:Gold:639484869809930251> Per piece. \n".format(userinfo["trader_metal"])



		staytime = 600

		curr_time = time.time()
		delta = float(curr_time) - float(userinfo["trader_time"])

		if delta <= staytime and delta > 0:
			seconds = staytime - delta
			m, s = divmod(seconds, 60)
			

			em = discord.Embed(title=title, description=list1 + "\nTraders profit:<:Gold:639484869809930251>" + str(round(userinfo["trader_profit"])) + "\n trader will stay for another " + str(round(m)) + " Minutes and " + str(round(s)) + " Seconds", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
		else:
			em = discord.Embed(title="No trader!", description="type `{}trader find` to find a trader to trade with!".format(ctx.prefix), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)


	
	@_trader.group(name="buy", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _buy(self, ctx, material:str, amount:int):
		"""Buy something from the trader!\nFor example | -trader buy wood 16\nFor iron plates type ironplates or iron_plates"""
		
		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has bought something from the trader")

		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return
		
		
		staytime = 600

		curr_time = time.time()
		delta = float(curr_time) - float(userinfo["trader_time"])

		if delta <= staytime and delta > 0:
			seconds = staytime - delta
			m, s = divmod(seconds, 60)
			
		
			if material == "wood" or material == "Wood" and userinfo["trader_wood"] >= amount:
				if userinfo["trader_wood"] - amount < 0:
					em = discord.Embed(title="Trade incomplete!", description="Trader doesnt have enough <:Wood:573574660185260042> in stock.\n\n trader will stay for another {}  Minutes and {} Seconds".format(str(round(m)), str(round(s))), color=discord.Colour(0xffffff))
					try:
						await ctx.send(embed=em)
						return
					except:
						try:
							await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
							return
						except:
							return
				cost = 70 * amount
				if not int(userinfo["gold"]) >= int(cost):
					neededgold = int(cost) - int(userinfo["gold"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to trade!**".format(neededgold))
					return

				userinfo["gold"] = userinfo["gold"] - cost
				userinfo["wood"] = userinfo["wood"] + amount
				userinfo["trader_wood"] = userinfo["trader_wood"] - amount
				userinfo["trader_profit"] = userinfo["trader_profit"] + cost

				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				em = discord.Embed(title="Trade complete!", description="You bought {} <:Wood:573574660185260042> for {} <:Gold:639484869809930251>\nTrader has {} <:Wood:573574660185260042> left\n\n trader will stay for another {}  Minutes and {} Seconds".format(amount, cost, userinfo["trader_wood"], str(round(m)), str(round(s))), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
					return
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			if material == "wood" or material == "Wood" and userinfo["trader_wood"] <= amount:
				em = discord.Embed(title="Trade incomplete!", description="Trader doesnt have any <:Wood:573574660185260042> left.\n\n trader will stay for another {}  Minutes and {} Seconds".format(str(round(m)), str(round(s))), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
					return
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			if material == "stone" or material == "Stone" and userinfo["trader_stone"] >= amount:
				if userinfo["trader_stone"] - amount < 0:
					em = discord.Embed(title="Trade incomplete!", description="Trader doesnt have enough <:Stone:573574662525550593> in stock.\n\n trader will stay for another {}  Minutes and {} Seconds".format(str(round(m)), str(round(s))), color=discord.Colour(0xffffff))
					try:
						await ctx.send(embed=em)
						return
					except:
						try:
							await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
							return
						except:
							return
				cost = 70 * amount
				if not int(userinfo["gold"]) >= int(cost):
					neededgold = int(cost) - int(userinfo["gold"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to trade!**".format(neededgold))
					return

				userinfo["gold"] = userinfo["gold"] - cost
				userinfo["stone"] = userinfo["stone"] + amount
				userinfo["trader_stone"] = userinfo["trader_stone"] - amount
				userinfo["trader_profit"] = userinfo["trader_profit"] + cost

				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				em = discord.Embed(title="Trade complete!", description="You bought {} <:Stone:573574662525550593> for {} <:Gold:639484869809930251>\nTrader has {} <:Stone:573574662525550593> left!\n\n trader will stay for another {}  Minutes and {} Seconds".format(amount, cost, userinfo["trader_stone"], str(round(m)), str(round(s))), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
					return
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			if material == "stone" or material == "Stone" and userinfo["trader_stone"] <= amount:
				em = discord.Embed(title="Trade incomplete!", description="Trader doesnt have any <:Stone:573574662525550593> left.\n\n trader will stay for another {}  Minutes and {} Seconds".format(str(round(m)), str(round(s))), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
					return
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			if material == "metal" or material == "Metal" and userinfo["trader_metal"] >= amount:
				if userinfo["trader_metal"] - amount < 0:
					em = discord.Embed(title="Trade incomplete!", description="Trader doesnt have enough <:Metal:573574661108006915> in stock.\n\n trader will stay for another {}  Minutes and {} Seconds".format(str(round(m)), str(round(s))), color=discord.Colour(0xffffff))
					try:
						await ctx.send(embed=em)
						return
					except:
						try:
							await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
							return
						except:
							return
				cost = 80 * amount
				if not int(userinfo["gold"]) >= int(cost):
					neededgold = int(cost) - int(userinfo["gold"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to trade!**".format(neededgold))
					return

				userinfo["gold"] = userinfo["gold"] - cost
				userinfo["metal"] = userinfo["metal"] + amount
				userinfo["trader_metal"] = userinfo["trader_metal"] - amount
				userinfo["trader_profit"] = userinfo["trader_profit"] + cost

				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				em = discord.Embed(title="Trade complete!", description="You bought {} <:Metal:573574661108006915> for {} <:Gold:639484869809930251>\nTrader has {} <:Metal:573574661108006915> left!\n\n trader will stay for another {}  Minutes and {} Seconds".format(amount, cost, userinfo["trader_metal"], str(round(m)), str(round(s))), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
					return
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			if material == "metal" or material == "Metal" and userinfo["trader_metal"] <= amount:
				em = discord.Embed(title="Trade incomplete!", description="Trader doesnt have any <:Metal:573574661108006915> left.\n\n trader will stay for another {}  Minutes and {} Seconds".format(str(round(m)), str(round(s))), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
					return
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			if userinfo["trader_rarity"] == "Rare" or userinfo["trader_rarity"] == "Legendary" or userinfo["trader_rarity"] == "Mythical":
				if material == "planks" or material == "Planks" and userinfo["trader_planks"] >= amount:
					if userinfo["trader_planks"] - amount < 0:
						em = discord.Embed(title="Trade incomplete!", description="Trader doesnt have enough <:PlanksbyMaxie:780992714463510530> in stock.\n\n trader will stay for another {}  Minutes and {} Seconds".format(str(round(m)), str(round(s))), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							return
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
								return
							except:
								return
					cost = 200 * amount
					if not int(userinfo["gold"]) >= int(cost):
						neededgold = int(cost) - int(userinfo["gold"])
						await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to trade!**".format(neededgold))
						return

					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["planks"] = userinfo["planks"] + amount
					userinfo["trader_planks"] = userinfo["trader_planks"] - amount
					userinfo["trader_profit"] = userinfo["trader_profit"] + cost

					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

					em = discord.Embed(title="Trade complete!", description="You bought {} <:PlanksbyMaxie:780992714463510530> for {} <:Gold:639484869809930251>\nTrader has {} <:PlanksbyMaxie:780992714463510530> left!\n\n trader will stay for another {}  Minutes and {} Seconds".format(amount, cost, userinfo["trader_planks"], str(round(m)), str(round(s))), color=discord.Colour(0xffffff))
					try:
						await ctx.send(embed=em)
						return
					except:
						try:
							await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
							return
						except:
							return

				if material == "planks" or material == "Planks" and userinfo["trader_planks"] <= amount:
					em = discord.Embed(title="Trade incomplete!", description="Trader doesnt have any <:PlanksbyMaxie:780992714463510530> left.\n\n trader will stay for another {}  Minutes and {} Seconds".format(str(round(m)), str(round(s))), color=discord.Colour(0xffffff))
					try:
						await ctx.send(embed=em)
						return
					except:
						try:
							await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
							return
						except:
							return
			else:
				em = discord.Embed(title="Wrong trader.", description="This trader doesnt sell planks.".format(ctx.prefix), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)



			if userinfo["trader_rarity"] == "Legendary" or userinfo["trader_rarity"] == "Mythical":
				if material == "bricks" or material == "Bricks" and userinfo["trader_bricks"] >= amount:
					if userinfo["trader_bricks"] - amount < 0:
						em = discord.Embed(title="Trade incomplete!", description="Trader doesnt have enough <:BricksbyMaxie:780999521249263616> in stock.\n\n trader will stay for another {}  Minutes and {} Seconds".format(str(round(m)), str(round(s))), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							return
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
								return
							except:
								return
					cost = 200 * amount
					if not int(userinfo["gold"]) >= int(cost):
						neededgold = int(cost) - int(userinfo["gold"])
						await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to trade!**".format(neededgold))
						return

					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["bricks"] = userinfo["bricks"] + amount
					userinfo["trader_bricks"] = userinfo["trader_bricks"] - amount
					userinfo["trader_profit"] = userinfo["trader_profit"] + cost
					
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

					em = discord.Embed(title="Trade complete!", description="You bought {} <:BricksbyMaxie:780999521249263616> for {} <:Gold:639484869809930251>\nTrader has {} <:BricksbyMaxie:780999521249263616> left!\n\n trader will stay for another {}  Minutes and {} Seconds".format(amount, cost, userinfo["trader_bricks"], str(round(m)), str(round(s))), color=discord.Colour(0xffffff))
					try:
						await ctx.send(embed=em)
						return
					except:
						try:
							await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
							return
						except:
							return

				if material == "bricks" or material == "Bricks" and userinfo["trader_bricks"] <= amount:
					em = discord.Embed(title="Trade incomplete!", description="Trader doesnt have any <:BricksbyMaxie:780999521249263616> left.\n\n trader will stay for another {}  Minutes and {} Seconds".format(str(round(m)), str(round(s))), color=discord.Colour(0xffffff))
					try:
						await ctx.send(embed=em)
						return
					except:
						try:
							await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
							return
						except:
							return
			else:
				em = discord.Embed(title="Wrong trader.", description="This trader doesnt sell planks.".format(ctx.prefix), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)


			if userinfo["trader_rarity"] == "Mythical":
				if material == "iron_plates" or material == "Iron_plates" or material == "Iron_Plates" or material == "IronPlates" or material == "Ironplates" or material == "ironplates" and userinfo["trader_iron_plates"] >= amount:
					if userinfo["trader_iron_plates"] - amount < 0:
						em = discord.Embed(title="Trade incomplete!", description="Trader doesnt have enough <:IronPlatebyMaxie:781003325675012146> in stock.\n\n trader will stay for another {}  Minutes and {} Seconds".format(str(round(m)), str(round(s))), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							return
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
								return
							except:
								return
					cost = 250 * amount
					if not int(userinfo["gold"]) >= int(cost):
						neededgold = int(cost) - int(userinfo["gold"])
						await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to trade!**".format(neededgold))
						return

					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["iron_plates"] = userinfo["iron_plates"] + amount
					userinfo["trader_iron_plates"] = userinfo["trader_iron_plates"] - amount
					userinfo["trader_profit"] = userinfo["trader_profit"] + cost

					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

					em = discord.Embed(title="Trade complete!", description="You bought {} <:IronPlatebyMaxie:781003325675012146> for {} <:Gold:639484869809930251>\nTrader has {} <:IronPlatebyMaxie:781003325675012146> left!\n\n trader will stay for another {}  Minutes and {} Seconds".format(amount, cost, userinfo["trader_iron_plates"], str(round(m)), str(round(s))), color=discord.Colour(0xffffff))
					try:
						await ctx.send(embed=em)
						return
					except:
						try:
							await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
							return
						except:
							return

				if material == "iron_plates" or material == "Iron_plates" or material == "Iron_Plates" or material == "IronPlates" or material == "Ironplates" or material == "ironplates" and userinfo["trader_iron_plates"] >= amount:
					em = discord.Embed(title="Trade incomplete!", description="Trader doesnt have any <:IronPlatebyMaxie:781003325675012146> left.\n\n trader will stay for another {}  Minutes and {} Seconds".format(str(round(m)), str(round(s))), color=discord.Colour(0xffffff))
					try:
						await ctx.send(embed=em)
						return
					except:
						try:
							await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
							return
						except:
							return
			else:
				em = discord.Embed(title="Wrong trader.", description="This trader doesnt sell planks.".format(ctx.prefix), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)




		else:
			em = discord.Embed(title="No trader!", description="type `{}trader find` to find a trader to trade with!".format(ctx.prefix), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)

def setup(bot):
	n = trader(bot)
	bot.add_cog(n)