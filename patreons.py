import discord
import random
import time
import datetime
from discord.ext import commands
import asyncio
from random import choice as randchoice
from discord import Permissions
from utils.checks import staff, developer, owner
# from cogs.economy import NoAccount
from utils.db import db
from utils.dataIO import fileIO

import threading


class patreons(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def patreon(self, ctx):

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has Checked Patreon site!!")

		#Website

	
		embed=discord.Embed(title="Solyx Patreon list!", color=discord.Colour(0xffffff))
		
		embed.add_field(name="Mythical Patreon ", value="<@157614072525881344>\n\n_ _", inline=False)
		embed.add_field(name="Legendary Patreon", value="<@440513778996609024>\n\n_ _", inline=False)			
		embed.add_field(name="Rare Patreon", value="Become the first!\n\n_ _", inline=False)
		embed.add_field(name="Common Patreon", value="<@370160829053796352>\n\n_ _", inline=False)
		embed.add_field(name="Become a patreon!", value="Click [here](https://www.patreon.com/Solyx?fan_landing=true) to visit the patreon site!", inline=False)
		embed.set_footer(text="Many Many thanks to these people!")
		embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/560845406750375937.png?v=1")
		await ctx.send(embed=embed)

	@commands.command(pass_context=True)
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def claim(self, ctx):

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has Claimed patreon rewards!!")

		userinfo = db.users.find_one({ "_id": user.id })
		titlesinfo = db.titles.find_one({ "_id": user.id })

		_titles = titlesinfo["titles_list"]

		try:
			
			# Time left till user can claim monthly rewards again
			curr_time = time.time()
			delta = float(curr_time) - float(userinfo["monthlyrewards"])
			seconds = 2505600 - delta
			m, s = divmod(seconds, 60)
			h, m = divmod(m, 60)
			d, h = divmod(h, 24)
			if userinfo["role"] == "Player" :
				embed=discord.Embed(title="You are not a patreon!".format(user.name), color=discord.Colour(0xff0000))
				embed.add_field(name="Become a patreon!", value="Click [here](https://www.patreon.com/Solyx?fan_landing=true) to visit the patreon site!", inline=False)
				embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/649157253701566474.png?v=1")
				await ctx.send(embed=embed)
				return

			if seconds <= 0:
				
				try:
					userinfo["monthlyrewards"] = curr_time
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

				if userinfo["role"] == "patreon1" or userinfo["role"] == "Developer":
					list1= ""
					list2= ""
					if "Common Supporter" in _titles :
						list1 += "Common supporter Title | <:ShieldCheck:560804135545602078> already claimed.\n"
					else:
						list1 += "Common supporter Title claimed!\n"
						newtitle = "Common Supporter"
						if not newtitle in titlesinfo["titles_list"]:
							titlesinfo["titles_list"].append(newtitle)
							titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
							db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
							em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
							try:
								await user.send(embed=em)
							except:
								await ctx.send(embed=em)

					list1 += "Open 2 crates at the same time!\n"
					list1 += "Use 2 Exp potions at the same time!\n"

					list2 += "<:GoldBars:573781770709893130>2500 Gold\n"
					list2 += "<:Crate:639425690072252426>15 crates\n"
					list2 += "<:Key:573780034355986432>15 keys\n"
					list2 += "<:HealingPotion:573577125064605706>25 Health Potions\n"
					list2 += "<:ExpBottle:770044187348566046>25 Experience Potions\n"

					embed=discord.Embed(color=discord.Colour(0x26b644))
					try:	
						embed.set_author(name="{} | Tier 1 Patreon".format(userinfo["name"]), icon_url=user.avatar_url)
					except:
						embed.set_author(name="{} | Tier 1 Patreon".format(userinfo["name"]))
						pass

									
					embed.add_field(name="_ _\nYour rewards", value=list1, inline=False)
					embed.add_field(name="_ _\nYour Monthly rewards", value=list2, inline=False)
					try:
						embed.set_footer(text="Thank you so much for being a patreon!", icon_url="https://cdn.discordapp.com/emojis/560845406750375937.png?v=1")
					except:
						pass
					embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/573784881012932618.png?v=1")
					await ctx.send(embed=embed)

					userinfo["gold"] += 52500
					userinfo["lootbag"] += 15
					userinfo["keys"] += 15
					userinfo["hp_potions"] += 15
					userinfo["exp_potions"] += 15
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)


				if userinfo["role"] == "patreon2":
					list1= ""
					list2= ""
					if "Rare Supporter" in _titles :
						list1 += "Rare supporter Title | <:ShieldCheck:560804135545602078> already claimed.\n"
					else:
						list1 += "Rare supporter Title claimed!\n"
						newtitle = "Rare Supporter"
						if not newtitle in titlesinfo["titles_list"]:
							titlesinfo["titles_list"].append(newtitle)
							titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
							db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
							em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
							try:
								await user.send(embed=em)
							except:
								await ctx.send(embed=em)

					list1 += "Open 3 crates at the same time!\n"
					list1 += "Use 3 Exp potions at the same time!\n"
					list1 += "1.2X daily rewards!\n"
					list1 += "1.2X vote rewards!\n"
					list1 += "Sneak peak at upcoming events.\n"
					list1 += "4th spot in support server.\n"

					list2 += "<:GoldBars:573781770709893130>5000 Gold\n"
					list2 += "<:Crate:639425690072252426>25 crates\n"
					list2 += "<:Key:573780034355986432>25 keys\n"
					list2 += "<:HealingPotion:573577125064605706>25 Health Potions\n"
					list2 += "<:ExpBottle:770044187348566046>25 Experience Potions\n"

					embed=discord.Embed(color=discord.Colour(0x26b644))
					try:	
						embed.set_author(name="{} | Tier 2 Patreon".format(userinfo["name"]), icon_url=user.avatar_url)
					except:
						embed.set_author(name="{} | Tier 2 Patreon".format(userinfo["name"]))
						pass

									
					embed.add_field(name="_ _\nYour rewards", value=list1, inline=False)
					embed.add_field(name="_ _\nYour Monthly rewards", value=list2, inline=False)
					try:
						embed.set_footer(text="Thank you so much for being a patreon!", icon_url="https://cdn.discordapp.com/emojis/560845406750375937.png?v=1")
					except:
						pass
					embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/573784880815538186.png?v=1")
					await ctx.send(embed=embed)

					userinfo["gold"] += 5000
					userinfo["lootbag"] += 25
					userinfo["keys"] += 25
					userinfo["hp_potions"] += 25
					userinfo["exp_potions"] += 25
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

				if userinfo["role"] == "patreon3":
					list1= ""
					list2= ""
					if "Legendary Supporter" in _titles :
						list1 += "Legendary supporter Title | <:ShieldCheck:560804135545602078> already claimed.\n"
					else:
						list1 += "Legendary supporter Title claimed!\n"
						newtitle = "Legendary Supporter"
						if not newtitle in titlesinfo["titles_list"]:
							titlesinfo["titles_list"].append(newtitle)
							titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
							db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
							em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
							try:
								await user.send(embed=em)
							except:
								await ctx.send(embed=em)

					list1 += "Open 4 crates at the same time!\n"
					list1 += "Use 4 Exp potions at the same time!\n"
					list1 += "1.5X daily rewards!\n"
					list1 += "1.5X vote rewards!\n"
					list1 += "Sneak peak at upcoming events.\n"
					list1 += "3rd spot in support server.\n"

					list2 += "<:GoldBars:573781770709893130>12000  Gold\n"
					list2 += "<:Crate:639425690072252426>40 crates\n"
					list2 += "<:Key:573780034355986432>40 keys\n"
					list2 += "<:HealingPotion:573577125064605706>40 Health Potions\n"
					list2 += "<:ExpBottle:770044187348566046>40 Experience Potions\n"

					embed=discord.Embed(color=discord.Colour(0x26b644))
					try:	
						embed.set_author(name="{} | Tier 3 Patreon".format(userinfo["name"]), icon_url=user.avatar_url)
					except:
						embed.set_author(name="{} | Tier 3 Patreon".format(userinfo["name"]))
						pass

									
					embed.add_field(name="_ _\nYour rewards", value=list1, inline=False)
					embed.add_field(name="_ _\nYour Monthly rewards", value=list2, inline=False)
					try:
						embed.set_footer(text="Thank you so much for being a patreon!", icon_url="https://cdn.discordapp.com/emojis/560845406750375937.png?v=1")
					except:
						pass
					embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/639425368167809065.png?v=1")
					await ctx.send(embed=embed)		

			


					userinfo["gold"] += 12000
					userinfo["lootbag"] += 40
					userinfo["keys"] += 40
					userinfo["hp_potions"] += 40
					userinfo["exp_potions"] += 40
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)


				if userinfo["role"] == "patreon4":
					list1= ""
					list2= ""
					if "Mythical Supporter" in _titles :
						list1 += "Mythical supporter Title | <:ShieldCheck:560804135545602078> already claimed.\n"
					else:
						list1 += "Mythical supporter Title claimed!\n"
						newtitle = "Mythical Supporter"
						if not newtitle in titlesinfo["titles_list"]:
							titlesinfo["titles_list"].append(newtitle)
							titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
							db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
							em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
							try:
								await user.send(embed=em)
							except:
								await ctx.send(embed=em)

					list1 += "Open 5 crates at the same time!\n"
					list1 += "Use 5 Exp potions at the same time!\n"
					list1 += "1.5X daily rewards!\n"
					list1 += "1.5X vote rewards!\n"
					list1 += "Sneak peak at upcoming events.\n"
					list1 += "2rd spot in support server.\n"

					list2 += "<:GoldBars:573781770709893130>20000  Gold\n"
					list2 += "<:Crate:639425690072252426>50 crates\n"
					list2 += "<:Key:573780034355986432>50 keys\n"
					list2 += "<:HealingPotion:573577125064605706>50 Health Potions\n"
					list2 += "<:ExpBottle:770044187348566046>50 Experience Potions\n"

					embed=discord.Embed(color=discord.Colour(0x26b644))
					try:	
						embed.set_author(name="{} | Tier 4 Patreon".format(userinfo["name"]), icon_url=user.avatar_url)
					except:
						embed.set_author(name="{} | Tier 4 Patreon".format(userinfo["name"]))
						pass
					
									
					embed.add_field(name="_ _\nYour rewards", value=list1, inline=False)
					embed.add_field(name="_ _\nYour Monthly rewards", value=list2, inline=False)
					try:
						embed.set_footer(text="Thank you so much for being a patreon!", icon_url="https://cdn.discordapp.com/emojis/560845406750375937.png?v=1")
					except:
						pass
					embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/573784881386225694.png?v=1")
					await ctx.send(embed=embed)		


					userinfo["gold"] += 50000
					userinfo["lootbag"] += 50
					userinfo["keys"] += 50
					userinfo["hp_potions"] += 50
					userinfo["exp_potions"] += 50
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)


			else:
				
				embed=discord.Embed(color=discord.Colour(0xffffff))
				embed.add_field(name="Cooldown!", value=":hourglass: You can't claim your monthly rewards for another \n**"+ str(round(d)) + " Days, "+ str(round(h)) + " hours, "+ str(round(m)) + " minutes and " + str(round(s)) + " seconds.**\n\n_ _", inline=False)
				embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/639447293271080982.png?v=1")
				await ctx.send(embed=embed)
				return
				

				


		except:
			embed=discord.Embed(title="Something went wrong!".format(user.name), color=discord.Colour(0xffffff))
			embed.set_footer(text="Please try again to claim your rewards!")
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/649157253701566474.png?v=1")
			await ctx.send(embed=embed)
			return
def setup(bot):
	n = patreons(bot)
	bot.add_cog(n)