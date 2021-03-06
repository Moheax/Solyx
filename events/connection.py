import datetime
import dbl

def listeners(bot):
	@bot.event
	async def on_connect():
		print("Shard Connected")

	@bot.event
	async def on_disconnect():
		print("Shard Disconnected")

	@bot.event
	async def on_resumed():
		print("Shard Resumed Connection!")

	@bot.event
	async def on_shard_ready(shard_id):
		print("Shard Ready: {}/{}".format(shard_id + 1, bot.shard_count))

	@bot.event
	async def on_ready():
		print("========== Solyx is Fully Operational ==========")
		print("Bot: {}#{}".format(bot.user.name, str(bot.user.discriminator)))
		print("Guilds: {}".format(len(bot.guilds)))
		print("Users: {}".format(len(set(bot.get_all_members()))))
		print("Shards: {}".format(bot.shard_count))
		print("================================================")
		#setattr(bot, "uptime", datetime.datetime.utcnow().timestamp())
	
	@bot.event
	async def on_dbl_vote(data):
		token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQ5NTkyODkxNDA0NTMwNDg0NyIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA1NDgxNzcwfQ.nNyRlcOlF_urWUlEDgMOI4WzVXG45MbZUFVzOsFO7kQ'  # set this to your DBL token
		dblpy = dbl.DBLClient(bot, token)
		print(data) 