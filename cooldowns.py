import datetime
import time

import discord
from discord.ext import commands

# from cogs.economy import NoAccount
from utils.db import db


class cooldowns(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True, aliases=["cd"])
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def cooldowns(self, ctx):

		user = ctx.message.author

		userinfo = db.users.find_one({"_id": user.id})

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		if userinfo and userinfo["blacklisted"] == "True":
			return

		print(current_time + " | " + guild.name + " | " + channel.name + " | " + user.name + "#" + user.discriminator,
			  "Has checked their cooldowns.")

		skill = "None"
		skill2 = "None"
		try:
			if userinfo["class"] == "Rogue" or userinfo["class"] == "High Rogue":
				skill = "Parry"
			elif userinfo["class"] == "Mesmer" or userinfo["class"] == "Adept Mesmer":
				skill = "Distort"
			elif userinfo["class"] == "Necromancer" or userinfo["class"] == "Developed Necromancer":
				skill = "Reap"
			elif userinfo["class"] == "Elementalist" or userinfo["class"] == "Adequate Elementalist":
				skill = "Overload"
			elif userinfo["class"] == "Paladin" or userinfo["class"] == "Grand Paladin":
				skill = "Fusillade"
			elif userinfo["class"] == "Samurai" or userinfo["class"] == "Master Samurai":
				skill = "Protrude"
			elif userinfo["class"] == "Ranger" or userinfo["class"] == "Skilled Ranger":
				skill = "Strike"
			elif userinfo["class"] == "Assassin" or userinfo["class"] == "Night Assassin":
				skill = "Corrupt"
		except:
			pass
		try:
			if userinfo["class"] == "High Rogue":
				skill2 = "Rupture"
			elif userinfo["class"] == "Adept Mesmer":
				skill2 = "Warp"
			elif userinfo["class"] == "Developed Necromancer":
				skill2 = "Arise"
			elif userinfo["class"] == "Adequate Elementalist":
				skill2 = "Surge"
			elif userinfo["class"] == "Master Samurai":
				skill2 = "Slice"
			elif userinfo["class"] == "Grand Paladin":
				skill2 = "Blockade"
			elif userinfo["class"] == "Night Assassin":
				skill2 = "Sneak"
			elif userinfo["class"] == "Skilled Ranger":
				skill2 = "Snipe"
		except:
			pass
		embed = discord.Embed(color=discord.Colour(0xffffff))
		embed.set_author(name="{} Cooldown list!".format(userinfo["name"]), icon_url=user.avatar_url)
		try:
			curr_time = time.time()
			delta = float(curr_time) - float(userinfo["mine_block"])

			cooldowntime = 600

			if userinfo["role"] == "patreon3":
				cooldowntime = 480

			if userinfo["role"] == "patreon4":
				cooldowntime = 300

			if delta >= cooldowntime and delta > 0:
				embed.add_field(name="Mine", value="<:Pickaxe:573574740640530471> You can mine again!\n\n_ _",
								inline=False)
			else:
				seconds = cooldowntime - delta
				m, s = divmod(seconds, 60)
				h, m = divmod(m, 60)
				embed.add_field(name="Mine", value=":hourglass: You can't mine for another  " + str(
					round(m)) + " minutes and " + str(round(s)) + " seconds.\n\n_ _", inline=False)
		except:
			pass
		try:
			curr_time = time.time()
			delta = float(curr_time) - float(userinfo["chop_block"])

			cooldowntime = 600

			if userinfo["role"] == "patreon3":
				cooldowntime = 480
			if userinfo["role"] == "patreon4":
				cooldowntime = 300

			if delta >= cooldowntime and delta > 0:
				embed.add_field(name="Chop", value="<:Axe:573574740220969007> You can chop again!\n\n_ _", inline=False)
			else:
				seconds = cooldowntime - delta
				m, s = divmod(seconds, 60)
				h, m = divmod(m, 60)
				embed.add_field(name="Chop", value=":hourglass: You can't chop for another  " + str(
					round(m)) + " minutes and " + str(round(s)) + " seconds.\n\n_ _", inline=False)
		except:
			pass
		try:
			if userinfo["sawmill"] == "True":
				curr_time = time.time()
				delta = float(curr_time) - float(userinfo["saw_block"])

				cooldowntime = 1200

				if userinfo["role"] == "patreon3":
					cooldowntime = 960
				if userinfo["role"] == "patreon4":
					cooldowntime = 600

				if delta >= cooldowntime and delta > 0:
					embed.add_field(name="saw", value=":carpentry_saw: You can saw again!\n\n_ _", inline=False)
				else:
					seconds = cooldowntime - delta
					m, s = divmod(seconds, 60)
					h, m = divmod(m, 60)
					embed.add_field(name="saw", value=":hourglass: You can't saw for another  " + str(
						round(m)) + " minutes and " + str(round(s)) + " seconds.\n\n_ _", inline=False)
		except:
			pass
		try:
			if userinfo["masonry"] == "True":
				curr_time = time.time()
				delta = float(curr_time) - float(userinfo["mason_block"])

				cooldowntime = 1200

				if userinfo["role"] == "patreon3":
					cooldowntime = 960
				if userinfo["role"] == "patreon4":
					cooldowntime = 600

				if delta >= cooldowntime and delta > 0:
					embed.add_field(name="mason", value=":hammer_pick: You can make bricks again!\n\n_ _", inline=False)
				else:
					seconds = cooldowntime - delta
					m, s = divmod(seconds, 60)
					h, m = divmod(m, 60)
					embed.add_field(name="mason", value=":hourglass: You can't mason for another  " + str(
						round(m)) + " minutes and " + str(round(s)) + " seconds.\n\n_ _", inline=False)
		except:
			pass
		try:
			if userinfo["smeltery"] == "True":
				curr_time = time.time()
				delta = float(curr_time) - float(userinfo["smelt_block"])

				cooldowntime = 1200

				if userinfo["role"] == "patreon3":
					cooldowntime = 960
				if userinfo["role"] == "patreon4":
					cooldowntime = 600

				if delta >= cooldowntime and delta > 0:
					embed.add_field(name="smelt", value=":hammer: You can smelt again!\n\n_ _", inline=False)
				else:
					seconds = cooldowntime - delta
					m, s = divmod(seconds, 60)
					h, m = divmod(m, 60)
					embed.add_field(name="smelt", value=":hourglass: You can't smelt for another  " + str(
						round(m)) + " minutes and " + str(round(s)) + " seconds.\n\n_ _", inline=False)
		except:
			pass
		try:
			if userinfo["trap"] >= 1:
				curr_time = time.time()
				delta = float(curr_time) - float(userinfo["trap_block"])

				cooldowntime = 3600

				if userinfo["role"] == "patreon3":
					cooldowntime = 2880
				if userinfo["role"] == "patreon4":
					cooldowntime = 1800

				if delta >= cooldowntime and delta > 0:
					embed.add_field(name="Traps", value="You can check your traps again!!\n\n_ _", inline=False)
				else:
					seconds = cooldowntime - delta
					m, s = divmod(seconds, 60)
					h, m = divmod(m, 60)
					embed.add_field(name="Traps", value=":hourglass: You can't check your traps for another  " + str(
						round(m)) + " minutes and " + str(round(s)) + " seconds.\n\n_ _", inline=False)
		except:
			pass
		try:
			staytime = 600

			curr_time = time.time()
			echo = float(curr_time) - float(userinfo["trader_time"])

			if echo <= staytime and echo > 0:
				seconds = staytime - echo
				m, s = divmod(seconds, 60)
				embed.add_field(name="Trader", value="<:Gold:639484869809930251> Trader will stay for another " + str(round(m)) + " Minutes and " + str(round(s)) + " Seconds\n\n_ _", inline=False)
				
			else:
				curr_time = time.time()
				delta = float(curr_time) - float(userinfo["trader_block"])

				cooldowntime = 28800

				if userinfo["role"] == "patreon3":
					cooldowntime = 23040
				if userinfo["role"] == "patreon4":
					cooldowntime = 14400

				if delta >= cooldowntime and delta > 0:
					embed.add_field(name="Trader", value="<:Gold:639484869809930251> You can Find a new trader!\n\n_ _", inline=False)

				else:
					seconds = cooldowntime - delta
					m, s = divmod(seconds, 60)
					h, m = divmod(m, 60)
					embed.add_field(name="Trader", value=":hourglass: Trader is away for another " + str(round(h)) + " Hours, " + str(round(m)) + " Minutes and " + str(round(s)) + " Seconds\n\n_ _", inline=False)
		except:
				pass
		try:
			curr_time = time.time()
			delta = float(curr_time) - float(userinfo["vote_block"])

			if delta >= 43200.0 and delta > 0:
				embed.add_field(name="Vote", value="<:TimeReduction:639447293271080982> You can vote again!\n\n_ _",
								inline=False)
			else:
				seconds = 43200 - delta
				m, s = divmod(seconds, 60)
				h, m = divmod(m, 60)
				embed.add_field(name="Vote",
								value=":hourglass: You can't vote for another  " + str(round(h)) + " hours, " + str(
									round(m)) + " minutes and " + str(round(s)) + " seconds.\n\n_ _", inline=False)
		except:
			pass
		try:
			curr_time = time.time()
			delta = float(curr_time) - float(userinfo["daily_block"])

			if delta >= 86400.0 and delta > 0:
				embed.add_field(name="Daily", value="<:Timer:639447292444934155> You can get your daily again!\n\n_ _",
								inline=False)
			else:
				seconds = 86400 - delta
				m, s = divmod(seconds, 60)
				h, m = divmod(m, 60)
				embed.add_field(name="Daily", value=":hourglass: You can't get your daily for another  " + str(
					round(h)) + " hours, " + str(round(m)) + " minutes and " + str(round(s)) + " seconds.\n\n_ _",
								inline=False)
		except:
			pass
		try:
			if not userinfo["role"] == "Player":
				curr_time = time.time()
				delta = float(curr_time) - float(userinfo["monthlyrewards"])

				if delta >= 2505600.0 and delta > 0:
					embed.add_field(name="Patreon Rewards!",
									value="<:TimeReduction:639447293271080982> You can claim your monthly rewards again!\n\n_ _",
									inline=False)
				else:
					seconds = 2505600 - delta
					m, s = divmod(seconds, 60)
					h, m = divmod(m, 60)
					d, h = divmod(h, 24)
					embed.add_field(name="Patreon Rewards!",
									value=":hourglass: You can't claim your monthly rewards for another \n" + str(
										round(d)) + " Days, " + str(round(h)) + " hours, " + str(
										round(m)) + " minutes and " + str(round(s)) + " seconds.\n\n_ _", inline=False)
		except:
			pass

		try:
			if 30 <= userinfo["lvl"] <= 90:
				try:
					embed.add_field(name="**{}**".format(skill),
									value="is on a **{} turn** cooldown.".format(userinfo["SkillCooldown1"]),
									inline=False)
				except:
					embed.add_field(name="**Skill 1**",
									value="is on a **{} turn** cooldown.".format(userinfo["SkillCooldown1"]),
									inline=False)
					pass
		except:
			pass
		try:
			if userinfo["lvl"] >= 90:
				try:
					embed.add_field(name="**{}**".format(skill),
									value="is on a **{} turn** cooldown.".format(userinfo["SkillCooldown1"]),
									inline=False)
				except:
					embed.add_field(name="**Skill 1**",
									value="is on a **{} turn** cooldown.".format(userinfo["SkillCooldown1"]),
									inline=False)
					pass
				try:
					embed.add_field(name="**{}**".format(skill2),
									value="is on a **{} turn** cooldown.".format(userinfo["SkillCooldown2"]),
									inline=False)
				except:
					embed.add_field(name="**Skill 2**",
									value="is on a **{} turn** cooldown.".format(userinfo["SkillCooldown2"]),
									inline=False)
					pass
		except:
			pass
		embed.add_field(name="_ _\nWant shorter cooldowns?",
						value="Become a [patreon](https://www.patreon.com/Solyx?fan_landing=true) to have shorter cooldowns and more rewards!")  # and have shorter cooldowns
		await ctx.send(embed=embed)


def setup(bot):
	n = cooldowns(bot)
	bot.add_cog(n)
