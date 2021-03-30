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



# 1. User creates party if not one made already.
# 2. User owns the party and can Add another user.
# 3. User that owns the party can Disband the party.
# 4. User that owns the party can Kick Party Members.
# 5. User that doesnt own the party cannot add users.
# 6. user thyat doesnt own the party can leave the party
# 7. party list is a individual database and wont be user only.


class party(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.group(name="party", aliases=["p"], pass_context=True, no_pm=True, hidden=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _party(self, ctx):
		"""Party!"""
		guild = ctx.guild
		channel = ctx.channel
		guildcolor = ctx.author.color

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]
			
		msg = ""
		if ctx.invoked_subcommand is None:
			for x in ctx.command.all_commands:
				if x not in ctx.command.all_commands[x].aliases:
					if not ctx.command.all_commands[x].hidden:
						msg += f"`{ctx.prefix}{ctx.command.name} {x}` - {ctx.command.all_commands[x].help} \n"
			embed=discord.Embed(colour=guildcolor)
			embed.set_author(name=ctx.command.name, icon_url=ctx.author.avatar_url)
			embed.add_field(name="Subcommands", value=msg, inline=False)
			
			try:
				await ctx.send(embed=embed)
			except:
				return
		return

	@_party.group(name="create", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _create(self, ctx):
		"""Create your own party"""

	


		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })
		partyinfo = db.party.find_one({ "_id": userinfo["party"] })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to check create a party")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return
		party_list = "" 
		if userinfo["party"] != "None":
			for i in range(partyinfo["amount"]):

			
				try:
					icon = ""
					Class = userinfo["class"]
					if Class == "Mage":
						icon = "<:Mage:752633441626882058> "
					if Class == "Elementalist":
						icon = "<:Elementalist:752638205584474164> "
					if Class == "Necromancer":
						icon = "<:Necromancer:752638205832069191> "
					if Class == "Developed Necromancer":
						icon = "<:Necromancer:752638205832069191> "
					if Class == "Adequate Elementalist":
						icon = "<:Elementalist:752638205584474164> "
					if Class == "Paladin":
						icon = "<:Paladin:752638205869949168> "
					if Class == "Samurai":
						icon = "<:Samurai:752638205920018603> "
					if Class == "Knight":
						icon = "<:Knight:752633441362903120> "
					if Class == "Master Samurai":
						icon = "<:Samurai:752638205920018603> "
					if Class == "Grand Paladin":
						icon = "<:Paladin:752638205869949168> "
					if Class == "Thief":
						icon = "<:Thief:752633441811693638> "
					if Class == "Mesmer":
						icon = "<:Mesmer:752638205697851413> "
					if Class == "Rogue":
						icon = "<:Rogue:752638205928538252> "
					if Class == "High Rogue":
						icon = "<:Rogue:752638205928538252> "
					if Class == "Adept Mesmer":
						icon = "<:Mesmer:752638205697851413> "
					if Class == "Archer":
						icon = "<:Archer:752633441282949222> "
					if Class == "Ranger":
						icon = "<:Ranger:752638206285185116> "
					if Class == "Assassin":
						icon = "<:Assassin:639473417791209472> "
					if Class == "Night Assassin":
						icon = "<:Assassin:639473417791209472> "
					if Class == "Skilled Ranger":
						icon = "<:Ranger:752638206285185116> "
				except:
					pass

				friend_id = partyinfo["members"][i]
				friend_info = db.users.find_one({ "_id": friend_id })


				friend_name = friend_info["name"]
				friend_level = friend_info["lvl"]
				friend_class = friend_info["class"]
		
				flist = ("{}. **{}**: {} <:Magic:560844225839890459>, **Class:** {} {}\n".format(i + 1, friend_name, friend_level, friend_class, icon))

				party_list +=  flist

			

			em = discord.Embed(description=party_list, color=discord.Colour(0xffffff))
			em.set_author(name="You already have a party!\n{}\n{}/{} Members".format(partyinfo["Title"], partyinfo["amount"], partyinfo["limit"]), icon_url=user.avatar_url)
		
			try:
				await ctx.send(embed=em)
				return
			except Exception as e:
				print(e)
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return


		if userinfo["role"] == "Developer":
			user_limit = 4
		if userinfo["role"] == "Player":
			user_limit = 4
		if userinfo["role"] == "patreon1":
			user_limit = 5
		if userinfo["role"] == "patreon2":
			user_limit = 5
		if userinfo["role"] == "patreon3":
			user_limit = 6
		if userinfo["role"] == "patreon4":
			user_limit = 6

		title = userinfo["name"]

		party_info = { "Title": title, "owner": user.id, "limit": user_limit, "members": [user.id], "amount": 1 }

		

		
		x = db.party.insert_one(party_info)
		userinfo["party"] = x.inserted_id		

		db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		partyinfo = db.party.find_one({ "_id": userinfo["party"] })
		userinfo = db.users.find_one({ "_id": user.id })
		
		
		
		party_list = "" 

		for i in range(partyinfo["amount"]):

			try:
				icon = ""
				Class = userinfo["class"]
				if Class == "Mage":
					icon = "<:Mage:752633441626882058> "
				if Class == "Elementalist":
					icon = "<:Elementalist:752638205584474164> "
				if Class == "Necromancer":
					icon = "<:Necromancer:752638205832069191> "
				if Class == "Developed Necromancer":
					icon = "<:Necromancer:752638205832069191> "
				if Class == "Adequate Elementalist":
					icon = "<:Elementalist:752638205584474164> "
				if Class == "Paladin":
					icon = "<:Paladin:752638205869949168> "
				if Class == "Samurai":
					icon = "<:Samurai:752638205920018603> "
				if Class == "Knight":
					icon = "<:Knight:752633441362903120> "
				if Class == "Master Samurai":
					icon = "<:Samurai:752638205920018603> "
				if Class == "Grand Paladin":
					icon = "<:Paladin:752638205869949168> "
				if Class == "Thief":
					icon = "<:Thief:752633441811693638> "
				if Class == "Mesmer":
					icon = "<:Mesmer:752638205697851413> "
				if Class == "Rogue":
					icon = "<:Rogue:752638205928538252> "
				if Class == "High Rogue":
					icon = "<:Rogue:752638205928538252> "
				if Class == "Adept Mesmer":
					icon = "<:Mesmer:752638205697851413> "
				if Class == "Archer":
					icon = "<:Archer:752633441282949222> "
				if Class == "Ranger":
					icon = "<:Ranger:752638206285185116> "
				if Class == "Assassin":
					icon = "<:Assassin:639473417791209472> "
				if Class == "Night Assassin":
					icon = "<:Assassin:639473417791209472> "
				if Class == "Skilled Ranger":
					icon = "<:Ranger:752638206285185116> "
			except:
				pass

			friend_id = partyinfo["members"][i]
			friend_info = db.users.find_one({ "_id": friend_id })


			friend_name = friend_info["name"]
			friend_level = friend_info["lvl"]
			friend_class = friend_info["class"]
		
			flist = ("{}. **{}**: {} <:Magic:560844225839890459>, **Class:** {} {}\n".format(i + 1, friend_name, friend_level, friend_class, icon))

			party_list +=  flist
		
			
		em = discord.Embed(description=party_list, color=discord.Colour(0xffffff))
		em.set_author(name="You have succesfully created your party!\n{}'s Party\n{}/{} Members".format(partyinfo["Title"], partyinfo["amount"], partyinfo["limit"]), icon_url=user.avatar_url)
		
		try:
			await ctx.send(embed=em)
			return
		except Exception as e:
			print(e)
			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return

	@_party.group(name="list", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _list(self, ctx):
		"""Check your party list"""


		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })
		partyinfo = db.party.find_one({ "_id": userinfo["party"] })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to check their friend list")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return
		

		party_list = "" 
		if userinfo["party"] == "None": 
			em = discord.Embed(title="Party list", description="You are not in a party.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		for i in range(partyinfo["amount"]):

			friend_id = partyinfo["members"][i]
			friend_info = db.users.find_one({ "_id": friend_id })

			try:

				icon = ""
				Class = friend_info["class"]
				if Class == "Mage":
					icon = "<:Mage:752633441626882058> "
				if Class == "Elementalist":
					icon = "<:Elementalist:752638205584474164> "
				if Class == "Necromancer":
					icon = "<:Necromancer:752638205832069191> "
				if Class == "Developed Necromancer":
					icon = "<:Necromancer:752638205832069191> "
				if Class == "Adequate Elementalist":
					icon = "<:Elementalist:752638205584474164> "
				if Class == "Paladin":
					icon = "<:Paladin:752638205869949168> "
				if Class == "Samurai":
					icon = "<:Samurai:752638205920018603> "
				if Class == "Knight":
					icon = "<:Knight:752633441362903120> "
				if Class == "Master Samurai":
					icon = "<:Samurai:752638205920018603> "
				if Class == "Grand Paladin":
					icon = "<:Paladin:752638205869949168> "
				if Class == "Thief":
					icon = "<:Thief:752633441811693638> "
				if Class == "Mesmer":
					icon = "<:Mesmer:752638205697851413> "
				if Class == "Rogue":
					icon = "<:Rogue:752638205928538252> "
				if Class == "High Rogue":
					icon = "<:Rogue:752638205928538252> "
				if Class == "Adept Mesmer":
					icon = "<:Mesmer:752638205697851413> "
				if Class == "Archer":
					icon = "<:Archer:752633441282949222> "
				if Class == "Ranger":
					icon = "<:Ranger:752638206285185116> "
				if Class == "Assassin":
					icon = "<:Assassin:639473417791209472> "
				if Class == "Night Assassin":
					icon = "<:Assassin:639473417791209472> "
				if Class == "Skilled Ranger":
					icon = "<:Ranger:752638206285185116> "
			except:
				pass

		


			friend_name = friend_info["name"]
			friend_level = friend_info["lvl"]
			friend_class = friend_info["class"]
		
			flist = ("{}. **{}**: {} <:Magic:560844225839890459>, **Class:** {} {}\n".format(i + 1, friend_name, friend_level, friend_class, icon))

			party_list +=  flist
		
			
		em = discord.Embed(description=party_list, color=discord.Colour(0xffffff))
		em.set_author(name="Party {}\n{}/{} Members".format(partyinfo["Title"], partyinfo["amount"], partyinfo["limit"]), icon_url=user.avatar_url)
		
		try:
			await ctx.send(embed=em)
			return
		except Exception as e:
			print(e)
			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return

		
	@_party.group(name="add", aliases=["invite"], pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _add(self, ctx, user: discord.Member):
		"""invite a user to your party!"""

		languageinfo = db.servers.find_one({ "_id": ctx.guild.id })
		language = languageinfo["language"]

		author = ctx.author
		
		# INVITER
		authorinfo = db.users.find_one({ "_id": author.id })

		# PARTY 
		partyinfo = db.party.find_one({ "_id": authorinfo["party"] })

		# USER
		userinfo = db.users.find_one({ "_id": user.id })

		# CHECK IF USERS INVITES ITSELF
		if authorinfo["_id"] == userinfo["_id"]:
			await ctx.send("<:Solyx:560809141766193152> **| You can't add yourself to your party.**")
			return

		# CHECK IF USERS EXIST
		if authorinfo["race"] == "None" or authorinfo["class"] == "None":
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		# CHECK IF INVITER IS ALREADY IN A PARTY

		if userinfo["party"] != "None":
			
			em = discord.Embed(title="Party invite Canceled", description="User is already in a party.", color=discord.Colour(0xffffff))
			em.set_footer(text="They can leave a party with {}party leave".format(ctx.prefix))
			await ctx.send(embed=em)
			return
	
	    # CHECK IF USERS AND AUTHOR ARE ALREADY IN THE PARTY

		if user.id in partyinfo["members"]:
			em = discord.Embed(title="Party invite", description="User is already in this Party.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		guild = ctx.guild
		channel = ctx.channel
		guildcolor = ctx.author.color

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+author.name+"#"+author.discriminator,"Has tried to add a user to their party.")

		await ctx.send("{}".format(user.mention))
		em = discord.Embed(title="Party invite", description="{} (Level: {}) has send a Party invite!\nDo you accept?".format(author.mention, authorinfo["lvl"]), color=discord.Colour(0xffffff))
		em.set_footer(text="Say yes/no")

		await ctx.send(embed=em)
		answer1 = await self.check_answer_other_user(ctx, user, ["yes", "no", "n", "y", "Y", "Yes", "N", "No"])
		if answer1 in ["y", "yes", "Y", "Yes"]:

			# USER GETS ADDED TO INVITERS PARTY LIST
			partyinfo["amount"] += 1
			partyinfo["members"].append(userinfo["_id"])
			
			userinfo["party"] = partyinfo["_id"]
			print(userinfo["party"])
			print(partyinfo["_id"])
			db.party.replace_one({ "_id": authorinfo["party"] }, partyinfo, upsert=True)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			
			em = discord.Embed(title="Party Invite Accepted", description="{} has joined {}".format(user.mention, partyinfo["Title"]), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return
			

		elif answer1 in ["n", "no", "N", "No"]:
			await ctx.send("<:CrossShield:560804112548233217> **| Party Request Denied.**")
			return

		
	@_party.group(name="leave", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _leave(self, ctx):
		"""leave the party"""

		languageinfo = db.servers.find_one({ "_id": ctx.guild.id })
		language = languageinfo["language"]

		user = ctx.author

		# REMOVER
		userinfo = db.users.find_one({ "_id": user.id })

		# PARTY 
		partyinfo = db.party.find_one({ "_id": userinfo["party"] })

		# CHECK IF USERS REMOVES ITSELF AS PARTYMEMEBER
		if userinfo["_id"] != userinfo["_id"]:
			await ctx.send("<:Solyx:560809141766193152> **| You can't remove another user from the party.**")
			return

		# CHECK IF USERS EXIST
		if userinfo["race"] == "None" or userinfo["class"] == "None":
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		guild = ctx.guild
		channel = ctx.channel
		guildcolor = ctx.author.color

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to remove a friend")

		if userinfo["party"] != "None":
			partyinfo["amount"] -= 1
			partyinfo["members"].remove(userinfo["_id"])

			db.party.replace_one({ "_id": userinfo["party"] }, partyinfo, upsert=True)

			userinfo["party"] = "None"
			
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			
			
			em = discord.Embed(title="Party left", description="{} has left the Party".format(user.mention), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		else:
			em = discord.Embed(title="Party left", description="You are not in a party.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return
			
	@_party.group(name="kick", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _kick(self, ctx,  user: discord.Member):
		"""kick a user from the party"""

		languageinfo = db.servers.find_one({ "_id": ctx.guild.id })
		language = languageinfo["language"]

		author = ctx.author

		# INVITER
		authorinfo = db.users.find_one({ "_id": author.id })

		# PARTY 
		partyinfo = db.party.find_one({ "_id": authorinfo["party"] })

		# USER
		userinfo = db.users.find_one({ "_id": user.id })

		# CHECK IF USERS REMOVES ITSELF AS PARTYMEMEBER
		if author == user:
			await ctx.send("<:Solyx:560809141766193152> **| You can't kick yourself from the party.**")
			return

		# CHECK IF USERS EXIST
		if userinfo["race"] == "None" or userinfo["class"] == "None":
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		guild = ctx.guild
		channel = ctx.channel
		guildcolor = ctx.author.color

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to kick a user from their party")
		if authorinfo["party"] == "None": 
			em = discord.Embed(title="Party left", description="You are not in a party.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		if partyinfo["owner"] == authorinfo["_id"]:
			partyinfo["amount"] -= 1
			partyinfo["members"].remove(userinfo["_id"])

			db.party.replace_one({ "_id": authorinfo["party"] }, partyinfo, upsert=True)

			userinfo["party"] = "None"
			
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			
			
			em = discord.Embed(title="Party kick.", description="{} has been kicked from {}".format(user.mention, partyinfo["Title"]), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
		else:
			em = discord.Embed(title="Party kick.", description="You cant kick people from this party.".format(), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)

	@_party.group(name="disband", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _disband(self, ctx):
		"""Disband your party"""

		languageinfo = db.servers.find_one({ "_id": ctx.guild.id })
		language = languageinfo["language"]


		author = ctx.author


		# PARTY OWNER
		authorinfo = db.users.find_one({ "_id": author.id })

		# PARTY 
		partyinfo = db.party.find_one({ "_id": authorinfo["party"] })

		# USER
		

		

		# CHECK IF USERS EXIST
		if authorinfo["race"] == "None" or authorinfo["class"] == "None":
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		guild = ctx.guild
		channel = ctx.channel
		guildcolor = ctx.author.color

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+author.name+"#"+author.discriminator,"Has tried to kick a user from their party")
		if authorinfo["party"] == "None": 
				em = discord.Embed(title="Party", description="You are not in a party.", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

		if partyinfo["owner"] == authorinfo["_id"]:
			
			try: 
				for i in range(partyinfo["amount"]):
					partyinfo["amount"] -= 1
					userinfo = db.users.find_one({ "_id": partyinfo["members"][i]-1})
					partyinfo["members"].remove(partyinfo["members"][i])

				
					userinfo["party"] = "None"

					db.party.replace_one({ "_id": authorinfo["party"] }, partyinfo, upsert=True)
					db.users.replace_one({ "_id": userinfo["_id"] }, userinfo, upsert=True)
			except:
				pass
			
		em = discord.Embed(title="Party Disbanded.", description="{} has been disbanded ".format( partyinfo["Title"]), color=discord.Colour(0xffffff))
		await ctx.send(embed=em)
		try:
			authorinfo["party"] = "None"
			db.users.replace_one({ "_id": author.id}, authorinfo, upsert=True)
		except:
			pass



	@_party.group(name="title", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _title(self, ctx, *new_title):
		"""Change the party name"""

		languageinfo = db.servers.find_one({ "_id": ctx.guild.id })
		language = languageinfo["language"]

		author = ctx.author

		# PARTY OWNER
		authorinfo = db.users.find_one({ "_id": author.id })

		# PARTY 
		partyinfo = db.party.find_one({ "_id": authorinfo["party"] })

		# CHECK IF USERS EXIST
		if authorinfo["race"] == "None" or authorinfo["class"] == "None":
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		guild = ctx.guild
		channel = ctx.channel
		guildcolor = ctx.author.color

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+author.name+"#"+author.discriminator,"Has tried to kick a user from their party")
		print(new_title)
		if authorinfo["party"] == "None": 
			em = discord.Embed(title="Party", description="You are not in a party.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		if partyinfo["owner"] == authorinfo["_id"]:
			try: 
				s = ' ' 
				new_correct_title = s.join(new_title)
				partyinfo["Title"] = new_correct_title

				db.party.replace_one({ "_id": authorinfo["party"] }, partyinfo, upsert=True)	
			except:
				pass
			
		em = discord.Embed(title="Party title.", description="Renamed party to {} ".format(partyinfo["Title"]), color=discord.Colour(0xffffff))
		await ctx.send(embed=em)
		print(new_title)

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

def setup(bot):
	c = party(bot)
	bot.add_cog(c)
