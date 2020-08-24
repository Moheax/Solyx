import os
import discord
import asyncio
from utils.db import db
from utils.defaults import userdata, titledata, battledata, guilddata
from utils import checks, dataIO
from datetime import datetime
from discord.ext import commands
from utils.dataIO import fileIO
from utils.checks import staff, developer, owner
from random import choice as randchoice
import time
from discord.ext.commands import Bot, has_permissions

class guilds(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_guild_join(self, ctx, guild: discord.Guild):
		# vars
		owner = guild.owner
		guildicon = guild.icon_url
		botavatar = self.bot.user.avatar_url
		solyxlogchannel = self.bot.get_channel('561200838790479873')
		solyxannouncechannel = self.bot.get_channel('559330366142545933')

		await self._create_guild(guild)

		# Try to send message to owner of the new guild
		try:
			em = discord.Embed(color=discord.Colour(0xffffff), description="Here is some useful information:")
			em.add_field(name="Get started", value="**-help** Get more information about a command\n**-commands** Shows all commands\n**-prefix** Set a new prefix for Solyx", inline=True)
			em.add_field(name="Need help?", value="Join the [support guild](https://discord.gg/CVxzCKj) or check out the full documentation on our [website](http://solyx.xyz)!", inline=True)
			em.set_author(name='Thanks for inviting me!', icon_url=guildicon)
			em.set_thumbnail(url=botavatar)
			await ctx.send(owner, embed=em)
		except:
			return

		await asyncio.sleep(1)

		# Send message to the log in the Solyx guild
		embed = discord.Embed(title='🎁 **New guild:** {} 🎁'.format(guild.name), color=discord.Colour(0xffdf00), description='**Members:** {}\n**Owner:** {}'.format(len(guild.members) - 1, guild.owner.name))
		embed.set_thumbnail(url=guildicon)
		await self.solyxlogchannel.send( embed=embed)

		await asyncio.sleep(1)

		# x00th guild message
		if (len(self.bot.guilds) % 100) == 0:
			await ctx.solyxannouncechannel.send( "🎉 Thanks for **{}** guilds! 🎉".format(len(self.bot.guilds)))

	@commands.Cog.listener()
	async def on_guild_remove(self, ctx, guild: discord.Guild):
		db.servers.remove({"_id": "{}".format(guild.id)}, 1)
		owner = guild.owner
		guildicon = guild.icon_url
		botavatar = self.bot.user.avatar_url
		solyxlogchannel = self.bot.get_channel('641274095400648704')
		# Send message to the log in the Solyx guild
		embed = discord.Embed(title='**Server removed:** {}'.format(guild.name), color=discord.Colour(0xff0000), description='**Members:** {}\n**Owner:** {}'.format(len(guild.members) - 1, guild.owner.name))
		embed.set_thumbnail(url=guildicon)
		await self.solyxlogchannel.send(embed=embed)

	@commands.Cog.listener()
	async def on_guild_update(self, before, after):
		guildinfo = db.servers.find_one({ "_id": after.id })
		if (not guildinfo):
			return
		if before.name != after.name:
			guildinfo["name"] = after.name
			db.servers.replace_one({ "_id": after.id }, guildinfo, upsert=True)

	@commands.Cog.listener()
	async def _create_guild(self, guild):
		exists = db.servers.find_one({ "_id": guild.id })
		if not exists:
			data = guilddata(guild)
			db.servers.insert_one(data)

	@commands.Cog.listener()
	async def on_member_join(self, member):
		guild = member.guild
		user = member
		await self._create_user(user)
		await self._create_guild(guild)

		guildinfo = db.servers.find_one({ "_id": guild.id })
		if not guildinfo["joinreward"] == "True":
			return

		if guildinfo["joinreward"] == "True":
			randomjoinreward = randchoice(["keys", "lootbag"])
			guildinfo["joined"].append(user.id)
			db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)


			userinfo = db.users.find_one({ "_id": user.id })
			curr_time = time.time()
			delta = float(curr_time) - float(userinfo["daily_block"])
			# calulate time left
			seconds = 86400 - delta
			if seconds <= 0 or userinfo["daily_block"] == 0:
				userinfo[randomjoinreward] = userinfo[randomjoinreward] + 30
				userinfo["daily_block"] = curr_time
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				await asyncio.sleep(3)
				try:
					if randomjoinreward == "keys":
						joinrewarddescription = "+20 <:Key:573780034355986432>"
					if randomjoinreward == "lootbags":
						joinrewarddescription = "+20 <:Crate:639425690072252426>"
					if randomjoinreward == "gold":
						joinrewarddescription = "+20 <:Gold:639484869809930251>"

					em = discord.Embed(title="Here is a small reward for joining:", description=joinrewarddescription, color=discord.Colour(0xffffff))
					em.set_author(name="Thanks for joining {}!".format(guild.name), icon_url=guildicon)
					em.set_thumbnail(url=botavatar)
					await ctx.send(user, embed=em)
				except:
					return
			else:
				return
			return

	@commands.command(name="language", pass_context=True, no_pm=True, aliases=["lang"])
	@has_permissions(administrator=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def guild_language(self, ctx, language: str):
		"""Select guild language"""
		author = ctx.message.author
		guild = ctx.message.guild
		guildinfo = db.servers.find_one({ "_id": guild.id })
		accepted = ["EN", "en", "english", "English", 
					"NL", "nl", "nederlands", "Nederlands", "dutch", "Dutch",
					"RU", "ru", "russian", "Russian", "русский", "russkiy",
					"ID", "id", "indonesian", "Indonesian", "Indonesia", "indonesia", "bahasa", "Bahasa", "bahasa Indonesia", "Bahasa Indonesia", "Bahasa indonesia", "bahasa indonesia",
					"KR", "kr", "korean", "Korean", "Korea", "korea", "한국어", "한국인"]
		if not language in accepted:
			em = discord.Embed(title="Accepted languages:", description="`English`, `Nederlands`", color=discord.Colour(0xffffff))
			em.set_thumbnail(url=guild.icon_url)
			em.set_footer(text="This feature is still in development, only English fully works currently!")
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
				except:
					return
			return

		if language == "EN" or language == "en" or language == "english" or language == "English":
			selectedlang = "EN"
			flagemoji = ":flag_us:"
		if language == "nl" or language == "NL" or language == "nederlands" or language == "Nederlands" or language == "dutch" or language == "Dutch":
			selectedlang = "NL"
			flagemoji = ":flag_nl:"
		if language == "RU" or language == "ru" or language == "russian" or language == "Russian" or language == "русский" or language == "russkiy":
			selectedlang = "RU"
			flagemoji = ":flag_ru:"
		if language == "DE" or language == "de" or language == "German" or language == "german" or language == "Deutsch" or language == "deutsch":
			selectedlang = "DE"
			flagemoji = ":flag_de:"
		if language == "ID" or language == "id" or language == "Indonesian" or language == "indonesian" or language == "bahasa Indonesia" or language == "Indonesia" or language == "Bahasa Indonesia" or language == "bahasa" or language == "Bahasa":
			selectedlang = "ID"
			flagemoji = ":flag_id:"
		if language == "KR" or language == "kr" or language == "Korean" or language == "korean" or language == "Korea" or language == "korea" or language == "한국어" or language == "한국인":
			selectedlang = "KR"
			flagemoji = ":flag_kr:"

		guildinfo["language"] = selectedlang
		db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)

		em = discord.Embed(title="Language Changed!", description="Language in {} has been set to {}!".format(guild.name, flagemoji), color=discord.Colour(0xffffff))
		em.set_thumbnail(url=guild.icon_url)
		em.set_footer(text="Use the {}language command to change it.".format(ctx.prefix))
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
			except:
				pass

		if not author == guild.owner:
			em2 = discord.Embed(title="Language Changed!", description="{} has set the language to {}.".format(author.name, flagemoji), color=discord.Colour(0xffffff))
			em2.set_thumbnail(url=guild.icon_url)
			em2.set_footer(text="Use the {}language command to change it.".format(ctx.prefix))
			try:
				await ctx.send(guild.owner, embed=em2)
			except:
				pass

	@commands.command(name="joinreward", pass_context=True, no_pm=True, aliases=["jr"])
	@has_permissions(administrator=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def guild_join_reward(self, ctx):
		"""Select guild language"""
		author = ctx.message.author
		guild = ctx.message.guild
		guildinfo = db.servers.find_one({ "_id": guild.id })

		if guildinfo["joinreward"] == "False":
			guildinfo["joinreward"] = "True"
			db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
			em = discord.Embed(title="Join reward enabled!", description="New members will now get a reward for joining {}!".format(guild.name), color=discord.Colour(0xffffff))
			em.set_thumbnail(url=guild.icon_url)
			em.set_footer(text="Use {}joinreward again to disable it.".format(ctx.prefix))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(author, embed=em)
				except:
					return
			return

		if guildinfo["joinreward"] == "True":
			guildinfo["joinreward"] = "False"
			db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
			em = discord.Embed(title="Join reward disabled!", description="New members will no longer get a reward for joining {}!".format(guild.name), color=discord.Colour(0xffffff))
			em.set_thumbnail(url=guild.icon_url)
			em.set_footer(text="Use {}joinreward again to enable it.".format(ctx.prefix))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(author, embed=em)
				except:
					return
			return

	@commands.command(pass_context=True, name="guilds")
	@commands.check(developer)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def _guild_count(self, ctx):
		"""Server count"""
		em = embed = discord.Embed(description="{}".format(len(self.bot.guilds)), colour=discord.Colour(0xffffff))
		em = embed.set_author(name='Solyx guild count', icon_url=self.bot.user.avatar_url)
		try:
			await ctx.send(embed=em)
		except:
			return

	# handles user creation.
	async def _create_user(self, user):
		exists = db.users.find_one({ "_id": user.id })
		if not exists:
			data = userdata(user)
			db.users.insert_one(data)
		await self._create_battle(user) # create battle file when a new user is created
		await self._create_titles(user) # create titles file when a new user is created

	# handles titles creation.
	async def _create_titles(self, user):
		exists = db.titles.find_one({ "_id": user.id })
		if not exists:
			data = titledata(user)
			db.titles.insert_one(data)

	# handles battle creation.
	async def _create_battle(self, user):
		exists = db.battles.find_one({ "_id": user.id })
		if not exists:
			data = battledata(user)
			db.battles.insert_one(data)

def setup(bot):
	n = guilds(bot)
	bot.add_cog(n)