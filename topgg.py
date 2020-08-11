import dbl
import discord
from discord.ext import commands, tasks

from utils.db import db
import asyncio
import logging


class TopGG(commands.Cog):
	"""Handles interactions with the top.gg API"""

	def __init__(self, bot):
		self.bot = bot
		self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQ5NTkyODkxNDA0NTMwNDg0NyIsImJvdCI6dHJ1ZSwiaWF0IjoxNTk2OTg1NTUyfQ.eAogWCDxTv_qYa22RVr7uaQUB6dzWGVxnzRFypDXOcY' # set this to your DBL token
		self.dblpy = dbl.DBLClient(self.bot, self.token, webhook_path='/dblwebhook', webhook_auth='387317544228487168', webhook_port=8080)

	# The decorator below will work only on discord.py 1.1.0+
	# In case your discord.py version is below that, you can use self.bot.loop.create_task(self.update_stats())

	@tasks.loop(minutes=30.0)
	async def update_stats(self):
		"""This function runs every 30 minutes to automatically update your server count"""
		logger.info('Attempting to post server count')
		try:
			await self.dblpy.post_guild_count()
			logger.info('Posted server count ({})'.format(self.dblpy.guild_count()))
		except Exception as e:
			logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

		# if you are not using the tasks extension, put the line below

		await asyncio.sleep(1800)

	@commands.Cog.listener()
	async def on_dbl_vote(self, data):
		logger.info('Received an upvote')
		print(data)
		
		userinfo = db.users.find_one({ "_id": user.id })

		print(user.name+"#"+user.discriminator,"Has Voted!")
		userinfo["voted"] = "True"
		db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
def setup(bot):
	global logger
	logger = logging.getLogger('bot')
	bot.add_cog(TopGG(bot))