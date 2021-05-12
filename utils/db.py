try:
  import pymongo
  from pymongo import MongoClient
except:
  raise RuntimeError("Can't load pymongo.")

try:
	#client = MongoClient('mongodb+srv://Max:Max@solyx.7mjw2.mongodb.net/Solyx?retryWrites=true&w=majority')
	#db = client['Solyx']
	client = MongoClient()
	db = client['solyx']

except:
	print("Can't load database.")

	


	