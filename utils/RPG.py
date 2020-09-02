import calculator as calc


class RPG():
	"""
	This class provides important utility functions for the whole RPG.
	It's NOT a cog and doesn't have any commands, those are all in the subcogs.
	This class will be attached to the bot to make it easier to use the functions
	"""
	def __init__(self, bot):
		self.bot = bot
		self.db = bot.db

	async def handle_level_up(self, userinfo):
		"""
		this will handle everything for the level up, including required xp
		increasing level, sending the "level up!" message and all that.
		Returns the modified userinfo dict
		"""
		return

	def spawn_monster(self, location, userinfo):
		"""
		based on the location and user,
		it will spawn a monster.
		Returns a monster class from cogs.abc.monsters
		"""
		return

	def get_user(self, userinfo):
		"""
		It will return a proper user class from cogs.abc.users
		this will make it WAYYYYYYY easier to deal with userinfo-related stuff
		"""
		return
