import discord
import random

import datetime
from random import choice as randchoice
from discord.ext import commands
from utils.db import db
from utils.defaults import userdata
from utils import checks
import asyncio
from utils.dataIO import fileIO

class quests(commands.Cog):
	def __init__(self, bot):
		self.bot = bot



	async def check_answer_other_user(self, ctx, user, valid_options):
		answer = await self.bot.wait_for_message(author=user, channel=ctx.message.channel)

		if answer.content.lower() in valid_options:
			return answer.content
		elif answer.content in valid_options:
			return answer.content
		elif answer.content.upper() in valid_options:
			return answer.content
		else:
			return #await self.check_answer(ctx, valid_options)  //  This could keep a check loop going



	@commands.command(pass_context=True,aliases=["quest"], no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def quests(self, ctx):
		"""Shows Current quests progress"""

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Checked quests")





		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })

		

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/En.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		if userinfo["questname"] == "Basic A" and userinfo["questprogress"] >= 1:
			oldquest = "Basic A"

			expgain = 20

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience".format(oldquest, expgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			newquest = "Basic B"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Open your Inventory!".format(newquest), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				userinfo["exp"] = 0
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			return

		elif userinfo["questname"] == "Basic B" and userinfo["questprogress"] >= 1:
			oldquest = "Basic B"

			expgain = 20
			goldgain = 20

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold".format(oldquest, expgain, goldgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Basic C"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Start your first fight!".format(newquest), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				userinfo["exp"] = 0
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			return

		elif userinfo["questname"] == "Basic C" and userinfo["questprogress"] >= 1:
			oldquest = "Basic C"

			expgain = 25
			goldgain = 25

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold".format(oldquest, expgain, goldgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Gathering Wood I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Gather 5 Wood!".format(newquest), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				userinfo["exp"] = 0
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			return

		elif userinfo["questname"] == "Gathering Wood I" and userinfo["questprogress"] >= 5:
			oldquest = "Gathering Wood I"

			expgain = 30
			goldgain = 30

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold".format(oldquest, expgain, goldgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Gathering Stone I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Gather 5 Stone!".format(newquest), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				userinfo["exp"] = 0
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			return

		elif userinfo["questname"] == "Gathering Stone I" and userinfo["questprogress"] >= 5:
			oldquest = "Gathering Stone I"

			expgain = 30
			goldgain = 30

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold".format(oldquest, expgain, goldgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Gathering Metal I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Gather 2 Metal!".format(newquest), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				userinfo["exp"] = 0
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			return

		elif userinfo["questname"] == "Gathering Metal I" and userinfo["questprogress"] >= 2:
			oldquest = "Gathering Metal I"

			expgain = 30
			goldgain = 30

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold".format(oldquest, expgain, goldgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Gathering Fish I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Fish 5 times!".format(newquest), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				userinfo["exp"] = 0
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			return

		elif userinfo["questname"] == "Gathering Fish I" and userinfo["questprogress"] >= 5:
			oldquest = "Gathering Fish I"

			expgain = 30
			goldgain = 30

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold".format(oldquest, expgain, goldgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Wood Trader I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Sell 10 Wood!".format(newquest), color=discord.Colour(0xffffff)) # MAKE WOOD TRADER I 
			await ctx.send(embed=em)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				userinfo["exp"] = 0
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			return

		elif userinfo["questname"] == "Wood Trader I" and userinfo["questprogress"] >= 10:
			oldquest = "Wood Trader I"

			expgain = 35
			goldgain = 35
			crategain = 1

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crate".format(oldquest, expgain, goldgain, crategain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Stone Trader I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Sell 10 Stone!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				userinfo["exp"] = 0
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			return
		elif userinfo["questname"] == "Stone Trader I" and userinfo["questprogress"] >= 10:
			oldquest = "Stone Trader I"

			expgain = 35
			goldgain = 35
			crategain = 1

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crate".format(oldquest, expgain, goldgain, crategain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Metal Trader I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Sell 5 Metal!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				userinfo["exp"] = 0
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			return

		elif userinfo["questname"] == "Metal Trader I" and userinfo["questprogress"] >= 5:
			oldquest = "Metal Trader I"

			expgain = 35
			goldgain = 35
			crategain = 1

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crate".format(oldquest, expgain, goldgain, crategain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Health acquisition"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\nBuy 5 Hp potions!\nUse 1 Hp potions".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				userinfo["exp"] = 0
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			return

		elif userinfo["questname"] == "Health acquisition" and userinfo["questpart"] == 2 and userinfo["questprogress"] >= 1:
			oldquest = "Health acquisition"

			expgain = 40
			goldgain = 40
			crategain = 2

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates".format(oldquest, expgain, goldgain, crategain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Unboxing I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Open 10 crates".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				userinfo["exp"] = 0
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				
				
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			return

		elif userinfo["questname"] == "Unboxing I"  and userinfo["questprogress"] >= 10:
			oldquest = "Unboxing I"

			expgain = 45
			goldgain = 45
			crategain = 5

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates".format(oldquest, expgain, goldgain, crategain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Daily I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Collect your daily reward!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				userinfo["exp"] = 0
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				
				
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			return

		elif userinfo["questname"] == "Daily I"  and userinfo["questprogress"] >= 1:


			if len(userinfo["inventory"]) >= 25:
				try:
					em = discord.Embed(description="Full item inventory, you cant finish this quest.", color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				except:
					return
				return


			oldquest = "Daily I"

			expgain = 45
			goldgain = 45
			crategain = 2
			keygain = 2

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys".format(oldquest, expgain, goldgain, crategain, keygain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Equip"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain

			Class = userinfo["class"]

			if Class == "Mage" or Class == "Elementalist" or Class == "Necromancer" or Class == "Developed Necromancer" or Class == "Adequate Elementalist":
				itemobj = {"name": "Training Staff", "type": "staff", "rarity": "Training", "stats_min": 1, "stats_max": 1, "refinement": "Normal", "description": "?!", "image": "None"}

			elif Class == "Paladin" or Class == "Samurai" or Class == "Knight" or Class == "Master Samurai" or Class == "Grand Paladin":
				itemobj = {"name": "Training Sword", "type": "sword", "rarity": "Training", "stats_min": 1, "stats_max": 1, "refinement": "Normal", "description": "?!", "image": "None"}

			elif Class == "Thief" or Class == "Mesmer" or Class == "Rogue" or Class == "High rogue" or Class == "Adept Mesmer":
				itemobj = {"name": "Training Sword", "type": "dagger", "rarity": "Training", "stats_min": 1, "stats_max": 1, "refinement": "Normal", "description": "?!", "image": "None"}

			elif Class == "Archer" or Class == "Ranger" or Class == "Assassin" or Class == "Night Assassin" or Class == "Skilled Ranger":
				itemobj = {"name": "Training Bow", "type": "bow", "rarity": "Training", "stats_min": 1, "stats_max": 1, "refinement": "Normal", "description": "?!", "image": "None"}


			
			userinfo["inventory"].append(itemobj)

			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Equip your training weapon\n Equip your weapon.".format(newquest), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			em = discord.Embed(title="New Quest Item!", description="You recieved your training weapon use it to equip!", color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				userinfo["exp"] = 0
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				
				
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			return
		elif userinfo["questname"] == "Equip"  and userinfo["questpart"] == 2 and userinfo["questprogress"] >= 1:
			oldquest = "Equip"

			expgain = 50
			goldgain = 50
			crategain = 3
			keygain = 3

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys".format(oldquest, expgain, goldgain, crategain, keygain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Vote I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Vote once for solyx to get extra rewards!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				userinfo["exp"] = 0
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				
				
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			return

		elif userinfo["questname"] == "Vote I"  and userinfo["questprogress"] >= 1:
			oldquest = "Vote I"

			expgain = 55
			goldgain = 55
			crategain = 3
			keygain = 3

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys".format(oldquest, expgain, goldgain, crategain, keygain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Fight I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Fight 25 times. NOT MADE YET!!!!!!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				userinfo["exp"] = 0
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				
				
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			return


		else:
			if userinfo["questname"] == "Basic A":
				em = discord.Embed(title="Basic A", description="**Objective**\nTake look at your stats.\nType {}stats".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="Unopend stats", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Basic B":
				em = discord.Embed(title="Basic B", description="**Objective**\nOpen your inventory.\nType {}inv".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="Unopend Inventory", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Basic C":
				em = discord.Embed(title="Basic C", description="**Objective**\nStart your first Fight.\nType {}fight".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="Fight not started.", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Gathering Wood I":
				em = discord.Embed(title="Gathering Wood I", description="**Objective**\nGather 5 wood.\nType {}chop".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/5 Wood collected".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Gathering Stone I":
				em = discord.Embed(title="Gathering Stone I", description="**Objective**\nGather 5 Stone.\nType {}mine".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/5 Stone collected".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Gathering Metal I":
				em = discord.Embed(title="Gathering Metal I", description="**Objective**\nGather 2 Metal.\nType {}mine".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/2 Metal collected".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Gathering Fish I":
				em = discord.Embed(title="Gathering Fish I", description="**Objective**\nFish 5 times.\nType {}fish".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/5 times Fished".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Wood Trader I":
				em = discord.Embed(title="Wood Trader I", description="**Objective**\nSell 10 Wood.\nType {}sell wood <amount> / all".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/10 Wood Sold".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Stone Trader I":
				em = discord.Embed(title="Stone Trader I", description="**Objective**\nSell 10 Stone.\nType {}sell stone <amount> / all".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/10 Stone Sold".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Metal Trader I":
				em = discord.Embed(title="Metal Trader I", description="**Objective**\nSell 10 Metal.\nType {}sell metal <amount> / all".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/5 Metal Sold".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Health acquisition" and  userinfo["questpart"] == 0:
				em = discord.Embed(title="Health acquisition", description="**Objective**\nBuy 5 health potions.\nType {}buy hp <amount>\n\nUse 1 hp potion\nType {}heal".format(ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="Part 1/2\n{}/5 health potions bought".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Health acquisition" and  userinfo["questpart"] == 1:
				userinfo["questprogress"] = 0
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				em = discord.Embed(title="Health acquisition", description="**Objective**\nBuy 5 health potions.\nType {}buy hp <amount>\n\nUse 1 hp potion\nType {}heal".format(ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="Part 2/2\n{}/1 health potions used".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Unboxing I":
				em = discord.Embed(title="Unboxing I ", description="**Objective**\nOpen 10 Crate.\nType {}lb / {}crate".format(ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/10 Crates opened".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Daily I":
				em = discord.Embed(title="Daily I ", description="**Objective**\nCollect your first daily reward.\nType {}daily / {}checkin".format(ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="Daily not collected", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Equip" and  userinfo["questpart"] == 0:
				em = discord.Embed(title="Equip", description="**Objective**\nEquip the training weapon\nType {}equip weapon <number>\n\nEquip your main weapon again.\nType Type {}equip weapon <number>".format(ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="Part 1/2\nTraining Weapon not equipped", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Equip" and  userinfo["questpart"] == 1:
				userinfo["questprogress"] = 0
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				em = discord.Embed(title="Equip", description="**Objective**\nEquip the training weapon\nType {}equip weapon <number>\n\nEquip your main weapon again.\nType Type {}equip weapon <number>".format(ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="Part 2/2\nMain Weapon not equipped", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Fight I":
				em = discord.Embed(title="Fight I Not Made Yet! ", description="**Objective**\Fight 25 times\nType {}Fight".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/25 times fought".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
def setup(bot):
	n = quests(bot)
	bot.add_cog(n)