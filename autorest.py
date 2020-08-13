import discord
import random
import datetime
from random import choice as randchoice
from discord.ext import commands
import asyncio
from utils.dataIO import fileIO
from utils.db import db
from utils.defaults import userdata, titledata, raiddata, battledata, guilddata


class autorest(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def rest_add_hp(self):
		while self is self.bot.get_cog("autorest"):
			for restinfo in db.users.find({}):
				idowo = restinfo["_id"]
				if not restinfo["health"] >= 100:
					randomhpgain = random.randint(1, 3)

					if restinfo["health"] + randomhpgain > 100:
						restinfo["health"] = 100
					else:
						restinfo["health"] = restinfo["health"] + randomhpgain
					db.users.replace_one({ "_id": idowo }, restinfo, upsert=True)

					now = datetime.datetime.now()

					current_time = now.strftime("%H:%M:%S")

					print(current_time+" | Added "+str(randomhpgain),"health to users!")
				
			await asyncio.sleep(60)


def setup(bot):
	n = autorest(bot)	
	loop = asyncio.get_event_loop()
	loop.create_task(n.rest_add_hp())
	bot.add_cog(n)