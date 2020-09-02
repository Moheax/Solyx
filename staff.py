import discord
from discord.ext import commands
import asyncio
import os, re, aiohttp
from utils.db import db
from utils.defaults import guilddata, userdata
from utils import checks
from discord.ext import commands
from utils.dataIO import fileIO

class staff(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def on_member_ban(self, member):
		guild = member.guild
		userinfo = db.users.find_one({ "_id": member.id })
		if not guild.id == "559328647639728128":
			return
		if userinfo["role"] == "Staff" or userinfo["role"] == "Developer":
			userinfo["role"] = "Player"
			db.users.replace_one({ "_id": member.id }, userinfo, upsert=True)

	async def on_member_remove(self, member):
		guild = member.guild
		userinfo = db.users.find_one({ "_id": member.id })
		if not guild.id == "559328647639728128":
			return
		if userinfo["role"] == "Staff" or userinfo["role"] == "Developer":
			userinfo["role"] = "Player"
			db.users.replace_one({ "_id": member.id }, userinfo, upsert=True)

def setup(bot):
	n = staff(bot)
	bot.add_cog(n)