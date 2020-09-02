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
	return ctx.author.id == 387317544228487168



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

def check_permissions(ctx, perms):
	if is_owner_check(ctx):
		return True
	elif not perms:
		return False

	ch = ctx.message.channel
	author = ctx.message.author
	resolved = ch.permissions_for(author)
	return all(getattr(resolved, name, None) == value for name, value in perms.items())

def role_or_permissions(ctx, check, **perms):
	if check_permissions(ctx, perms):
		return True

	ch = ctx.message.channel
	author = ctx.message.author
	if ch.is_private:
		return False # can't have roles in PMs

	role = discord.utils.find(check, author.roles)
	return role is not None

def mod_or_permissions(**perms):
	def predicate(ctx):
		server = ctx.message.guild
		mod_role = settings.get_guild_mod(server).lower()
		admin_role = settings.get_guild_admin(server).lower()
		return role_or_permissions(ctx, lambda r: r.name.lower() in (mod_role,admin_role), **perms)

	return commands.check(predicate)

def admin_or_permissions(**perms):
	def predicate(ctx):
		server = ctx.message.guild
		admin_role = settings.get_guild_admin(server)
		return role_or_permissions(ctx, lambda r: r.name.lower() == admin_role.lower(), **perms)

	return commands.check(predicate)

def serverowner_or_permissions(**perms):
	def predicate(ctx):
		if ctx.message.guild is None:
			return False
		guild = ctx.message.guild
		owner = guild.owner

		if ctx.message.author.id == owner.id:
			return True

		return check_permissions(ctx,perms)
	return commands.check(predicate)

def serverowner():
	return serverowner_or_permissions()

def admin():
	return admin_or_permissions()

def mod():
	return mod_or_permissions()