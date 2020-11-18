from discord.ext import commands, tasks

import dbl


class TopGG(commands.Cog):
	"""
	This example uses tasks provided by discord.ext to create a task that posts guild count to top.gg every 30 minutes.
	"""
	

	def __init__(self, bot):
		self.bot = bot
		self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQ5NTkyODkxNDA0NTMwNDg0NyIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA1NDgxNzcwfQ.nNyRlcOlF_urWUlEDgMOI4WzVXG45MbZUFVzOsFO7kQ'  # set this to your DBL token
		self.dblpy = dbl.DBLClient(self.bot, self.token)
		self.update_stats.start()
		

	def cog_unload(self):
		self.update_stats.cancel()
	
	def guild_count(self):
		# Gets the guild count from the provided Client object.
		return len(self.bot.guilds)


	@commands.Cog.listener()
	async def get_bot_upvotes(data):
		"""An event that is called whenever someone votes for the bot on top.gg."""
		print("Received an upvote:", "\n", data, sep="")

	@commands.command(pass_context=True, no_pm=True)
	async def voting(self, ctx):
		async def get_bot_upvotes(data):
			"""An event that is called whenever someone votes for the bot on top.gg."""
			print("Received an upvote:", "\n", data, sep="")
	@commands.command(pass_context=True, no_pm=True)
	async def votes(self, ctx):
		
		async def get_bot_upvotes(self, ctx):
			#This function is a coroutine.

		   # Gets information about last 1000 upvotes for your bot on top.gg.

			#.. note::

		   #     This API endpoint is only available to the bot's owner.

		   # Returns
			#=======

			users: list
			print(list)
			#    Users who voted for your bot.
			print("done")
			await self._ensure_bot_user()
			return await self.http.get_bot_upvotes(self.bot_id)

	

	@tasks.loop(minutes=30)
	async def update_stats(self):
		"""This function runs every 30 minutes to automatically update your server count."""
		await self.bot.wait_until_ready()
		try:
			server_count = len(self.bot.guilds) 
			await self.dblpy.post_guild_count(server_count)
			print('Posted server count ({})'.format(server_count))
		except Exception as e:
			print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

def setup(bot):
	bot.add_cog(TopGG(bot))