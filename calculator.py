from random import randint

def get_required_xp(level):
	"""
	Calculates required xp for each level. This
	formula scales well, but can be changed, of course.
	"""
	return round(100 * level ** 1.5)

def chance(percentage):
	"""
	percentage is a number between 1 and 100.
	Returns True or False
	"""
	return True if randint(1, 100) <= percentage else False

def max_health(base_health, level):
	"""
	Formula for calculating health, based on base_health and level
	"""
	return round(base_health * level ** 0.5)

def xp_reward(base_reward, level):
	"""
	formula for calculating xp rewards given
	by monsters, based on base_xp_reward and level
	"""
	return round(base_reward * level / 1.5)

def gold_reward(base_reward, level):
	"""
	formulal for calculating gold rewards given
	by monsters, based on base_gold_rewad and level
	"""
	return round(base_reward * level / 2)

def get_level(max, min, userlevel):
	"""
	for getting the level of the monsters, based
	on monster's max/min level, and the user's level
	"""
	if userlevel >= max:
		return max
	elif userlevel <= min:
		return min
	else:
		step = round((max - min) / 3)
		step_a = min + (step * 1)
		step_b = min + (step * 2)
		step_c = min + (step * 3)

		if userlevel <= step_a:
			return round(randint(min, step_a))
		elif userlevel <= step_b:
			return round(randint(step_a, step_b))
		else:
			return round(randint(step_b, step_c))
