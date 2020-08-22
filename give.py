import discord
import platform, asyncio, string, operator, textwrap
import random
import os, re, aiohttp
from random import choice as randchoice
from discord.ext import commands
from utils.db import db
from utils.defaults import guilddata, userdata
from utils import checks
from utils.chat_formatting import pagify
from utils.dataIO import fileIO
import math
from utils.checks import staff, developer, owner
try:
	from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageOps, ImageFilter
except:
	raise RuntimeError("Can't load pillow. Do 'pip3 install pillow'.")
try:
	import scipy
	import scipy.misc
	import scipy.cluster
except:
	pass


class give(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group(name="give", pass_context=True, no_pm=True, hidden=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def _give(self, ctx):
		author = ctx.message.author
		authorinfo = db.users.find_one({ "_id": author.id })
		if not authorinfo["role"] in ["Developer", "Staff"]:
			return

		server = ctx.guild
		channel = ctx.channel
		servercolor = ctx.author.color

		msg = ""
		if ctx.invoked_subcommand is None:
			for x in ctx.command.all_commands:
				if x not in ctx.command.all_commands[x].aliases:
					if not ctx.command.all_commands[x].hidden:
						msg += f"`{ctx.prefix}{ctx.command.name} {x}` - {ctx.command.all_commands[x].help} \n"
			embed=discord.Embed(colour=servercolor)
			embed.set_author(name=ctx.command.name, icon_url=ctx.author.avatar_url)
			embed.add_field(name="Subcommands", value=msg, inline=False)
			
			try:
				await ctx.send(embed=embed)
			except:
				return
		return

	
	@_give.group(name="role", pass_context=True, no_pm=True)
	@commands.check(developer)
	async def _set_role(self, ctx):
		author = ctx.message.author
		authorinfo = db.users.find_one({ "_id": author.id })
		if not authorinfo["role"] in ["Developer", "Staff"]:
			return

		em = discord.Embed(title="Give someone a new role", description="player / donator / developer / staff", color=discord.Colour(0xffffff))
		em.set_footer(text="-give role [role] [user]")
		await ctx.send(embed=em)

	
	@_set_role.command(name="player", pass_context=True)
	@commands.check(developer)
	async def set_role_player(self, ctx, user: discord.Member):
		author = ctx.message.author
		authorinfo = db.users.find_one({ "_id": author.id })
		if not authorinfo["role"] == "Developer" or not authorinfo["role"] == "Staff":
			return

		userinfo = db.users.find_one({ "_id": user.id })
		role = "Player"
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send("That user doesn't play yet... D:")
			return
		else:
			userinfo["role"] = role
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Done", description="Changed {}'s role to {}.".format(user.mention, role), color=discord.Colour(0xffffff))
			em.set_footer(text="{} ({})".format(user.name, user.id))
			await ctx.send(embed=em)

			em = discord.Embed(title="Role given: {}".format(role), description="{} ({}) got the {} role from {} ({})!".format(user, user.id, role, author.mention, author.id), color=discord.Colour(0xff0000))
			em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560809103346368522.png")
			await ctx.send(self.bot.get_channel('643899016156938260'), embed=em)

	
	@_set_role.command(name="donator", pass_context=True)
	@commands.check(developer)
	async def set_role_donator(self, ctx, user: discord.Member):
		author = ctx.message.author
		authorinfo = db.users.find_one({ "_id": author.id })
		if not authorinfo["role"] in ["Developer", "Staff"]:
			return

		userinfo = db.users.find_one({ "_id": user.id })
		role = "Donator"
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send("That user doesn't play yet... D:")
			return
		else:
			userinfo["role"] = role
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Done", description="Changed {}'s role to {}.".format(user.mention, role), color=discord.Colour(0xffffff))
			em.set_footer(text="{} ({})".format(user.name, user.id))
			await ctx.send(embed=em)

			em = discord.Embed(title="Role given: {}".format(role), description="{} ({}) got the {} role from {} ({})!".format(user, user.id, role, author.mention, author.id), color=discord.Colour(0xff0000))
			em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560809103346368522.png")
			await ctx.send(self.bot.get_channel('643899016156938260'), embed=em)

	
	@_set_role.command(name="subscriber", pass_context=True)
	@commands.check(developer)
	async def set_role_subscriber(self, ctx, user: discord.Member):
		author = ctx.message.author
		authorinfo = db.users.find_one({ "_id": author.id })
		if not authorinfo["role"] == "Subscriber":
			return

		userinfo = db.users.find_one({ "_id": user.id })
		role = "Subscriber"
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send("That user doesn't play yet... D:")
			return
		else:
			userinfo["role"] = role
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Done", description="Changed {}'s role to {}.".format(user.mention, role), color=discord.Colour(0xffffff))
			em.set_footer(text="{} ({})".format(user.name, user.id))
			await ctx.send(embed=em)

			em = discord.Embed(title="Role given: {}".format(role), description="{} ({}) got the {} role from {} ({})!".format(user, user.id, role, author.mention, author.id), color=discord.Colour(0xff0000))
			em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560809103346368522.png")
			await ctx.send(self.bot.get_channel('643899016156938260'), embed=em)

	
	@_set_role.command(name="developer", pass_context=True)
	@commands.check(developer)
	
	async def set_role_developer(self, ctx, user: discord.Member):
		author = ctx.message.author
		channel = ctx.message.channel
		userinfo = db.users.find_one({ "_id": user.id })
		role = "Developer"
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send("That user doesn't play yet... D:")
			return
		else:
			userinfo["role"] = role
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Done", description="Changed {}'s role to {}.".format(user.mention, role), color=discord.Colour(0xffffff))
			em.set_footer(text="{} ({})".format(user.name, user.id))
			await ctx.send(embed=em)

			em = discord.Embed(title="Role given: {}".format(role), description="{} ({}) got the {} role from {} ({})!".format(user, user.id, role, author.mention, author.id), color=discord.Colour(0xff0000))
			em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560809103346368522.png")
			await ctx.send(self.bot.get_channel('643899016156938260'), embed=em)


	@_set_role.command(name="staff", pass_context=True)
	@commands.check(developer)
	async def set_role_staff(self, ctx, user: discord.Member):
		author = ctx.message.author
		channel = ctx.message.channel
		userinfo = db.users.find_one({ "_id": user.id })
		role = "Staff"
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send("That user doesn't play yet... D:")
			return
		else:
			userinfo["role"] = role
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Done", description="Changed {}'s role to {}.".format(user.mention, role), color=discord.Colour(0xffffff))
			em.set_footer(text="{} ({})".format(user.name, user.id))
			await ctx.send(embed=em)

			em = discord.Embed(title="Role given: {}".format(role), description="{} ({}) got the {} role from {} ({})!".format(user, user.id, role, author.mention, author.id), color=discord.Colour(0xff0000))
			em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560809103346368522.png")
			await ctx.send(self.bot.get_channel('643899016156938260'), embed=em)

	
	@_give.command(name="crate", pass_context=True)
	@commands.check(developer)
	async def give_crate(self, ctx, user: discord.Member, amount: int):
		author = ctx.message.author
		authorinfo = db.users.find_one({ "_id": author.id })
		if not authorinfo["role"] in ["Developer", "Staff"]:
			return

		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send("That user doesn't play yet... D:")
			return
		else:
			userinfo["lootbag"] = userinfo["lootbag"] + amount
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Done", description="Gave {} {} <:Lootbag:573575192224464919>".format(user.mention, amount), color=discord.Colour(0xffffff))
			em.set_footer(text="{} | {}".format(user.name, user.id))
			await ctx.send(embed=em)

			em = discord.Embed(title="Crates given: {}".format(amount), description="{} ({}) got {} crates from {} ({})!".format(user, user.id, amount, author.mention, author.id), color=discord.Colour(0xff0000))
			em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560809103346368522.png")
			await ctx.send(self.bot.get_channel('643899016156938260'), embed=em)

	
	@_give.command(name="gold", pass_context=True, aliases=["money"])
	@commands.check(developer)
	async def give_gold(self, ctx, user: discord.Member, amount: int):
		author = ctx.message.author
		authorinfo = db.users.find_one({ "_id": author.id })
		if not authorinfo["role"] in ["Developer", "Staff"]:
			return

		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send("That user doesn't play yet... D:")
			return
		else:
			userinfo["gold"] = userinfo["gold"] + amount
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Done", description="Gave {} {} <:Gold:639484869809930251>".format(user.mention, amount), color=discord.Colour(0xffffff))
			em.set_footer(text="{} | {}".format(user.name, user.id))
			await ctx.send(embed=em)

			em = discord.Embed(title="Gold given: {}".format(amount), description="{} ({}) got {} gold from {} ({})!".format(user, user.id, amount, author.mention, author.id), color=discord.Colour(0xff0000))
			em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560809103346368522.png")
			await ctx.send(self.bot.get_channel('643899016156938260'), embed=em)

	
	@_give.command(name="key", pass_context=True, aliases=["keys"])
	@commands.check(developer)
	async def give_key(self, ctx, user: discord.Member, amount: int):
		author = ctx.message.author
		authorinfo = db.users.find_one({ "_id": author.id })
		if not authorinfo["role"] in ["Developer", "Staff"]:
			return

		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send("That user doesn't play yet... D:")
			return
		else:
			userinfo["keys"] = userinfo["keys"] + amount
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Done", description="Gave {} {} <:Key:573780034355986432>".format(user.mention, amount), color=discord.Colour(0xffffff))
			em.set_footer(text="{} | {}".format(user.name, user.id))
			await ctx.send(embed=em)

			em = discord.Embed(title="Keys given: {}".format(amount), description="{} ({}) got {} keys from {} ({})!".format(user, user.id, amount, author.mention, author.id), color=discord.Colour(0xff0000))
			em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560809103346368522.png")
			await ctx.send(self.bot.get_channel('643899016156938260'), embed=em)

	
	@_give.command(name="wood", pass_context=True)
	@commands.check(developer)
	async def give_wood(self, ctx, user: discord.Member, amount: int):
		author = ctx.message.author
		authorinfo = db.users.find_one({ "_id": author.id })
		if not authorinfo["role"] in ["Developer", "Staff"]:
			return

		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send("That user doesn't play yet... D:")
			return
		else:
			userinfo["wood"] = userinfo["wood"] + amount
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Done", description="Gave {} {} wood".format(user.mention, amount), color=discord.Colour(0xffffff))
			em.set_footer(text="{} | {}".format(user.name, user.id))
			await ctx.send(embed=em)

			em = discord.Embed(title="Wood given: {}".format(amount), description="{} ({}) got {} wood from {} ({})!".format(user, user.id, amount, author.mention, author.id), color=discord.Colour(0xff0000))
			em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560809103346368522.png")
			await ctx.send(self.bot.get_channel('643899016156938260'), embed=em)

	
	@_give.command(name="stone", pass_context=True)
	@commands.check(developer)
	async def give_stone(self, ctx, user: discord.Member, amount: int):
		author = ctx.message.author
		authorinfo = db.users.find_one({ "_id": author.id })
		if not authorinfo["role"] in ["Developer", "Staff"]:
			return

		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send("That user doesn't play yet... D:")
			return
		else:
			userinfo["stone"] = userinfo["stone"] + amount
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Done", description="Gave {} {} stone".format(user.mention, amount), color=discord.Colour(0xffffff))
			em.set_footer(text="{} | {}".format(user.name, user.id))
			await ctx.send(embed=em)

			em = discord.Embed(title="Stone given: {}".format(amount), description="{} ({}) got {} stone from {} ({})!".format(user, user.id, amount, author.mention, author.id), color=discord.Colour(0xff0000))
			em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560809103346368522.png")
			await ctx.send(self.bot.get_channel('643899016156938260'), embed=em)

	
	@_give.command(name="metal", pass_context=True)
	@commands.check(developer)
	async def give_metal(self, ctx, user: discord.Member, amount: int):
		author = ctx.message.author
		authorinfo = db.users.find_one({ "_id": author.id })
		if not authorinfo["role"] in ["Developer", "Staff"]:
			return

		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send("That user doesn't play yet... D:")
			return
		else:
			userinfo["metal"] = userinfo["metal"] + amount
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Done", description="Gave {} {} metal".format(user.mention, amount), color=discord.Colour(0xffffff))
			em.set_footer(text="{} | {}".format(user.name, user.id))
			await ctx.send(embed=em)

			em = discord.Embed(title="Metal given: {}".format(amount), description="{} ({}) got {} metal from {} ({})!".format(user, user.id, amount, author.mention, author.id), color=discord.Colour(0xff0000))
			em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560809103346368522.png")
			await ctx.send(self.bot.get_channel('643899016156938260'), embed=em)

	
	@_give.command(name="hp", pass_context=True, aliases=["potion"])
	@commands.check(developer)
	async def give_hp(self, ctx, user: discord.Member, amount: int):
		author = ctx.message.author
		authorinfo = db.users.find_one({ "_id": author.id })
		if not authorinfo["role"] in ["Developer", "Staff"]:
			return

		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send("That user doesn't play yet... D:")
			return
		else:
			userinfo["hp_potions"] = userinfo["hp_potions"] + amount
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Done", description="Gave {} {} <:HealingPotion:573577125064605706>".format(user.mention, amount), color=discord.Colour(0xffffff))
			em.set_footer(text="{} | {}".format(user.name, user.id))
			await ctx.send(embed=em)

			em = discord.Embed(title="Healing Potions given: {}".format(amount), description="{} ({}) got {} healing potions from {} ({})!".format(user, user.id, amount, author.mention, author.id), color=discord.Colour(0xff0000))
			em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560809103346368522.png")
			await ctx.send(self.bot.get_channel('643899016156938260'), embed=em)

	
	@_give.command(name="level", pass_context=True, aliases=["lvl"])
	@commands.check(developer)
	async def give_lvl(self, ctx, user: discord.Member, amount: int):
		author = ctx.message.author
		authorinfo = db.users.find_one({ "_id": author.id })
		if not authorinfo["role"] in ["Developer", "Staff"]:
			return

		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send("That user doesn't play yet... D:")
			return
		else:
			userinfo["lvl"] = userinfo["lvl"] + amount
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Done", description="Gave {} {} :chart_with_upwards_trend:".format(user.mention, amount), color=discord.Colour(0xffffff))
			em.set_footer(text="{} | {}".format(user.name, user.id))
			await ctx.send(embed=em)

			em = discord.Embed(title="Levels given: {}".format(amount), description="{} ({}) got {} levels from {} ({})!".format(user, user.id, amount, author.mention, author.id), color=discord.Colour(0xff0000))
			em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560809103346368522.png")
			await ctx.send(self.bot.get_channel('643899016156938260'), embed=em)

	
	@_give.command(name="title", pass_context=True)
	@commands.check(developer)
	async def give_title(self, ctx, user: discord.Member, *, title):
		author = ctx.message.author
		authorinfo = db.users.find_one({ "_id": author.id })
		if not authorinfo["role"] == "Developer":
			return

		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send("That user doesn't play yet... D:")
			return
		else:
			titlesinfo = db.titles.find_one({ "_id": user.id })
			titlesinfo["titles_list"].append(title)
			titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
			db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
			em = discord.Embed(title="The Developer Gave You A Special Title!", description=title, color=discord.Colour(0x00ff00))
			try:
				await ctx.send(user, embed=em)
			except:
				await ctx.send(embed=em)
			em = discord.Embed(title="Done", description="Gave {} the title `{}`.".format(user.mention, title), color=discord.Colour(0xffffff))
			em.set_footer(text="{} | {}".format(user.name, user.id))
			await ctx.send(embed=em)

			em = discord.Embed(title="Title given: {}".format(title), description="{} ({}) got {} title from {} ({})!".format(user, user.id, title, author.mention, author.id), color=discord.Colour(0xff0000))
			em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560809103346368522.png")
			await ctx.send(self.bot.get_channel('643899016156938260'), embed=em)

	
	@_give.group(name="race", pass_context=True, no_pm=True)
	@commands.check(developer)
	async def _set_race(self, ctx):
		author = ctx.message.author
		authorinfo = db.users.find_one({ "_id": author.id })
		if not authorinfo["role"] == "Developer":
			return

		em = discord.Embed(title="Give someone a new race", description="human / elf / orc", color=discord.Colour(0xffffff))
		em.set_footer(text="-give race [race] [user]")
		await ctx.send(embed=em)

	
	@_set_race.command(name="human", pass_context=True)
	@commands.check(developer)
	async def set_race_human(self, ctx, user: discord.Member):
		author = ctx.message.author
		authorinfo = db.users.find_one({ "_id": author.id })
		if not authorinfo["role"] == "Developer":
			return

		userinfo = db.users.find_one({ "_id": user.id })
		race = "Human"
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send("That user doesn't play yet... D:")
			return
		else:
			userinfo["race"] = race
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Done", description="Changed {}'s race to {}.".format(user.mention, race), color=discord.Colour(0xffffff))
			em.set_footer(text="{} | {}".format(user.name, user.id))
			await ctx.send(embed=em)

	
	@_set_race.command(name="elf", pass_context=True)
	@commands.check(developer)
	async def set_race_elf(self, ctx, user: discord.Member):
		author = ctx.message.author
		authorinfo = db.users.find_one({ "_id": author.id })
		if not authorinfo["role"] == "Developer":
			return

		userinfo = db.users.find_one({ "_id": user.id })
		race = "Elf"
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send("That user doesn't play yet... D:")
			return
		else:
			userinfo["race"] = race
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Done", description="Changed {}'s race to {}.".format(user.mention, race), color=discord.Colour(0xffffff))
			em.set_footer(text="{} | {}".format(user.name, user.id))
			await ctx.send(embed=em)

	
	@_set_race.command(name="orc", pass_context=True)
	@commands.check(developer)
	async def set_race_orc(self, ctx, user: discord.Member):
		author = ctx.message.author
		authorinfo = db.users.find_one({ "_id": author.id })
		if not authorinfo["role"] == "Developer":
			return

		userinfo = db.users.find_one({ "_id": user.id })
		race = "Orc"
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send("That user doesn't play yet... D:")
			return
		else:
			userinfo["race"] = race
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Done", description="Changed {}'s race to {}.".format(user.mention, race), color=discord.Colour(0xffffff))
			em.set_footer(text="{} | {}".format(user.name, user.id))
			await ctx.send(embed=em)

def setup(bot):
	bot.add_cog(give(bot))