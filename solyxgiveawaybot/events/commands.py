import discord
from discord.ext import commands
import traceback
import os
import time
import asyncio

from utils.db import db

def listeners(bot):
	



	@bot.event
	async def on_command(ctx):
		
		user = ctx.author
		userinfo = db.users.find_one({ "_id": user.id })

		if isinstance(ctx.channel, discord.channel.DMChannel):
			e=discord.Embed(colour=discord.Colour(0xffffff))
			e.set_author(name="Not available in dm's", icon_url=bot.user.avatar_url)
			await user.send(embed=e)
			return

		if userinfo["blacklisted"] == "True":
			em = discord.Embed(title="You have been Blacklisted", description="{} ({}) has been blacklisted from Solyx!\nFor breaking the cooldown limits 10 times!.\n Join the [**Support Server**](https://discord.gg/Nufxs8vRWx) to apply for a blacklist remove.\n\n**You can play again in 30 seconds.**\n Drink some water, Stay hydrated!".format(user, user.id), color=discord.Colour(0xff0000))
			em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560804112548233217.png")
			await ctx.send(embed=em)
			return

		
		
		TIME = 20 # check infractions for the last <TIME> seconds
		LIMIT = 6 # <LIMIT> for cooldown infractions
			
		
		# Blacklist user if the infractions hit the <LIMIT>
		if userinfo["cooldown_infraction"] >= 10:
			if userinfo["blacklisted"] == "True":
				return

		if userinfo["cooldown_infraction"] >= 10:
			if userinfo["blacklisted"] == "True":
				return
			userinfo["blacklisted"] = "True"
			db.users.replace_one({ "_id": user.id }, userinfo)
			print("User got blacklisted",user)
			try:
				em = discord.Embed(title="User blacklisted: {}".format(user), description="{} ({}) has been blacklisted from Solyx automatically!".format(user, user.id), color=discord.Colour(0xff0000))
				em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560804112548233217.png")
				await bot.get_channel(643899016156938260).send(embed=em)
			except:
				pass
			try:
				em = discord.Embed(description="For breaking the cooldown limits 10 times!.\n\nJoin [the support server](https://discord.gg/Nufxs8vRWx) for more info.\n **you can play again in 30 seconds.**\n Drink some water, Stay hydrated!", color=discord.Colour(0xff0000))
				em.set_author(name="You have been blacklisted from Solyx!", icon_url=user.avatar_url)
				em.set_footer(text=message.timestamp.strftime("%d %m %Y %H:%M"))
				await bot.send(embed=em)
			except:
				pass

			await asyncio.sleep(60)
			
			userinfo["cooldown_infraction"] = 0
			userinfo["blacklisted"] = "False"
			db.users.replace_one({ "_id": user.id}, userinfo)
			em = discord.Embed(title="User removed from blacklisted: {}".format(user), description="{} ({}) has been removed from the blacklist by automatic cooldown!".format(user, user.id), color=discord.Colour(0x00ff00))
			em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560804135545602078.png")
			await bot.get_channel(643899016156938260).send(embed=em)
			

		
		

	@bot.event
	async def on_command_error(ctx, error, *args, **kwargs):
		channel = ctx.channel
		if isinstance(error, commands.CheckFailure):
			pass

		elif isinstance(error, commands.NoPrivateMessage):
			e=discord.Embed(colour=discord.Colour(0xffffff))
			e.set_author(name="Not available in dm's", icon_url=bot.user.avatar_url)
			await user.send(embed=e)

		elif isinstance(error, commands.DisabledCommand):
			e=discord.Embed(colour=discord.Colour(0xffffff))
			e.set_author(name="Command Disabled", icon_url=bot.user.avatar_url)
			await channel.send(embed=e)

		elif isinstance(error, commands.CommandOnCooldown):
			user = ctx.author
			userinfo = db.users.find_one({ "_id": user.id })
	
			userinfo["cooldown_infraction"] = userinfo["cooldown_infraction"] + 1
			db.users.replace_one({ "_id": user.id }, userinfo)
			m, s = divmod(error.retry_after, 60)
			h, m = divmod(m, 60)
			if h == 0 and m == 0:
				time = "%d seconds" % (s)
			elif h == 0:
				time = "%d minutes %d seconds" % (m, s)
			else:
				time = "%d hours %d minutes %d seconds" % (h, m, s)
			try:
				cdmsg = await channel.send(":hourglass: **Cooldown:** {}".format(time))
			except:
				return
			try:
				await cdmsg.delete(delay=float(s))
			except:
				return
			return
			
		elif isinstance(error, commands.MissingRequiredArgument):
			msg = ""
			if not ctx.command.usage:
				for x in ctx.command.params:
					if x != "ctx":
						if x != "self":
							if "None" in str(ctx.command.params[x]):
								msg += "[{}] ".format(x)
							else:
								msg += "<{}> ".format(x)
			else:
				msg += ctx.command.usage
			e=discord.Embed(title="Example", description="{}{} {}".format(ctx.prefix, ctx.command, msg), colour=discord.Colour(0xffffff))
			e.set_author(name="{}".format(ctx.command), icon_url=bot.user.avatar_url)
			e.set_footer(text="{}".format(ctx.command.help))
			await channel.send(embed=e)
		elif isinstance(error, commands.CommandNotFound):
			pass

		elif isinstance(error, commands.BotMissingPermissions):
			if bin(error.missing.value).count("1") == 1:  # Only one perm mis
					plural = ""
			else:
				plural = "s"
			e=discord.Embed(description="{error.missing}", colour=discord.Colour(0xffffff))
			e.set_author(name="Missing permission{plural}", icon_url=bot.user.avatar_url)
			await channel.send(embed=e)

		elif isinstance(error, commands.BadArgument):
			msg = ""
			if not ctx.command.usage:
				for x in ctx.command.params:
					if x != "ctx":
						if x != "self":
							if "None" in str(ctx.command.params[x]):
								msg += "[{}] ".format(x)
							else:
								msg += "<{}> ".format(x)
			else:
				msg += ctx.command.usage
			e=discord.Embed(title="Example", description="{}{} {}".format(ctx.prefix, ctx.command, msg), colour=discord.Colour(0xffffff))
			e.set_author(name="{}".format(ctx.command), icon_url=bot.user.avatar_url)
			e.set_footer(text="{}".format(ctx.command.help))
			await channel.send(embed=e)

		elif isinstance(error, commands.CommandInvokeError):
			exception_log = "Exception in command '{}'\n" "".format(ctx.command.qualified_name)
			exception_log += "".join(traceback.format_exception(type(error), error, error.__traceback__))
			bot._last_exception = exception_log
			print("".join(traceback.format_exception(type(error), error, error.__traceback__)))
			e=discord.Embed(description=ctx.command.qualified_name, colour=discord.Colour(0xffffff))
			e.set_author(name="Error", icon_url=bot.user.avatar_url)
			await channel.send(embed=e)