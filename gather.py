import discord
import random
import time
import datetime
from discord.ext import commands
from random import choice as randchoice
# from cogs.economy import NoAccount
from cogs.rpgutils.db import db
from cogs.utils.dataIO import fileIO

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
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def boop(self, ctx):
		print('boop')

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
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

		if userinfo["gold"] < 10:
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["gather"]["fish"]["notenoughgold"]["translation"])
			return

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

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has mined")

		mined_metal = random.randint(0, 2)
		mined_rock = random.randint(1, 5)
		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.guild.find_one({ "_id": guild.id })
	
		curr_time = time.time()
		delta = float(curr_time) - float(userinfo["mine_block"])

		if delta >= 600.0 and delta > 0:

			try:
				mission = "Collect 120 metal"
				await self._guild_mission_check(user, guild, mission, mined_metal)
			except:
				pass

			userinfo["metal"] = userinfo["metal"] + mined_metal
			userinfo["stone"] = userinfo["stone"] + mined_rock
			userinfo["mine_block"] = curr_time
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="<:Pickaxe:573574740640530471> You mined a rock!", description="+" + str(mined_rock) + " Stone <:Stone:573574662525550593>\n+" + str(mined_metal) + "  Metal <:Metal:573574661108006915>", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
		else:
			# calulate time left
			seconds = 600 - delta
			m, s = divmod(seconds, 60)
			h, m = divmod(m, 60)
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
		

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has chopped wood")

		chopped = random.randint(1, 5)
		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.guild.find_one({ "_id": guild.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return
		curr_time = time.time()
		delta = float(curr_time) - float(userinfo["chop_block"])

		if delta >= 600.0 and delta > 0:

			try:
				mission = "Collect 200 wood"
				await self._guild_mission_check(user, guild, mission, chopped)
			except:
				pass

			userinfo["wood"] = userinfo["wood"] + chopped
			userinfo["chop_block"] = curr_time
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="<:Axe:573574740220969007> You chopped a tree!", description="+" + str(chopped) + " Wood <:Wood:573574660185260042>", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
		else:
			# calulate time left
			seconds = 600 - delta
			m, s = divmod(seconds, 60)
			h, m = divmod(m, 60)
			em = discord.Embed(title=":hourglass: You can't chop yet!", description="" + str(round(m)) + " Minutes and " + str(round(s)) + " seconds", color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
				except:
					return

	async def _guild_mission_check(self, user, guild, mission, add):
		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.guild.find_one({ "_id": guild.id })

		if guild == "None":
			return

		if mission == "Collect 200 wood":
			if not guildinfo["mission"] == "Collect 200 wood":
				return
			try:
				guildinfo["missionprogress"] = guildinfo["missionprogress"] + add
				db.guild.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
				return
			except:
				print("Error while trying to log guild mission" + mission + "for: " + user.name + " (" + user.id + ") Guild leader id: " + guild.id)
				return

		elif mission == "Collect 120 metal":
			if not guildinfo["mission"] == "Collect 120 metal":
				return
			try:
				guildinfo["missionprogress"] = guildinfo["missionprogress"] + add
				db.guild.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
				return
			except:
				print("Error while trying to log guild mission" + mission + "for: " + user.name + " (" + user.id + ") Guild leader id: " + guild.id)
				return

		else:
			print(user.name + " (" + user.id + ") from guild with leader id " + guild.id + "managed to check a non-existing mission!")
			return

def setup(bot):
	n = gather(bot)
	bot.add_cog(n)