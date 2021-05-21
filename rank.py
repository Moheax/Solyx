import discord
from discord.ext import commands


import string
import aiohttp
import datetime
import asyncio
import random
import operator


from requests import Request, Session
from random import choice as randchoice
from time import time

from utils.dataIO import fileIO
from utils.db import db
from utils.defaults import userdata, titledata, raiddata, battledata, guilddata

from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageOps, ImageFilter
from cogs.quests import _quest_check

class rank(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.session = aiohttp.ClientSession(loop=self.bot.loop)

	@commands.cooldown(1, 12, commands.BucketType.user)
	@commands.command(name="rank", pass_context=True, no_pm=True)
	async def _player_rank(self,ctx, *, user : discord.Member=None):
		"""Displays a user rank"""
		if user == None:
			user = ctx.message.author
		channel = ctx.message.channel
		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send("<:Solyx:560809141766193152> | Please start your character using `-begin`")
			return
		await self.draw_profile(user)
		try:
			await ctx.trigger_typing()
		except discord.HTTPException:
			pass
		try:
			#await self.bot.send_file(channel, 'data/RPGR/{}_rank.png'.format(user.id), content='<:Solyx:560809141766193152> **| rank card for {}**'.format(user.mention), filename="Solyx.png")
			await channel.send(content='<:Solyx:560809141766193152> **| rank card for {}**'.format(user.mention),file=discord.File('data/RPGR/{}_rank.png'.format(user.id)))
			#try:
			#	os.remove('data/RPGR/{}_rank.png'.format(user.id))
			#except:
			#	await ctx.send("**ERROR | I can't send images here!**")
			#return
		except:
			return
		await asyncio.sleep(10)

		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has requested their rank!")

	async def draw_profile(self, user):

		# Fonts
		font_file = 'data/fonts/font.ttf'
		font_bold_file = 'data/fonts/font_bold.ttf'
		font_unicode_file = 'data/fonts/unicode.ttf'

		header_u_fnt = ImageFont.truetype(font_unicode_file, 40, encoding="utf-8")
		level_label_fnt = ImageFont.truetype(font_bold_file, 40, encoding="utf-8")
		general_info_fnt = ImageFont.truetype(font_bold_file, 24, encoding="utf-8")
		general_info_u_fnt = ImageFont.truetype(font_unicode_file, 12, encoding="utf-8")

		def _write_unicode(text, init_x, y, font, unicode_font, fill):
			write_pos = init_x
			for char in text:
				if char.isalnum() or char in string.punctuation or char in string.whitespace:
					draw.text((write_pos, y), u"{}".format(char), font=font, fill=fill)
					write_pos += font.getsize(char)[0]
				else:
					draw.text((write_pos, y), u"{}".format(char), font=unicode_font, fill=fill)
					write_pos += unicode_font.getsize(char)[0]

		# Vars
		userinfo = db.users.find_one({ "_id": user.id })
		bg_url = userinfo["background"]
		bg_image = Image

		async with self.session.get(bg_url) as r:
			image = await r.content.read()
		with open('data/RPGR/{}_temp_rank_bg.png'.format(user.id),'wb') as f:
			f.write(image)
		bg_image = Image.open('data/RPGR/{}_temp_rank_bg.png'.format(user.id)).convert('RGBA')

		# Canvas
		bg_color = (255,255,255,0)
		result = Image.new('RGBA', (900, 250), bg_color)
		process = Image.new('RGBA', (900, 250), bg_color)
		draw = ImageDraw.Draw(process)

		# Background
		bg_image = bg_image.resize((1080, 720), Image.ANTIALIAS)
		bg_image = bg_image.crop((0,0, 900, 250))
		bg_image = self._add_corners(bg_image, 20)
		result.paste(bg_image, (0,0))

		# Filter
		draw.rectangle([(0,0),(900, 250)], fill=(0,0,0,10))

		# Up and down (X and Y vars)
		expbar_y = 90
		textvalue_y = 170

		# I use this white image for the exp bar because it's easy
		whitefuq = "https://i.imgur.com/hmT9MoI.png"
		async with self.session.get(whitefuq) as r:
			image = await r.content.read()
		with open('data/RPGR/{}_temp_white.png'.format(user.id),'wb') as f:
			f.write(image)
		whiteboy = Image.open('data/RPGR/{}_temp_white.png'.format(user.id)).convert('RGBA')
		whiteboy = whiteboy.resize((900, 250), Image.ANTIALIAS)
		whiteboy = self._add_corners(whiteboy, 20)

		# EXP bar
		barthiccness = 15
		expbar = Image.open('data/RPGR/{}_temp_white.png'.format(user.id)).convert('RGBA')
		expbar = expbar.resize((880, barthiccness), Image.ANTIALIAS)
		if not userinfo["exp"] == 0 and not userinfo["lvl"] == 0:
			expamt = int(880 * (userinfo["exp"]/((userinfo["lvl"] + 1) * 3.5)))
		else:
			expamt = 1
		waveexp = expbar.crop((0, 0, expamt, barthiccness)) # left, up, right, bottom
		waveexp = self._add_corners(waveexp, 5)
		process.paste(waveexp, (10, expbar_y))

		# Info text color vars
		white_color = (240,240,240,255)
		light_color = (160,160,160,255)

		# % under exp bar
		percent = ((userinfo["exp"] + 1)/(((userinfo["lvl"] + 1) * 3.5)/100))
		percentage = "{}%".format(int(percent))
		draw.text((expamt + 5, expbar_y + 20), percentage, font=general_info_fnt, fill=white_color)

		# Name
		_write_unicode(self._name(user, 50), 20, 20, level_label_fnt, header_u_fnt, white_color)

		# Level
		lvl_text = "{}".format(userinfo["lvl"])
		draw.text((self._center(0, 450, lvl_text, level_label_fnt), textvalue_y), lvl_text,  font=level_label_fnt, fill=(white_color[0],white_color[1],white_color[2],255))

		draw.text((self._center(0, 450, "Level", general_info_fnt), textvalue_y + 35), "Level",  font=general_info_fnt, fill=(white_color[0],white_color[1],white_color[2],255))

		# Global rank
		getrank = await self._find_rank(user)
		rank_text = "#{}".format(getrank)
		draw.text((self._center(800, 900, rank_text, level_label_fnt), 20), rank_text,  font=level_label_fnt, fill=(white_color[0],white_color[1],white_color[2],255))

		#draw.text((self._center(0, 900, "rank", general_info_fnt), textvalue_y + 35), "rank",  font=general_info_fnt, fill=(white_color[0],white_color[1],white_color[2],255))

		# EXP have
		exphave_text = "{}".format(userinfo["exp"])
		draw.text((self._center(0, 900, exphave_text, level_label_fnt), textvalue_y), exphave_text,  font=level_label_fnt, fill=(white_color[0],white_color[1],white_color[2],255))

		draw.text((self._center(0, 900, "Current exp", general_info_fnt), textvalue_y + 35), "Current exp",  font=general_info_fnt, fill=(white_color[0],white_color[1],white_color[2],255))

		# EXP need
		expneeded = (((100) + (userinfo["lvl"] + 1) * 3.5) - userinfo["exp"])
		expneed_text = "{}".format(expneeded)
		draw.text((self._center(450, 900, expneed_text, level_label_fnt), textvalue_y), expneed_text,  font=level_label_fnt, fill=(white_color[0],white_color[1],white_color[2],255))

		draw.text((self._center(450, 900, "Next level up", general_info_fnt), textvalue_y + 35), "Next level up",  font=general_info_fnt, fill=(white_color[0],white_color[1],white_color[2],255))

		# Final image
		result = Image.alpha_composite(result, process)
		result.save('data/RPGR/{}_rank.png'.format(user.id),'PNG', quality=100)

		# Remove temp images
		try:
			os.remove('data/RPGR/{}_temp_rank_bg.png'.format(user.id))
		except:
			pass
		try:
			os.remove('data/RPGR/{}_temp_profile_profile.png'.format(user.id))
		except:
			pass
		try:
			os.remove('data/RPGR/{}_temp_white.png'.format(user.id))
		except:
			pass

	# Rounden an image
	def _add_corners(self, im, rad, multiplier = 6):
		raw_length = rad * 2 * multiplier
		circle = Image.new('L', (raw_length, raw_length), 0)
		draw = ImageDraw.Draw(circle)
		draw.ellipse((0, 0, raw_length, raw_length), fill=255)
		circle = circle.resize((rad * 2, rad * 2), Image.ANTIALIAS)

		alpha = Image.new('L', im.size, 255)
		w, h = im.size
		alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
		alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
		alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
		alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
		im.putalpha(alpha)
		return im

	# Returns a string with possibly a nickname
	def _name(self, user, max_length):
		if user.name == user.display_name:
			return user.name
		else:
			return "{}".format(self._truncate_text(user.name, max_length - 3), max_length)

	# Shorten a text if it's too long
	def _truncate_text(self, text, max_length):
		if len(text) > max_length:
			if text.strip('$').isdigit():
				text = int(text.strip('$'))
				return "${:.2E}".format(text)
			return text[:max_length-3] + "..."
		return text

	# Center a text
	def _center(self, start, end, text, font):
		dist = end - start
		width = font.getsize(text)[0]
		start_pos = start + ((dist-width)/2)
		return int(start_pos)

	# Find rank in db
	async def _find_rank(self, user):
		users = []

		for userinfo in db.users.find({}):
			try:
				userid = userinfo["_id"]
				users.append((userid, userinfo["lvl"]))
			except KeyError:
				pass
		sorted_list = sorted(users, key=operator.itemgetter(1), reverse=True)

		rank = 1
		for stats in sorted_list:
			if stats[0] == user.id:
				return rank
			rank+=1

def setup(bot):
	n = rank(bot)
	bot.add_cog(n)