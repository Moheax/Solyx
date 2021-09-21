import discord
from discord.ext import commands


import string
import aiohttp
import datetime
import asyncio
import random
import operator
import os
from requests import Request, Session
from random import choice as randchoice
from time import time

from utils.dataIO import fileIO
from utils.db import db
from utils.defaults import userdata, titledata, raiddata, battledata, guilddata

from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageOps, ImageFilter
from cogs.quests import _quest_check

class image(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.session = aiohttp.ClientSession()

	@commands.command(name="profile", pass_context=True, no_pm=True)
	@commands.cooldown(1, 12, commands.BucketType.user)
	async def _player_profile(self,ctx, *, user : discord.Member=None):
		
		"""Displays a user profile"""

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		if user == None:
			user = ctx.message.author
		channel = ctx.message.channel
		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return


		em1 = discord.Embed(description="<a:Solyxloadside:783364003367485460> Gathering profile image! <:Solyx:560809141766193152>", color=discord.Colour(0xffffff)) 
		try:
			await ctx.send(embed=em1)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
				return
			except:
				return
		
		await self.draw_profile(user)
		try:
			await ctx.trigger_typing()
		except discord.HTTPException:
			pass
		try:
			#await ctx.send("<:Solyx:560809141766193152> **| Profile for {}**".format(user.mention))
			#await ctx.send(channel, 'data/RPG/{}_profile.png'.format(user.id), content='<:Solyx:560809141766193152> **| Profile for {}**'.format(user.mention), filename="data/RPG/{}_profile.png")
			await channel.send(content='<:Solyx:560809141766193152> **| Profile for {}**'.format(user.mention),file=discord.File('data/RPG/{}_profile.png'.format(user.id)))
		except:
			return
		await asyncio.sleep(10)
		

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+user.name+"#"+user.discriminator,"checked their profile")
	async def draw_profile(self, user):

		default_avatar_url = str(user.avatar_url)
		# fonts
		font_file = 'data/fonts/font.ttf'
		font_bold_file = 'data/fonts/font_bold.ttf'
		font_unicode_file = 'data/fonts/unicode.ttf'

		name_fnt = ImageFont.truetype(font_bold_file, 22, encoding="utf-8")
		header_u_fnt = ImageFont.truetype(font_unicode_file, 40, encoding="utf-8")
		title_fnt = ImageFont.truetype(font_file, 18, encoding="utf-8")
		sub_header_fnt = ImageFont.truetype(font_bold_file, 14, encoding="utf-8")
		badge_fnt = ImageFont.truetype(font_bold_file, 10, encoding="utf-8")
		exp_fnt = ImageFont.truetype(font_bold_file, 13, encoding="utf-8")
		large_fnt = ImageFont.truetype(font_bold_file, 33, encoding="utf-8")
		level_label_fnt = ImageFont.truetype(font_bold_file, 40, encoding="utf-8")
		general_info_fnt = ImageFont.truetype(font_bold_file, 24, encoding="utf-8")
		general_info_u_fnt = ImageFont.truetype(font_unicode_file, 12, encoding="utf-8")
		hpfnt = ImageFont.truetype(font_bold_file, 26, encoding="utf-8")
		text_fnt = ImageFont.truetype(font_bold_file, 12, encoding="utf-8")
		text_u_fnt = ImageFont.truetype(font_unicode_file, 8, encoding="utf-8")
		credit_fnt = ImageFont.truetype(font_bold_file, 10, encoding="utf-8")

		def _write_unicode(text, init_x, y, font, unicode_font, fill):
			write_pos = init_x

			for char in text:
				if char.isalnum() or char in string.punctuation or char in string.whitespace:
					draw.text((write_pos, y), u"{}".format(char), font=font, fill=fill)
					write_pos += font.getsize(char)[0]
				else:
					draw.text((write_pos, y), u"{}".format(char), font=unicode_font, fill=fill)
					write_pos += unicode_font.getsize(char)[0]
						
		# get urls
		userinfo = db.users.find_one({ "_id": user.id })
		bg_url = userinfo["background"]
		profile_url = user.avatar_url

		# create image objects
		bg_image = Image
		profile_image = Image

		async with self.session.get(bg_url) as r:
			image = await r.content.read()
		with open('data/RPG/{}_temp_profile_bg.png'.format(user.id),'wb') as f:
			f.write(image)
		try:
			async with self.session.get(profile_url) as r:
				image = await r.content.read()
		except:
			async with self.session.get(default_avatar_url) as r:
				image = await r.content.read()
		with open('data/RPG/{}_temp_profile_profile.png'.format(user.id),'wb') as f:
			f.write(image)

		bg_image = Image.open('data/RPG/{}_temp_profile_bg.png'.format(user.id)).convert('RGBA')
		try:
			profile_image = Image.open('data/RPG/{}_temp_profile_profile.png'.format(user.id)).convert('RGBA')
		except:
			profile_image = Image.open('data/RPG/Solyx.png').convert('RGBA')

		# set canvas
		bg_color = (255,255,255,0)
		result = Image.new('RGBA', (1080, 700), bg_color)
		process = Image.new('RGBA', (1080, 700), bg_color)

		# draw
		draw = ImageDraw.Draw(process)

		# puts in background
		bg_image = bg_image.resize((960, 540), Image.ANTIALIAS)
		bg_image = bg_image.crop((0,0, 960, 540))
		bg_image = self._add_corners(bg_image, 25)
		result.paste(bg_image, (60,60))

		# draw filter
		draw.rectangle([(0,0),(1080, 700)], fill=(0,0,0,10))

		# draw transparent overlay
		vert_pos = 80
		left_pos = 80
		right_pos = 580
		title_height = 65
		gap = 2

		# determines rep section color
		rep_fill = (92,130,203,230)
		# determines badge section color, should be behind the titlebar
		badge_fill = (128,151,165,230)

		info_color = (255, 255 ,255, 90)


		# draw level circle
		multiplier = 8
		lvl_circle_dia = 150
		circle_left = 790
		circle_top = 450
		raw_length = lvl_circle_dia * multiplier

		# create mask
		mask = Image.new('L', (raw_length, raw_length), 0)
		draw_thumb = ImageDraw.Draw(mask)
		draw_thumb.ellipse((0, 0) + (raw_length, raw_length), fill = 255, outline = 0)

		# drawing level bar calculate angle
		start_angle = -90 # from top instead of 3oclock
		if not userinfo["exp"] == 0 and not userinfo["lvl"] == 0:
			angle = int(360 * (userinfo["exp"]/((userinfo["lvl"] + 1) * 165))) + start_angle
		else:
			angle = start_angle

		# level outline
		lvl_circle = Image.new("RGBA", (raw_length, raw_length))
		draw_lvl_circle = ImageDraw.Draw(lvl_circle)
		draw_lvl_circle.ellipse([0, 0, raw_length, raw_length], fill=(240,240,240,255), outline = (240,240,240,255))
		exp_fill = (240,240,240,255)
		draw_lvl_circle.pieslice([0, 0, raw_length, raw_length], start_angle, angle, fill=exp_fill, outline = (240,240,240,255))
		lvl_circle = lvl_circle.resize((lvl_circle_dia, lvl_circle_dia), Image.ANTIALIAS)
		lvl_bar_mask = mask.resize((lvl_circle_dia, lvl_circle_dia), Image.ANTIALIAS)
		process.paste(lvl_circle, (145, 295), lvl_circle)

		#draw.rectangle([(left_pos, vert_pos), (right_pos, 166)], fill=info_color) # Top profile bar
		#draw.rectangle([(75,280), (310, 370)], fill=info_color)
		#draw.rectangle([(75,385), (312, 465)], fill=info_color)
		#draw.rectangle([(328,280), (555, 370)], fill=info_color)
		#draw.rectangle([(328,385), (555, 465)], fill=info_color)

		# Info white under wave
		draw.rectangle([(60, 390), (1019, 580)], fill=(255,255,255))

		# Bottom curve fix
		expfix = "https://i.imgur.com/hmT9MoI.png"
		async with self.session.get(expfix) as r:
			image = await r.content.read()
		with open('data/RPG/{}_temp_expfix.png'.format(user.id),'wb') as f:
			f.write(image)
		expfix_image = Image.open('data/RPG/{}_temp_expfix.png'.format(user.id)).convert('RGBA')
		expfix_image = expfix_image.resize((960, 20), Image.ANTIALIAS)
		expfix_image = self._add_corners(expfix_image, 20)
		process.paste(expfix_image, (60, 580), expfix_image)

		# Wave
		wave1 = "https://i.imgur.com/ugYC2ZW.png"
		async with self.session.get(wave1) as r:
			image = await r.content.read()
		with open('data/RPG/{}_temp_wave1.png'.format(user.id),'wb') as f:
			f.write(image)
		wave1_image = Image.open('data/RPG/{}_temp_wave1.png'.format(user.id)).convert('RGBA')
		wave1_image = wave1_image.resize((960, 110), Image.ANTIALIAS)
		process.paste(wave1_image, (60, 280), wave1_image)

		# Exp bar wave
		wave2 = "https://i.imgur.com/vawPyAJ.png"
		async with self.session.get(wave2) as r:
			image = await r.content.read()
		with open('data/RPG/{}_temp_wave2.png'.format(user.id),'wb') as f:
			f.write(image)
		wave2_image = Image.open('data/RPG/{}_temp_wave2.png'.format(user.id)).convert('RGBA')
		wave2_image = wave2_image.resize((960, 110), Image.ANTIALIAS)
		if not userinfo["exp"] == 0 and not userinfo["lvl"] == 0:
			expbar = int(960 * (userinfo["exp"]/((userinfo["lvl"] + 1) * 165)))
		else:
			expbar = 1
		waveexp = wave2_image.crop((0, 0, expbar, 110)) # left, up, right, bottom
		process.paste(waveexp, (60, 280), waveexp)

		# Info boxes
		slot = "https://i.imgur.com/39kg1ir.png"
		async with self.session.get(slot) as r:
			image = await r.content.read()
		with open('data/RPG/{}_temp_slot.png'.format(user.id),'wb') as f:
			f.write(image)

		# Name
		slot0_image = Image.open('data/RPG/{}_temp_slot.png'.format(user.id)).convert('RGBA')
		slot0_image = slot0_image.resize((200, 50), Image.ANTIALIAS)
		process.paste(slot0_image, (120, 450))
		# Level
		slot1_image = Image.open('data/RPG/{}_temp_slot.png'.format(user.id)).convert('RGBA')
		slot1_image = slot1_image.resize((140, 30), Image.ANTIALIAS)
		process.paste(slot1_image, (150, 500))
		# Title
		slot2_image = Image.open('data/RPG/{}_temp_slot.png'.format(user.id)).convert('RGBA')
		slot2_image = slot2_image.resize((180, 30), Image.ANTIALIAS)
		process.paste(slot2_image, (130, 550))
		# Class
		slot3_image = Image.open('data/RPG/{}_temp_slot.png'.format(user.id)).convert('RGBA')
		slot3_image = slot3_image.resize((200, 50), Image.ANTIALIAS)
		process.paste(slot3_image, (350, 450))
		# Race
		slot4_image = Image.open('data/RPG/{}_temp_slot.png'.format(user.id)).convert('RGBA')
		slot4_image = slot4_image.resize((200, 50), Image.ANTIALIAS)
		process.paste(slot4_image, (350, 500))
		# Gold
		slot5_image = Image.open('data/RPG/{}_temp_slot.png'.format(user.id)).convert('RGBA')
		slot5_image = slot5_image.resize((200, 50), Image.ANTIALIAS)
		process.paste(slot5_image, (550, 450))
		# Exp
		slot6_image = Image.open('data/RPG/{}_temp_slot.png'.format(user.id)).convert('RGBA')
		slot6_image = slot6_image.resize((200, 50), Image.ANTIALIAS)
		process.paste(slot6_image, (550, 500))
		# Weapon
		slot7_image = Image.open('data/RPG/{}_temp_slot.png'.format(user.id)).convert('RGBA')
		slot7_image = slot7_image.resize((200, 50), Image.ANTIALIAS)
		process.paste(slot7_image, (750, 450))
		# Armor
		slot8_image = Image.open('data/RPG/{}_temp_slot.png'.format(user.id)).convert('RGBA')
		slot8_image = slot8_image.resize((200, 50), Image.ANTIALIAS)
		process.paste(slot8_image, (750, 500))

		# Profile picture
		total_gap = 10
		border = int(total_gap/2)
		profile_size = lvl_circle_dia - total_gap
		raw_length = profile_size * multiplier

		output = ImageOps.fit(profile_image, (raw_length, raw_length), centering=(0.5, 0.5))
		output = output.resize((profile_size, profile_size), Image.ANTIALIAS)
		mask = mask.resize((profile_size, profile_size), Image.ANTIALIAS)
		profile_image = profile_image.resize((profile_size, profile_size), Image.ANTIALIAS)
		process.paste(profile_image, (150, 300), mask)

		# Info text color vars
		white_color = (240,240,240,255)
		light_color = (160,160,160,255)

		"""# determine info text color
		dark_text = (35, 35, 35, 230)
		info_text_color = self._contrast(info_color, light_color, dark_text)"""

		hptext = "{} health".format(userinfo["health"])
		draw.text((self._center(1780, 120, hptext, hpfnt), 80), hptext, font=hpfnt, fill=white_color) # Health

		namestuff1 = self._name(user, 12)
		namestuff2 = self._truncate_text(namestuff1, 12)
		namestuff3 = self._center(215, 280, namestuff2 , header_u_fnt)
		_write_unicode(namestuff2, namestuff3, 460, level_label_fnt, header_u_fnt, white_color) # NAME

		lvl_text = "LEVEL {}".format(userinfo["lvl"])
		draw.text((self._center(280, 158, lvl_text, general_info_fnt), 505), lvl_text,  font=general_info_fnt, fill=(white_color[0],white_color[1],white_color[2],255)) # Level

		titletxt = "{}".format(userinfo["title"])
		titletext = self._truncate_text(titletxt, 15)
		draw.text((self._center(280, 158, titletext, general_info_fnt), 556), titletext,  font=general_info_fnt, fill=(white_color[0],white_color[1],white_color[2],255)) # Level

		classs = userinfo["class"]
		classtxt = "Class: {}".format(classs)
		classtext = self._truncate_text(classtxt, 19)
		draw.text((370, 465), classtext,  font=general_info_fnt, fill=white_color) # Class

		racee = userinfo["race"]
		racetxt = "Race: {}".format(racee)
		racetext = self._truncate_text(racetxt, 19)
		draw.text((370, 515), racetext,  font=general_info_fnt, fill=white_color) # Race

		gold = userinfo["gold"]
		goldtxt = "Gold: {}".format(gold)
		goldtext = self._truncate_text(goldtxt, 19)
		draw.text((570, 465), goldtext,  font=general_info_fnt, fill=white_color) # Gold

		expp = "Exp: {}".format(userinfo["exp"])
		exptxt = expp
		exptext = self._truncate_text(exptxt, 19)
		draw.text((570, 515), exptext,  font=general_info_fnt, fill=white_color) # Exp

		if not userinfo["equip"] == "None":
			weaponn = userinfo["equip"]["name"]
		else:
			weaponn = "None"
		weapontxt = "Weapon: {}".format(weaponn)
		weapontext = self._truncate_text(weapontxt, 19)
		draw.text((770, 465), weapontext,  font=general_info_fnt, fill=white_color) # Weapon

		if not userinfo["wearing"] == "None":
			wearingg = userinfo["wearing"]["name"]
		else:
			wearingg = "None"
		wearingtxt = "Armor: {}".format(wearingg)
		wearingtext = self._truncate_text(wearingtxt, 19)
		draw.text((770, 515), wearingtext,  font=general_info_fnt, fill=white_color) # Weapon

		"""guildd = "-"
		s_rank_txt = self._truncate_text(guildd, 19)
		expp = "{}".format(userinfo["exp"])
		s_exp_txt = expp

		killss = userinfo["enemieskilled"]
		s_kills_txt = "{}".format(killss)
		deathss = userinfo["deaths"]
		s_deaths_txt = "{}".format(deathss)"""

		# Badges
		# get rank/badge images
		rank1star = "https://i.imgur.com/AF8wOcM.png"
		rank2star = "https://i.imgur.com/EWUIg1u.png"
		rank3star = "https://i.imgur.com/emud1Yj.png"

		# get user rank
		userrank = int("{}".format(await self._find_rank(user)))

		if userrank == 1 or userrank == 2 or userrank == 3:
			# create image object
			rs3 = Image
			async with self.session.get(rank3star) as r:
				image = await r.content.read()
			with open('data/RPG/{}_temp_profile_badge.png'.format(user.id),'wb') as f:
				f.write(image)
			rs3_image = Image.open('data/RPG/{}_temp_profile_badge.png'.format(user.id)).convert('RGBA')
			# apply badge
			badge_image = rs3_image.resize((100, 100), Image.ANTIALIAS)
			process.paste(badge_image, (900, 330), badge_image)

		elif userrank == 4 or userrank == 5 or userrank == 6 or userrank == 7 or userrank == 8 or userrank == 9 or userrank == 10:
			# create image object
			rs2 = Image
			async with self.session.get(rank2star) as r:
				image = await r.content.read()
			with open('data/RPG/{}_temp_profile_badge.png'.format(user.id),'wb') as f:
				f.write(image)
			rs2_image = Image.open('data/RPG/{}_temp_profile_badge.png'.format(user.id)).convert('RGBA')
			# apply badge
			badge_image = rs2_image.resize((100, 100), Image.ANTIALIAS)
			process.paste(badge_image, (900, 330), badge_image)

		elif userrank >= 100:
			# create image object
			rs1 = Image
			async with self.session.get(rank1star) as r:
				image = await r.content.read()
			with open('data/RPG/{}_temp_profile_badge.png'.format(user.id),'wb') as f:
				f.write(image)
			rs1_image = Image.open('data/RPG/{}_temp_profile_badge.png'.format(user.id)).convert('RGBA')
			# apply badge
			badge_image = rs1_image.resize((100, 100), Image.ANTIALIAS)
			process.paste(badge_image, (900, 330), badge_image)

		result = Image.alpha_composite(result, process)
		result.save('data/RPG/{}_profile.png'.format(user.id),'PNG', quality=100)

		# remove images
		try:
			os.remove('data/RPG/{}_temp_profile_bg.png'.format(user.id))
		except:
			pass
		try:
			os.remove('data/RPG/{}_temp_profile_profile.png'.format(user.id))
		except:
			pass
		try:
			os.remove('data/RPG/{}_temp_profile_badge.png'.format(user.id))
		except:
			pass
		try:
			os.remove('data/RPG/{}_temp_slot.png'.format(user.id))
		except:
			pass
		try:
			os.remove('data/RPG/{}_temp_wave1.png'.format(user.id))
		except:
			pass
		try:
			os.remove('data/RPG/{}_temp_wave2.png'.format(user.id))
		except:
			pass
		try:
			os.remove('data/RPG/{}_temp_expfix.png'.format(user.id))
		except:
			pass

		


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

	# returns color that contrasts better in background
	def _contrast(self, bg_color, color1, color2):
		color1_ratio = self._contrast_ratio(bg_color, color1)
		color2_ratio = self._contrast_ratio(bg_color, color2)
		if color1_ratio >= color2_ratio:
			return color1
		else:
			return color2

	def _luminance(self, color):
		# convert to greyscale
		luminance = float((0.2126*color[0]) + (0.7152*color[1]) + (0.0722*color[2]))
		return luminance

	def _contrast_ratio(self, bgcolor, foreground):
		f_lum = float(self._luminance(foreground)+0.05)
		bg_lum = float(self._luminance(bgcolor)+0.05)

		if bg_lum > f_lum:
			return bg_lum/f_lum
		else:
			return f_lum/bg_lum

	# returns a string with possibly a nickname
	def _name(self, user, max_length):
		if user.name == user.display_name:
			return user.name
		else:
			return "{}".format(self._truncate_text(user.name, max_length - 3), max_length)

	async def _add_dropshadow(self, image, offset=(4,4), background=0x000, shadow=0x0F0, border=3, iterations=5):
		totalWidth = image.size[0] + abs(offset[0]) + 2*border
		totalHeight = image.size[1] + abs(offset[1]) + 2*border
		back = Image.new(image.mode, (totalWidth, totalHeight), background)

		# Place the shadow, taking into account the offset from the image
		shadowLeft = border + max(offset[0], 0)
		shadowTop = border + max(offset[1], 0)
		back.paste(shadow, [shadowLeft, shadowTop, shadowLeft + image.size[0], shadowTop + image.size[1]])

		n = 0
		while n < iterations:
			back = back.filter(ImageFilter.BLUR)
			n += 1

		# Paste the input image onto the shadow backdrop
		imageLeft = border - min(offset[0], 0)
		imageTop = border - min(offset[1], 0)
		back.paste(image, (imageLeft, imageTop))
		return back

	def _truncate_text(self, text, max_length):
		if len(text) > max_length:
			if text.strip('$').isdigit():
				text = int(text.strip('$'))
				return "${:.2E}".format(text)
			return text[:max_length-3] + "..."
		return text

	def _center(self, start, end, text, font):
		dist = end - start
		width = font.getsize(text)[0]
		start_pos = start + ((dist-width)/2)
		return int(start_pos)

#				- - - - B O R I N G   P A R T - - - -

	async def on_message(self, message):
		await self._handle_on_message(message)

	async def _handle_on_message(self, message):
		user = message.author
		# creates user if doesn't exist
		await self._create_user(user)

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
	n = image(bot)
	bot.add_cog(n)