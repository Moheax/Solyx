import discord
from discord.ext import commands

import datetime
import asyncio
import random
from random import choice as randchoice
from time import time

from utils.dataIO import fileIO
from utils.db import db
from utils.defaults import userdata, titledata, raiddata, battledata, guilddata



class titles(commands.Cog):
	def __init__(self, bot):
		super().__init__()
		self.bot = bot

# - - - Titles - - - # 



	@commands.group(name="title", pass_context=True, no_pm=True, aliases=["titles"])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def title(self, ctx):

		server = ctx.guild
		channel = ctx.channel
		servercolor = ctx.author.color

		user = ctx.message.author



		msg = ""
		if ctx.invoked_subcommand is None:
			for x in ctx.command.all_commands:
				if x not in ctx.command.all_commands[x].aliases:
					if not ctx.command.all_commands[x].hidden:
						msg += f"`{ctx.prefix}{ctx.command.name} {x}` - {ctx.command.all_commands[x].help} \n"
			embed=discord.Embed(colour=servercolor)
			embed.set_author(name=ctx.command.name, icon_url=ctx.author.avatar_url)
			embed.add_field(name="Subcommands", value=msg, inline=False)
			
			try:
				await ctx.send(embed=embed)
			except:
				return
		return


	@title.command(name="select", pass_context=True, no_pm=True, aliases=["title select","title equip","equip"])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def title_select(self, ctx):
		"""Select your title"""


		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		titlesinfo = db.titles.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to select a Title")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return
		choices = []
		inv_list = [i for i in titlesinfo["titles_list"]]
		if len(inv_list) == 0:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["title"]["notitles"]["translation"], color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					pass
				except:
					pass
		else:
			
			choices.append(inv_list)
			try:
				em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["title"]["select"]["title"]["translation"], color=discord.Colour(0xffffff))
				em.add_field(name="Titles:", value="\n{}".format("\n".join(inv_list)))
				em.set_footer(text=fileIO(f"data/languages/EN.json", "load")["rpg"]["title"]["select"]["footer"]["translation"])
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						pass
					except:
						pass
				answer1 = await self.check_answer(ctx, inv_list)
				em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["title"]["selected"]["translation"], description="{}".format(answer1), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						pass
					except:
						pass
			except:
				pass
			userinfo["title"] = answer1
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
	async def check_answer(self, ctx, valid_options):
		def pred(m):
			return m.author == ctx.author and m.channel == ctx.channel
		answer = await self.bot.wait_for('message', check=pred)

		if answer.content.lower() in valid_options:
			return answer.content
		elif answer.content in valid_options:
			return answer.content
		elif answer.content.upper() in valid_options:
			return answer.content
		else:
			return #await self.check_answer(ctx, valid_options)  //  This could keep a check loop going

	async def check_answer_other_user(self, ctx, user, valid_options):
		def pred(m):
			return m.author == user and m.channel == ctx.channel
		answer = await self.bot.wait_for('message', check=pred)

		if answer.content.lower() in valid_options:
			return answer.content
		elif answer.content in valid_options:
			return answer.content
		elif answer.content.upper() in valid_options:
			return answer.content
		else:
			return #await self.check_answer(ctx, valid_options)  //  This could keep a check loop going

	@title.command(name="list", pass_context=True, no_pm=True, aliases=["title list"])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def title_list(self, ctx):
		"""List your titles"""


		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })

		
		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to select a Title")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		
		titlesinfo = db.titles.find_one({ "_id": user.id })

		_titles = titlesinfo["titles_list"]
		
		list1 = ""
		list2 = ""
		list3 = ""
		list4 = ""
		list5 = ""
		list6 = ""
		list7 = ""
		list8 = ""
		list9 = ""
		list10 = ""
		try:
			if "Beginner" in _titles :
				list1 += "Beginner\n"

			if "Amateur" in _titles :
				list1 += "Amateur\n"

			if "Novice" in _titles :
				list1 += "Novice\n"

			if "Apprentice" in _titles :
				list1 += "Apprentice\n"

			if "Respected" in _titles :
				list1 += "Respected\n"

			if "Renowned" in _titles :
				list1 += "Renowned\n"

			if "Professional" in _titles :
				list1 += "Professional\n"

			if "Master" in _titles :
				list1 += "Master\n"

			if "Grand-Master" in _titles :
				list1 += "Grand-Master\n"

			if "Enlightened" in _titles :
				list1 += "Enlightened\n"

			if "Mighty" in _titles :
				list1 += "Mighty\n"

			if "Empowered" in _titles :
				list1 += "Empowered\n"

			if "Golden" in _titles :
				list1 += "Golden\n"
				
			if "Radiant" in _titles :
				list1 += "Radiant\n"

			if "Arcane" in _titles :
				list1 += "Arcane\n"

			if "Iridescent" in _titles :
				list1 += "Iridescent\n"

			if "Luminescent" in _titles :
				list1 += "Luminescent\n"

			if "Celestial" in _titles :
				list1 += "Celestial\n"

			if "Unbelievable" in _titles :
				list1 += "Unbelievable\n"

			if "Unreal" in _titles :
				list1 += "Unreal\n"

			if "Godlike" in _titles :
				list1 += "Godlike\n"

			if "Uncoordinated" in _titles :
				list2 += "Uncoordinated\n"
			
			if "Unhandy" in _titles :
				list2 += "Unhandy\n"
			
			if "Clumsy" in _titles :
				list2 += "Clumsy\n"
			
			if "Unskillful" in _titles :
				list2 += "Unskillful\n"
			
			if "Unskillful" in _titles :
				list2 += "Unskillful\n"
			
			if "Inexpert" in _titles :
				list2 += "Inexpert\n"
			
			if "I'm playing the game wrong..." in _titles :
				list2 += "I'm playing the game wrong...\n"
			
			if "Legendary" in _titles :
				list3 += "Legendary\n"
			
			if "Twice Told Legend" in _titles :
				list3 += "Twice Told Legend\n"
		
			if "Broke" in _titles :
				list4 += "Broke\n"
		
			if "Poor" in _titles :
				list4 += "Poor\n"
		
			if "Rich" in _titles :
				list4 += "Rich\n"
		
			if "Wealthy" in _titles :
				list4 += "Wealthy\n"
		
			if "Millionaire" in _titles :
				list4 += "Millionaire\n"
				
			if "Rookie Contractor" in _titles :
				list5 += "Rookie Contractor\n"

			if "Novice Contractor" in _titles :
				list5 += "Novice Contractor\n"

			if "Aspiring Contractor" in _titles :
				list5 += "Aspiring Contractor\n"

			if "Trusted Contractor" in _titles :
				list5 += "Trusted Contractor\n"

			if "Famed Contractor" in _titles :
				list5 += "Famed Contractor\n"

			if "Noble Contractor" in _titles :
				list5 += "Noble Contractor\n"
				
			if "Peek-a-Boo" in _titles :
				list6 += "Peek-A-Boo\n"
				
			if "Storyteller" in _titles :
				list6 += "Storyteller\n"
			
			if "Santa's Helper" in _titles :
				list6 += "Santa's Helper\n"

			if "Ho ho ho" in _titles :
				list6 += "Ho ho ho\n"
				
			if "Monster Slayer" in _titles :
				list7 += "Monster Slayer\n"

			if "Monster Hunter" in _titles :
				list7 += "Monster Hunter\n"

			if "Monster Killer" in _titles :
				list7 += "Monster Killer\n"

			if "Monster Executioner" in _titles :
				list7 += "Monster Executioner \n"

			if "Monster Exterminator" in _titles :
				list7 += "Monster Exterminator\n"

			if "Rachi Killer" in _titles :
				list8 += "Rachi Killer\n"

			if "Debin Killer" in _titles :
				list8 += "Debin Killer\n"
			
			if "Debin Killer" in _titles :
				list8 += "Debin Killer\n"

			if "Oofer Killer" in _titles :
				list8 += "Oofer Killer\n"

			if "Wyvern Killer" in _titles :
				list8 += "Wyvern Killer\n"

			if "Draugr Killer" in _titles :
				list8 += "Draugr Killer\n"

			if "Stalker Killer" in _titles :
				list8 += "Stalker Killer\n"

			if "Souleater Killer" in _titles :
				list8 += "Souleater Killer\n"

			if "Wolf Killer" in _titles :
				list8 += "Wolf Killer\n"

			if "Goblin Killer" in _titles :
				list8 += "Goblin Killer\n"

			if "Zombie Killer" in _titles :
				list8 += "Zombie Killer\n"

			if "Elder Dragon Killer" in _titles :
				list8 += "Elder Dragon Killer\n"

			if "Hades Killer" in _titles :
				list8 += "Hades Killer\n"

			if "Ebony Guardian Killer" in _titles :
				list8 += "Ebony Guardian Killer\n"

			if "Ettin Killer" in _titles :
				list8 += "Ettin Killer\n"
			
			if "Dormammu Killer" in _titles :
				list8 += "Dormammu Killer\n"

			if "Harpy Killer" in _titles :
				list8 += "Harpy Killer\n"

			if "Saurian Killer" in _titles :
				list8 += "Saurian Killer\n"

			if "Deathclaw Killer" in _titles :
				list8 += "Deathclaw Killer\n"

			if "Largos Killer" in _titles :
				list8 += "Largos Killer\n"

			if "Skeleton Killer" in _titles :
				list8 += "Skeleton Killer\n"

			if "Lizardmen Killer" in _titles :
				list8 += "Lizardmen Killer\n"

			if "Giant Killer" in _titles :
				list8 += "Giant Killer\n"

			if "Ice Wolves Killer" in _titles :
				list8 += "Ice Wolves Killer\n"

			if "Frost Goblin Killer" in _titles :
				list8 += "Frost Goblin Killer\n"

			if "Frost Orc Killer" in _titles :
				list8 += "Frost Orc Killer\n"

			if "Fire Golem Killer" in _titles :
				list9 += "Fire Golem Killer\n"

			if "The Corrupted Killer" in _titles :
				list9 += "The Corrupted Killer\n"

			if "Phantasm Killer" in _titles :
				list9 += "Phantasm Killer\n"

			if "The Accursed Killer" in _titles :
				list9 += "The Accursed Killer\n"

			if "The Nameless King Killer" in _titles :
				list9 += "The Nameless King Killer\n"

			if "The Venomous Killer" in _titles :
				list9 += "The Venomous Killer\n"

			if "Death Knight Killer" in _titles :
				list9 += "Death Knight Killer\n"

			if "Frost Dragon Killer" in _titles :
				list9 += "Frost Dragon Killer\n"

			if "Goose catcher" in _titles :
				list10 += "Goose catcher\n"

			if "Fox tracker" in _titles :
				list10 += "Fox tracker\n"

			if "Bear friend" in _titles :
				list10 += "Bear friend\n"

			if "Strange dog keeper" in _titles :
				list10 += "Strange dog keeper\n"

			if "Dino-Bird trainer" in _titles :
				list10 += "Dino-Bird trainer\n"

			
		
		
			
		except:
			pass
		#for i, x in enumerate(range(0, 100)):
		#	try:
		#		item = _titles[i]
		#		
		#		if i <= 49 and i >= 0:	
		#			list1 += "{} - {}\n".format(i + 1, item)
		#		
		#		if i <= 100 and i >= 50:	
		#			list2 += "{} - {}\n".format(i + 1, item)	
		#	except:
		#		pass
		
		list1 += "_ _\n"
		list2 += "_ _\n"
		list3 += "_ _\n"
		list4 += "_ _\n"
		list5 += "_ _\n"
		list6 += "_ _\n"
		list7 += "_ _\n"
		list8 += "_ _\n"
		list9 += "_ _\n"
		list10 += "_ _\n"



		em = discord.Embed(title="{}'s Titles, {} / 89 Aquired!".format(user.name, titlesinfo["titles_amount"]), color=discord.Colour(0xffffff))
		
		
		try:
			em.add_field(name="Death Titles", value=list2)
		except:
			pass

		try:
			em.add_field(name="Quests titles", value=list5)
		except:
			pass
	
		try:
			em.add_field(name="Money titles", value=list4)
		except:
			pass

		

		try:
			em.add_field(name="Pet titles", value=list10)
		except:
			pass

		try:
			em.add_field(name="Event titles", value=list6)
		except:
			pas
		
		try:
			em.add_field(name="Legendary titles", value=list3)
		except:
			pass
		
		em2 = discord.Embed(title="{}'s Titles".format(user.name), color=discord.Colour(0xffffff))
			
		
		try:
			em2.add_field(name="Monster kill titles", value=list8)
		except:
			pass

		try:
			em2.add_field(name="Level titles", value=list1)
		except:
			pass

		try:
			em2.add_field(name="Boss kill titles", value=list9)
		except:
			pass

		try:
			em2.add_field(name="Kill count titles", value=list7)
		except:
			pass
		



		try:
			try:
				await ctx.send(embed=em)
				await ctx.send(embed=em2)
			except:
				pass
		except:

			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return

	@title.command(name="flex", pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def _flex(self, ctx):
		"""Flex!!"""
		
		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })

		
		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has Flexed")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return


		titlesinfo = db.titles.find_one({ "_id": user.id })


		em = discord.Embed(title="{} ".format(userinfo["name"]),description="**Title:** {}\n**Kills:** {}".format(userinfo["title"], userinfo["enemieskilled"]), color=discord.Colour(0xff0000))
		await ctx.send(embed=em)

		

def setup(bot):
	c = titles(bot)
	bot.add_cog(c)