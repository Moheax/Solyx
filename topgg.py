import dbl
import discord
from discord.ext import commands, tasks

import asyncio
import logging
from utils.db import db

class api(commands.Cog):
	"""Handles interactions with the top.gg API"""

	def __init__(self, bot):
		self.bot = bot
		self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQ5NTkyODkxNDA0NTMwNDg0NyIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA1NDgxNzcwfQ.nNyRlcOlF_urWUlEDgMOI4WzVXG45MbZUFVzOsFO7kQ' # set this to your DBL token
		self.dblpy = dbl.DBLClient(self.bot, self.token, webhook_path='/', webhook_auth='387317544228487168', webhook_port=8080)

	# The decorator below will work only on discord.py 1.1.0+
	# In case your discord.py version is below that, you can use self.bot.loop.create_task(self.update_stats())

	@tasks.loop(minutes=30.0)
	async def update_stats(self):
		"""This function runs every 30 minutes to automatically update your server count"""
		logger.info('Attempting to post server count')
		try:
			await self.dblpy.post_guild_count() + 200
			await self.dblpy.post_shard_count() + 3
			logger.info('Posted server count ({})'.format(self.dblpy.guild_count()))
		except Exception as e:
			logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

		# if you are not using the tasks extension, put the line below

		await asyncio.sleep(1800)


	@commands.Cog.listener()
	async def on_dbl_vote(data):
		"""An event that is called whenever someone votes for the bot on top.gg."""
		userinfo = db.users.find_one({"_id": data['user']})

		# Account check
		if userinfo["class"] == "None" and userinfo["race"] == "None":
			return
		if request.json["isWeekend"] == "True":
			userinfo["voted"] = "weekend"
		else:
			userinfo["voted"] = "True"
		db.users.replace_one({"_id": data['user']}, userinfo, upsert=True)
		logger.info('Received an upvote')
		print(data)
		
		print(f"Received an upvote:\n{data}")

	@commands.Cog.listener()
	async def on_dbl_test(data):
		"""An event that is called whenever someone tests the webhook system for your bot on top.gg."""
		print(f"Received a test upvote:\n{data}")
	@commands.Cog.listener()
	async def on_dbl_vote(self, data):
		
		userinfo = db.users.find_one({"_id": data['user']})

		# Account check
		if userinfo["class"] == "None" and userinfo["race"] == "None":
			return
		if request.json["isWeekend"] == "True":
			userinfo["voted"] = "weekend"
		else:
			userinfo["voted"] = "True"
		db.users.replace_one({"_id": data['user']}, userinfo, upsert=True)
		logger.info('Received an upvote')
		print(data)

def setup(bot):
	global logger
	logger = logging.getLogger('bot')
	bot.add_cog(api(bot))