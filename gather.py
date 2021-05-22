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
from cogs.guild import _guild_mission_check
from cogs.quests import _quest_check

# All the positive ones and their rewards!
fishables = {
	":fish:": 5,
	":tropical_fish:": 10,
	":blowfish:": 4,
	":prayer_beads:": 15,
	":key2:": 2,
	":paperclip:": 2,
	":potato:": 2
}
# All the extra items
extras = {
	":wastebasket:": 10,
	":crab:": 5
}

def get_reply(user, item):
	if item in fishables:
		reward = fishables[item]
		return (":fishing_pole_and_fish: **| "+ (user.name) + " , you caught " + item + "!** +"+str(reward)+" <:Gold:639484869809930251>")
	elif item in extras:
		penalty = extras[item]
		if item == ":wastebasket:":
			return (":fishing_pole_and_fish: **|"+ (user.name) + ", your line broke when you caught " + item + "!**  -"+str(penalty)+"<:Gold:639484869809930251>")
		elif item == ":crab:":
			return (":fishing_pole_and_fish: **|"+ (user.name) + ", you caught " + item + " but it pinched your nose!**  -"+str(penalty)+"<:Gold:639484869809930251>")
	else:
		return (":fishing_pole_and_fish: **| Uh-oh! "+ (user.name) + " failed to catch anything!**")


class gather(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 1, commands.BucketType.user)
	async def fish(self, ctx):

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has fished")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		if userinfo["gold"] < 10:
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["gather"]["fish"]["notenoughgold"]["translation"])
			return

		if userinfo["questname"] == "Gathering Fish I":
			userinfo["questprogress"] = userinfo["questprogress"] + 1
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
			if userinfo["questprogress"] >= 5:
				await _quest_check(self, ctx, user)
			pass
	

		all_items = list(fishables.keys()) + list(extras.keys())
		result = randchoice(all_items)
		reply = get_reply(user, result)

		if result in fishables:
			await ctx.send(reply)
			amount = fishables[result]
			userinfo["gold"] += amount
		elif result in extras:
			await ctx.send(reply)
			amount = extras[result]
			userinfo["gold"] -= amount
		else:
			return
		db.users.replace_one({ "_id": user.id }, userinfo)


	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def mine(self, ctx):

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has mined")

		mined_metal = random.randint(0, 2)
		mined_rock = random.randint(1, 5)

		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return
		if userinfo["pickaxelvl"] == 0:
			userinfo["pickaxelvl"] = 1
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		if userinfo["pickaxelvl"] == 2:
			mined_metal = random.randint(2, 4)
			mined_rock = random.randint(3, 7)
		if userinfo["pickaxelvl"] == 3:
			mined_metal = random.randint(4, 6)
			mined_rock = random.randint(5, 9)
		if userinfo["pickaxelvl"] == 4:
			mined_metal = random.randint(6, 8)
			mined_rock = random.randint(7, 11)
		if userinfo["pickaxelvl"] == 5:
			mined_metal = random.randint(8, 10)
			mined_rock = random.randint(9, 13)
		if userinfo["pickaxelvl"] == 6:
			mined_metal = random.randint(10, 12)
			mined_rock = random.randint(11, 15)
		if userinfo["pickaxelvl"] == 7:
			mined_metal = random.randint(11, 14)
			mined_rock = random.randint(12, 17)
		if userinfo["pickaxelvl"] == 8:
			mined_metal = random.randint(12, 16)
			mined_rock = random.randint(13, 19)
		if userinfo["pickaxelvl"] == 9:
			mined_metal = random.randint(13, 18)
			mined_rock = random.randint(14, 21)
		if userinfo["pickaxelvl"] == 10:
			mined_metal = random.randint(14, 20)
			mined_rock = random.randint(15, 23)


	

		curr_time = time.time()
		delta = float(curr_time) - float(userinfo["mine_block"])

		cooldowntime = 600
		

		if userinfo["role"] == "patreon3":
			cooldowntime = 480
		if userinfo["role"] == "patreon4":
			cooldowntime = 300

		if delta >= cooldowntime and delta > 0:

			try:
				mission = "Collect 160 stone"
				add = mined_rock
				await _guild_mission_check(self, user, mission, guild, add)
			except:
				print("Error while trying to log guild mission" + guildinfo["mission"] + "for: " + user.name + " (" + user.id + ") Guild leader id: " + guild.id)
				pass

			try:
				mission = "Collect 120 metal"
				add = mined_metal
				await _guild_mission_check(self, user, mission, guild, add)
			except:
				print("Error while trying to log guild mission" + guildinfo["mission"] + "for: " + user.name + " (" + user.id + ") Guild leader id: " + guild.id)
				pass

			if userinfo["questname"] == "Gathering Metal I":
				userinfo["questprogress"] = userinfo["questprogress"] + mined_metal
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
				if userinfo["questprogress"] >= 2:
					await _quest_check(self, ctx, user)
				pass
	
			if userinfo["questname"] == "Gathering Stone I":
				userinfo["questprogress"] = userinfo["questprogress"] + mined_rock
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
				if userinfo["questprogress"] >= 5:
					await _quest_check(self, ctx, user)
				pass

			userinfo["metal"] = userinfo["metal"] + mined_metal
			userinfo["stone"] = userinfo["stone"] + mined_rock
			userinfo["mine_block"] = curr_time
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="<:Pickaxe:573574740640530471> You mined a rock!", description="+" + str(mined_rock) + " Stone <:Stone:573574662525550593>\n+" + str(mined_metal) + "  Metal <:Metal:573574661108006915>", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
		else:
			# calulate time left
			seconds = cooldowntime - delta
			m, s = divmod(seconds, 60)
			em = discord.Embed(title=":hourglass: You can't mine yet!", description="" + str(round(m)) + " Minutes and " + str(round(s)) + " seconds", color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
				except:
					return

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def chop(self, ctx):
		
		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has chopped wood")

		chopped = random.randint(1, 5)

		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		if userinfo["axelvl"] == 0:
			userinfo["axelvl"] = 1
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		if userinfo["axelvl"] == 2:
			chopped = random.randint(3, 7)
		if userinfo["axelvl"] == 3:
			chopped = random.randint(5, 9)
		if userinfo["axelvl"] == 4:
			chopped = random.randint(7, 11)
		if userinfo["axelvl"] == 5:
			chopped = random.randint(9, 13)
		if userinfo["axelvl"] == 6:
			chopped = random.randint(11, 15)
		if userinfo["axelvl"] == 7:
			chopped = random.randint(12, 17)
		if userinfo["axelvl"] == 8:
			chopped = random.randint(13, 19)
		if userinfo["axelvl"] == 9:
			chopped = random.randint(14, 21)
		if userinfo["axelvl"] == 10:
			chopped = random.randint(15, 23)


		
		

		curr_time = time.time()
		delta = float(curr_time) - float(userinfo["chop_block"])


		cooldowntime = 600
		

		if userinfo["role"] == "patreon3":
			cooldowntime = 480
		if userinfo["role"] == "patreon4":
			cooldowntime = 300


		if delta >= cooldowntime and delta > 0:

			try:
				mission = "Collect 200 wood"
				add = chopped
				await _guild_mission_check(self, user, mission, guild, add)
			except:
				print("Error while trying to log guild mission" + guildinfo["mission"] + "for: " + user.name + " (" + user.id + ") Guild leader id: " + guild.id)
				pass
		
			if userinfo["questname"] == "Gathering Wood I":
				userinfo["questprogress"] = userinfo["questprogress"] + chopped
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
				if userinfo["questprogress"] >= 5:
					await _quest_check(self, ctx, user)
				pass

			userinfo["wood"] = userinfo["wood"] + chopped
			userinfo["chop_block"] = curr_time
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="<:Axe:573574740220969007> You chopped a tree!", description="+" + str(chopped) + " Wood <:Wood:573574660185260042>", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
		else:
			# calulate time left
			seconds = cooldowntime - delta
			m, s = divmod(seconds, 60)
			em = discord.Embed(title=":hourglass: You can't chop yet!", description="" + str(round(m)) + " Minutes and " + str(round(s)) + " seconds", color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
				except:
					return

def setup(bot):
	n = gather(bot)
	bot.add_cog(n)