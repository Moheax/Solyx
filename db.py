try:
  import pymongo
  from pymongo import MongoClient
except:
  raise RuntimeError("Can't load pymongo.")

try:
  client = MongoClient()
  db = client['solyx']
except:
	print("Can't load database.")
