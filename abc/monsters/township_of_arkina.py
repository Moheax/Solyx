from cogs.rpgutils.calculator import get_level, max_health

class MonsterName:
	"""
	This is what EVERY monster's class should look like.
	Just use this as an example to fill in data for the rest of the monsters
	Each file will have classes for the monsters in that location
	"""
	def __init__(self, userinfo):
		self.location = "Township of Arkina"
		self.base_dmg = 35
		self.base_def = 8
		self.base_health = 60
		self.base_xp_reward = 120
		self.base_gold_reward = 80

		_level = userinfo["enemylvl"]
		if _level and _level != "None":
			self.level = _level
		else:
			max_lvl = 40
			min_lvl = 20
			self.level = get_level(max_lvl, min_lvl, userinfo["level"])

		_health = userinfo["enemyhealth"]
		if _health and _health != "None":
			self.health = _health
		else:
			self.health = max_health(self.base_health, self.level)

	def special(self, userinfo):
		"""
		This will be the special attack, if this monster has any.
		This will be used in apply_attack()
		"""
		return

	def apply_attack(self, userinfo):
		"""
		This is where the monster will apply its attack on userinfo.
		"""
		return