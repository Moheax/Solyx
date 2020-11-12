import discord
import datetime
from discord.ext import commands

import asyncio

class command(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

# - - - Commands menu - - -
	@commands.command(name="commands", aliases=["commandlist", "cmds"])
	@commands.cooldown(1, 2, commands.BucketType.user)
	async def _commands(self, ctx, *, topic=None):
		"""Commands list"""

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"looked at commands")

		if topic == None:
			em = embed = discord.Embed(description="Click [here](https://solyxbot.webflow.io/commands) for a detailed documentation.", color=discord.Colour(0xffffff))
			em = embed.set_author(name="Solyx Commands:", icon_url=ctx.message.author.avatar_url)
			em = embed.add_field(name="🇦 Getting Started", value="The basics", inline=False)
			em = embed.add_field(name="🇧 Fighting", value="All basic fighting related commands", inline=False)
			em = embed.add_field(name="🇨 Inventory & Items", value="Items, weapons, equip, ...", inline=False)
			em = embed.add_field(name="🇩 Economy", value="Buying, selling, gold, ...", inline=False)
			em = embed.add_field(name="🇪 Guilds", value="Guild related commands", inline=False)
			em = embed.add_field(name="🇫 Battles", value="1v1 battles commands", inline=False)
			em = embed.add_field(name="🇬 Raids", value="Coming soon", inline=False)
			em = embed.add_field(name="🇭 Admin Commands", value="Server administration commands", inline=False)
			em = embed.add_field(name="🇮 Miscellaneous Commands", value="Miscellaneous commands", inline=False)
			em = embed.set_footer(text="Type | -commands <letter> |  to go to that command page!")
			try:
				msg = await ctx.send(embed=em)
			except:
				try:
					await ctx.send("I cound't send the message.")
				except:
					return
				return
		
		elif topic == "A" or topic == "a":
 
			e = discord.Embed(color=discord.Colour(0xffffff))
			e.set_author(name="Getting Started", icon_url=user.avatar_url)
			e.add_field(name="{}tutorial".format(ctx.prefix), value="Learn how to use the bot", inline=True)
			e.add_field(name="{}begin".format(ctx.prefix), value="Create a character to start your adventure!", inline=True)
			await ctx.send(embed=e)
			return

		elif topic == "B" or topic == "b":

			e = discord.Embed(color=discord.Colour(0xffffff))
			e.set_author(name="Fighting", icon_url=user.avatar_url)
			e.add_field(name="{}fight".format(ctx.prefix), value="Fight a monster", inline=True)
			e.add_field(name="{}hp".format(ctx.prefix), value="Check your health", inline=True)
			e.add_field(name="{}heal".format(ctx.prefix), value="Use a healing potion to gain HP", inline=False)
			e.add_field(name="{}exp".format(ctx.prefix), value="Use a experience potion to gain more EXP", inline=False)
			e.add_field(name="{}travel".format(ctx.prefix), value="Go to a new location to fight different monsters", inline=False)
			await ctx.send(embed=e)
			return

		elif topic == "C" or topic == "c":
	
			e = discord.Embed(color=discord.Colour(0xffffff))
			e.set_author(name="Inventory & Items", icon_url=user.avatar_url)
			e.add_field(name="{}inv".format(ctx.prefix), value="Check your inventory", inline=True)
			e.add_field(name="{}stats".format(ctx.prefix), value="See your statistics", inline=True)
			e.add_field(name="{}profile".format(ctx.prefix), value="Show your profile card", inline=False)
			e.add_field(name="{}rank".format(ctx.prefix), value="Show your rank card", inline=False)
			e.add_field(name="{}market".format(ctx.prefix), value="Sell and buy items on the market", inline=False)
			e.add_field(name="{}equip".format(ctx.prefix), value="Equip a weapon or a piece of armor", inline=False)
			e.add_field(name="{}sell".format(ctx.prefix), value="Sell an item", inline=False)
			e.add_field(name="{}crate".format(ctx.prefix), value="Open a crate", inline=False)
			e.add_field(name="{}mine".format(ctx.prefix), value="Mine for stone and metal", inline=False)
			e.add_field(name="{}chop".format(ctx.prefix), value="Chop for wood", inline=False)
			e.add_field(name="{}fish".format(ctx.prefix), value="Fishing command", inline=False)
			await ctx.send(embed=e)
			return

		elif topic == "D" or topic == "d":
			
			e = discord.Embed(color=discord.Colour(0xffffff))
			e.set_author(name="Economy", icon_url=user.avatar_url)
			e.add_field(name="{}inv".format(ctx.prefix), value="Check your inventory", inline=True)
			e.add_field(name="{}sell".format(ctx.prefix), value="Sell an item", inline=True)
			e.add_field(name="{}market".format(ctx.prefix), value="Check the market or buy/sell items", inline=False)
			e.add_field(name="{}hp buy".format(ctx.prefix), value="Buy a healing potion", inline=False)
			e.add_field(name="{}buy exp".format(ctx.prefix), value="Buy a experience potion", inline=False)
			e.add_field(name="{}daily".format(ctx.prefix), value="Earn daily credits", inline=False)
			e.add_field(name="{}vote".format(ctx.prefix), value="Vote for the bot and get a big reward", inline=False)
			await ctx.send(embed=e)
			return

		elif topic == "E" or topic == "e":

			e = discord.Embed(color=discord.Colour(0xffffff))
			e.set_author(name="Guilds", icon_url=user.avatar_url)
			e.add_field(name="{}guild".format(ctx.prefix), value="Check all guild commands", inline=True)
			e.add_field(name="{}leaderboard".format(ctx.prefix), value="Open the players/guilds leaderboard", inline=True)
			await ctx.send(embed=e)
			return

		elif topic == "F" or topic == "f":

			e = discord.Embed(color=discord.Colour(0xffffff))
			e.set_author(name="Battles", icon_url=user.avatar_url)
			e.add_field(name="{}battle".format(ctx.prefix), value="Check all battle commands", inline=True)
			e.add_field(name="{}heal".format(ctx.prefix), value="Gain HP by consuming a health potion", inline=True)
			e.add_field(name="{}equip".format(ctx.prefix), value="Equip a weapon or a piece of armor", inline=False)
			await ctx.send(embed=e)	
			return

		elif topic == "G" or topic == "g":

			e = discord.Embed(color=discord.Colour(0xffffff))
			e.set_author(name="Raids", icon_url=user.avatar_url)
			e.add_field(name="Soon...", value="This is still in development", inline=True)
			await ctx.send(embed=e)	
			return

		elif topic == "H" or topic == "h":

			e = discord.Embed(color=discord.Colour(0xffffff))
			e.set_author(name="Admin Commands", icon_url=user.avatar_url)
			e.add_field(name="{}help".format(ctx.prefix), value="Shows a menu with useful links or get more information about a command", inline=True)
			e.add_field(name="{}commands".format(ctx.prefix), value="Shows this menu", inline=True)
			e.add_field(name="{}prefix".format(ctx.prefix), value="Set a new prefix for Solyx", inline=False)
			e.add_field(name="{}ignore".format(ctx.prefix), value="Set channels the bot has to ignore", inline=False)
			await ctx.send(embed=e)	
			return

		elif topic == "I" or topic == "i":

			e = discord.Embed(color=discord.Colour(0xffffff))
			e.set_author(name="Miscellaneous Commands", icon_url=user.avatar_url)
			e.add_field(name="{}vote".format(ctx.prefix), value="Vote for the bot and get a sweet reward", inline=True)
			e.add_field(name="{}help".format(ctx.prefix), value="Shows this menu", inline=False)
			e.add_field(name="{}commands".format(ctx.prefix), value="Shows this menu", inline=True)
			e.add_field(name="{}invite".format(ctx.prefix), value="Invite Solyx to your server", inline=True)
			e.add_field(name="{}info".format(ctx.prefix), value="See some information about Solyx, and it's status", inline=True)
			e.add_field(name="{}server".format(ctx.prefix), value="Get an invite to the Solyx server", inline=True)
			e.add_field(name="{}support".format(ctx.prefix), value="A list of all ways to get help with Solyx", inline=True)
			e.add_field(name="{}botstatus".format(ctx.prefix), value="Get a link to the Solyx status page", inline=True)
			e.add_field(name="{}website".format(ctx.prefix), value="Get a link to the Solyx website", inline=True)
			await ctx.send(embed=e)
			return

def setup(bot):
	n = command(bot)
	bot.add_cog(n)