import discord
import platform, asyncio, string, operator, textwrap
import random
import os, re, aiohttp
from random import choice as randchoice
from discord.ext import commands
from utils.db import db
from utils.defaults import guilddata, userdata
from utils import checks
from utils.chat_formatting import pagify
from utils.dataIO import fileIO
import math
try:
    from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageOps, ImageFilter
except:
    raise RuntimeError("Can't load pillow. Do 'pip3 install pillow'.")
try:
    import scipy
    import scipy.misc
    import scipy.cluster
except:
    pass


class wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True, aliases=["wikipedia"], no_pm=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def wiki(self, ctx, *, topic=None):
        guild = ctx.guild
       

        if topic == None:
            title="Wiki topics"
            description="`elf`, `orc`, `phantasm`, `corrupted`, `fire golem`, `test`, `Guild Bonus`"
            footer="Command usage: {}wiki [subject].".format(ctx.prefix)
            icon = guild.icon_url
        elif topic == "elf":
            title="Elf"
            description="In the lush forested areas of east Solyx, the elves thrive. While their bodies are naturally slim, they are surprisingly strong and can easily hold their own in a fight. However, elves do not prioritize physical strength; instead favoring the charismatic members of society. While many things can be seen as status symbols to individual elf communities, the pointiness of their ears is the most common way an elf shows off their looks."
            footer="Submitted by (8ᘌꇤ⁐ꃳ 三#2369\nSubmit your wiki acticle by sending a dm/message to @TheMaksoo#1212.".format(ctx.prefix)

        elif topic == "orc":
            title="Orc"
            description="To the far west of Solyx, deep into the cold and dangerous mountain ranges, lies the kingdom of the orc. This grand and heavily fortified city is home to the orcs. To survive the cold and harsh lands they live in, the orcs have to go through hellish training, starting from the day they can walk. Once they become of age, these fierce creatures will have been shaped up to be the pinnacle of raw physical strength, and combat prowess."
            footer="Submitted by Rideric#4935\nSubmit your wiki acticle by sending a dm/message to @TheMaksoo#1212.".format(ctx.prefix)

        elif topic == "phantasm":
            title="Phantasm"
            description="The Phantasm has long protected The Forest. The Monks prayed and offered sacrifices to keep it satisfied. The Phantasm resides near hidden lakes throughout the forest, as the water is it's life source. As the praying monks became extinct it no longer has any peace. Whenever the Phantasm feels threatened it gathers dark clouds and density into an eerie storm. It uses it's long slithering body to smother its threats. And guides the lightning of the storm onto it's foes."
            footer="Submitted by AceTheBear223#4562\nSubmit your wiki acticle by sending a dm/message to @TheMaksoo#1212.".format(ctx.prefix)

        elif topic == "corrupted" or topic == "the corrupted":
            title="The Corrupted"
            description="The Corrupted originally came from a relatively peaceful race of dragons. Their emerald green scales became a very wanted loot amongst adventurers. The adventurers betrayed the race it's trust and slaughtered almost all of the dragons. The survivors went into a frenzy. No longer able to tell any difference between living beings. The Corrupted kill blindly. Their snake like fangs have teared trough many houses and castles alike. Their horns grow as they kill, and their roaring can be heard from afar. Now they roam the ruins of Saker Keep."
            footer="Submitted by AceTheBear223#4562\nSubmit your wiki acticle by sending a dm/message to @TheMaksoo#1212.".format(ctx.prefix)

        elif topic == "fire golem" or topic == "fire":
            title="Fire Golem"
            description="**\u27a4 Health** - 30 to 50 \n**\u27a4 Damage** - 10 to 20 \n**\u27a4 Gold** - 18 to 21   \n**\u27a4 Exp** -4 \n \nThe fire golem's name speaks for itself. The golems arose from the depths of a volcano, summoned by an ancient group of druids to protect the Golden Temple. The golem's bodies are made from magnetized lava rock. built to withstand high pressure and has strong resistance against piercing attacks. Long have the golems been asleep. But the increase of wandering adventurers have woken them once more. The golems have no feelings and only one objective in mind. To kill tresspassers."
            footer="Submitted by AceTheBear223#4562\nSubmit your wiki acticle by sending a dm/message to @TheMaksoo#1212.".format(ctx.prefix)

        elif topic == "test" or topic == "testing":
            title="Test123"
            description="**\u27a4 Health** - 1 \n**\u27a4 Damage** - 2 \n**\u27a4 Gold** - 3 \n**\u27a4 Exp** -4 \n \n  yes sum text blabla big monster RAWR big mad long story \n"
            footer="Submitted by your mom **>:c**\nSubmit your wiki acticle by sending a dm/message to @TheMaksoo#1212.".format(ctx.prefix)
            icon = ('https://cdn.discordapp.com/attachments/750681506262810624/751520899848601620/unknown.png')

        elif topic == "guild bonus" or topic == "guildbonus":
            title= "Guild Bonus"
            description="The Guild bonus will apply to every killed mob.\nThe Guild Bonus is in the form of gold.\nThe Guild Bonus varies from 5 to 20 gold X Guildbonus multiplier. \n The gold get form a monster is its own random gold drop + guild bonus if the player is representing a guild."
            footer="submitted by TheMaksoo#1212\nSubmit your wiki acticle by sending a dm/message to @TheMaksoo#1212.".format(ctx.prefix)
            icon = ('https://cdn.discordapp.com/attachments/737821854680744017/751554397456040088/unknown.png')

        try:
            em = discord.Embed(title=title, description=description, color=discord.Colour(0xffffff))
            em.set_footer(text=footer)
            em.set_thumbnail(url=icon)
            await ctx.send(embed=em)
        except:
            try:
                await ctx.send(ctx.message.channel, "I cound't send the message.")
            except:
                return


def setup(bot):
    n = wiki(bot)
    bot.add_cog(n)