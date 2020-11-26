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

class materials(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def saw(self, ctx, amount:int):

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has sawed wod")

		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })
		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return
		if userinfo["sawmill"] == "False":
			em = discord.Embed(description="You have to build a sawmill first!\ntype {}build sawmill".format(ctx.prefix), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		if userinfo["role"] == "Player":
			if amount == 1:
				pass

			if amount == 2 and userinfo["lvl"] >= 100:
				pass

			if amount == 2 and not userinfo["lvl"] >= 100:
				em = discord.Embed(description="Reach level 100+ to saw 2 logs at once!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			if amount == 3 and userinfo["lvl"] >= 200:
				pass

			if amount == 3 and not userinfo["lvl"] >= 200:
				em = discord.Embed(description="Reach level 200+ to saw 2 logs at once!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			if amount >= 4:
				em = discord.Embed(description="You cant saw more then 3 logs!\n Become a patreon to saw more logs!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

		if userinfo["role"] == "patreon2":

			if amount >= 4:
				em = discord.Embed(description="You cant saw more then 3 logs!\n Become a higher tier patreon to saw more logs!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

		if userinfo["role"] == "patreon3":

			if amount >= 5:
				em = discord.Embed(description="You cant saw more then 4 logs!\n Become a higher tier patreon to saw more logs!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return


		if userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":

			if amount >= 6:
				em = discord.Embed(description="You cant saw more then 5 logs!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return


		used_wood = amount * 3
		made_planks = amount * 2


		if userinfo["wood"] < used_wood:
			missing = used_wood - userinfo["wood"]
			em = discord.Embed(title="Not enough materials!", description="You are missing {} wood\n3 wood = 2 planks.".format(missing), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		curr_time = time.time()
		delta = float(curr_time) - float(userinfo["saw_block"])

		cooldowntime = 1200
		

		if userinfo["role"] == "patreon3":
			cooldowntime = 960
		if userinfo["role"] == "patreon4":
			cooldowntime = 600

		if delta >= cooldowntime and delta > 0:

			userinfo["wood"] = userinfo["wood"] - used_wood
			userinfo["planks"] = userinfo["planks"] + made_planks
			userinfo["saw_block"] = curr_time
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title=":carpentry_saw: You sawed some wood!", description="-" + str(used_wood) + " Wood <:Wood:573574660185260042>\n+" + str(made_planks) + "  Planks <:PlanksbyMaxie:780992714463510530>", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
		else:
			# calulate time left
			seconds = cooldowntime - delta
			m, s = divmod(seconds, 60)
			h, m = divmod(m, 60)
			em = discord.Embed(title=":hourglass: You can't saw yet!", description="" + str(round(m)) + " Minutes and " + str(round(s)) + " seconds", color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
				except:
					return

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def mason(self, ctx, amount:int):

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"did some masonry")

		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })
		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return
		if userinfo["masonry"] == "False":
			em = discord.Embed(description="You have to build a masonry first!\ntype {}build masonry".format(ctx.prefix), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		if userinfo["role"] == "Player":
			if amount == 1:
				pass

			if amount == 2 and userinfo["lvl"] >= 100:
				pass

			if amount == 2 and not userinfo["lvl"] >= 100:
				em = discord.Embed(description="Reach level 100+ to make 2 bricks at once!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			if amount == 3 and userinfo["lvl"] >= 200:
				pass

			if amount == 3 and not userinfo["lvl"] >= 200:
				em = discord.Embed(description="Reach level 200+ to make 2 bricks at once!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			if amount >= 4:
				em = discord.Embed(description="You cant make more then 3 bricks!\n Become a patreon to make more bricks!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

		if userinfo["role"] == "patreon2":

			if amount >= 4:
				em = discord.Embed(description="You cant make more then 3 bricks!\n Become a higher tier patreon to make more bricks!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

		if userinfo["role"] == "patreon3":

			if amount >= 5:
				em = discord.Embed(description="You cant make more then 4 bricks!\n Become a higher tier patreon to make more bricks!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return


		if userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":

			if amount >= 6:
				em = discord.Embed(description="You cant make more then 5 bricks!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return


		used_stone = amount * 5
		made_bricks = amount * 4

		if userinfo["stone"] < used_stone:
			missing = used_stone - userinfo["stone"]
			em = discord.Embed(title="Not enough materials!", description="You are missing {} stone\n5 stone = 4 bricks.".format(missing), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		curr_time = time.time()
		delta = float(curr_time) - float(userinfo["mason_block"])

		cooldowntime = 1200
		

		if userinfo["role"] == "patreon3":
			cooldowntime = 960
		if userinfo["role"] == "patreon4":
			cooldowntime = 600

		if delta >= cooldowntime and delta > 0:

			userinfo["stone"] = userinfo["stone"] - used_stone
			userinfo["bricks"] = userinfo["bricks"] + made_bricks
			userinfo["mason_block"] = curr_time
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title=":hammer_pick: You made some bricks!", description="-" + str(used_stone) + " stone <:Stone:573574662525550593>\n+" + str(made_bricks) + "  Bricks <:BricksbyMaxie:780999521249263616>", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
		else:
			# calulate time left
			seconds = cooldowntime - delta
			m, s = divmod(seconds, 60)
			h, m = divmod(m, 60)
			em = discord.Embed(title=":hourglass: You can't mason yet!", description="" + str(round(m)) + " Minutes and " + str(round(s)) + " seconds", color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
				except:
					return

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def smelt(self, ctx, amount:int):

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has smelted")

		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })
		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return
		if userinfo["smeltery"] == "False":
			em = discord.Embed(description="You have to build a smeltery first!\ntype {}build smeltery".format(ctx.prefix), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		if userinfo["role"] == "Player":
			if amount == 1:
				pass

			if amount == 2 and userinfo["lvl"] >= 100:
				pass

			if amount == 2 and not userinfo["lvl"] >= 100:
				em = discord.Embed(description="Reach level 100+ to make 2 iron plates at once!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			if amount == 3 and userinfo["lvl"] >= 200:
				pass

			if amount == 3 and not userinfo["lvl"] >= 200:
				em = discord.Embed(description="Reach level 200+ to make 2 iron plates at once!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			if amount >= 4:
				em = discord.Embed(description="You cant make more then 3 iron plates!\n Become a patreon to make more iron plates!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

		if userinfo["role"] == "patreon2":

			if amount >= 4:
				em = discord.Embed(description="You cant make more then 3 iron plates!\n Become a higher tier patreon to make more iron plates!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

		if userinfo["role"] == "patreon3":

			if amount >= 5:
				em = discord.Embed(description="You cant make more then 4 iron plates!\n Become a higher tier patreon to make more iron plates!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return


		if userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":

			if amount >= 6:
				em = discord.Embed(description="You cant make more then 5 iron plates!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return


		used_metal = amount * 5
		made_iron_plates = amount * 4

		if userinfo["metal"] < used_metal:
			missing = used_metal - userinfo["metal"]
			em = discord.Embed(title="Not enough materials!", description="You are missing {} metal\n5 metal = 4 iron plates.".format(missing), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		curr_time = time.time()
		delta = float(curr_time) - float(userinfo["smelt_block"])

		cooldowntime = 1200
		

		if userinfo["role"] == "patreon3":
			cooldowntime = 960
		if userinfo["role"] == "patreon4":
			cooldowntime = 600

		if delta >= cooldowntime and delta > 0:

			userinfo["metal"] = userinfo["metal"] - used_metal
			userinfo["iron_plates"] = userinfo["iron_plates"] + made_iron_plates
			userinfo["smelt_block"] = curr_time
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title=":hammer:  You made some iron plates!", description="-" + str(used_metal) + " metal <:Metal:573574661108006915>\n+" + str(made_iron_plates) + "  Iron plates <:IronPlatebyMaxie:781003325675012146>", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
		else:
			# calulate time left
			seconds = cooldowntime - delta
			m, s = divmod(seconds, 60)
			h, m = divmod(m, 60)
			em = discord.Embed(title=":hourglass: You can't smelt yet!", description="" + str(round(m)) + " Minutes and " + str(round(s)) + " seconds", color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
				except:
					return

def setup(bot):
	n = materials(bot)
	bot.add_cog(n)