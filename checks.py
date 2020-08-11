import discord
from discord.ext import commands, tasks
from utils.db import db
from utils.defaults import userdata

def staff(ctx):
	userinfo = db.users.find_one({ "_id": ctx.author.id })
	if not userinfo:
			data = userdata(ctx.author.id)
			db.users.insert_one(data)
			return
	return userinfo["role"] in ["Owner", "Developer", "Staff"]

def developer(ctx):
	userinfo = db.users.find_one({ "_id": ctx.author.id })
	if not userinfo:
			data = userdata(ctx.author.id)
			db.users.insert_one(data)
			return
	return userinfo["role"] in ["Owner", "Developer"]

def owner(ctx):
	return ctx.author.id == 123468845749895170

"""@commands.check(developer)
# Check against your own function that returns those able to use your command

@commands.has_role("name") 
# Check if member has a role with the name "name"

@commands.bot_has_role("name") 
# As above, but for the bot itself.

@commands.has_any_role("role1","foo","bar") 
# Check if user has any of the roles with the names "role1", "foo", or "bar"

@commands.bot_has_any_role("role1","foo","bar") 
# As above, but for the bot itself

@commands.has_permissions(**perms) 
# Check if user has any of a list of passed permissions 
#  e.g. ban_members=True administrator=True

@commands.bot_has_permissions(**perms)
# As above, but for the bot itself.

from discord.ext.commands.cooldowns import BucketType
@commands.cooldown(rate,per,BucketType) 
# Limit how often a command can be used, (num per, seconds, BucketType)
# BucketType can be BucketType.default, user, server, or channel

@commands.guild_only()
# Rewrite Only: Command cannot be used in private messages. (Replaces no_pm=True)

@commands.is_owner()
# Rewrite Only: Command can only be used by the bot owner.

@commands.is_nsfw()
# Rewrite Only: Command can only be used in NSFW channels"""