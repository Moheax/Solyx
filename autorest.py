import asyncio
import random

import discord
from discord.ext import commands
import datetime
from utils.db import db


class autorest(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def rest_add_hp(self):
		while self is self.bot.get_cog("autorest"):
			users = db.users.count()
			message = "-help | " + str(round(users)) + " Users"
			activity = discord.Game(name=message)
			await self.bot.change_presence(status=discord.Status.online, activity=activity)

			for restinfo in db.users.find({}):
				idowo = restinfo["_id"]

				if not restinfo["health"] >= restinfo["MaxHealth"]:
					randomhpgain = random.randint(1, 3)

					if restinfo["health"] + randomhpgain > restinfo["MaxHealth"]:
						restinfo["health"] = restinfo["MaxHealth"]
					else:
						restinfo["health"] = restinfo["health"] + randomhpgain
					db.users.replace_one({"_id": idowo}, restinfo, upsert=True)
					

			await asyncio.sleep(60)


def setup(bot):
	n = autorest(bot)
	loop = asyncio.get_event_loop()
	loop.create_task(n.rest_add_hp())
	bot.add_cog(n)
