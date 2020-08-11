from cogs.rpgutils.defaults import locationdata, monsterdata, itemdata, skilldata

try:
	import pymongo
	from pymongo import MongoClient
except:
	raise RuntimeError("Can't load pymongo. Do 'pip3 install pymongo'.")

try:
	client = MongoClient()
	db = client['solyx']
except:
	print("Can't load database. Follow instructions on Git/online to install MongoDB.")

def create_location(data):
	default = locationdata(data)

def create_monster(data):
	default = monsterdata(data)

def create_item(data):
	default = weapondata(data)

def create_skill(data):
	default = skilldata(data)
