import discord
import platform, asyncio, string, operator, textwrap
import random
import os, re, aiohttp
from random import choice as randchoice
from discord.ext import commands
from cogs.rpgutils.db import db
from cogs.rpgutils.defaults import serverdata, userdata
from cogs.utils import checks
from cogs.utils.chat_formatting import pagify
from cogs.utils.dataIO import fileIO
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

prefix = fileIO("data/red/settings.json", "load")['PREFIXES']

class wiki:
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True, aliases=["wikipedia"], no_pm=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def wiki(self, ctx, *, topic=None):
        if topic == None:
            title="Wiki topics"
            description="`elf`, `orc`, `phantasm`, `corrupted`, `fire golem`"
            footer="Command usage: {}wiki [subject].".format(ctx.prefix)

        elif topic == "elf":
            title="Elf"
            description="In the lush forested areas of east Solyx, the elves thrive. While their bodies are naturally slim, they are surprisingly strong and can easily hold their own in a fight. However, elves do not prioritize physical strength; instead favoring the charismatic members of society. While many things can be seen as status symbols to individual elf communities, the pointiness of their ears is the most common way an elf shows off their looks."
            footer="Submitted by (8ᘌꇤ⁐ꃳ 三#2369 | Submit your wiki acticle using {}server.".format(ctx.prefix)

        elif topic == "orc":
            title="Orc"
            description="To the far west of Solyx, deep into the cold and dangerous mountain ranges, lies the kingdom of the orc. This grand and heavily fortified city is home to the orcs. To survive the cold and harsh lands they live in, the orcs have to go through hellish training, starting from the day they can walk. Once they become of age, these fierce creatures will have been shaped up to be the pinnacle of raw physical strength, and combat prowess."
            footer="Submitted by Rideric#4935 | Submit your wiki acticle using {}server.".format(ctx.prefix)

        elif topic == "phantasm":
            title="Phantasm"
            description="The Phantasm has long protected The Forest. The Monks prayed and offered sacrifices to keep it satisfied. The Phantasm resides near hidden lakes throughout the forest, as the water is it's life source. As the praying monks became extinct it no longer has any peace. Whenever the Phantasm feels threatened it gathers dark clouds and density into an eerie storm. It uses it's long slithering body to smother its threats. And guides the lightning of the storm onto it's foes."
            footer="Submitted by AceTheBear223#4562 | Submit your wiki acticle using {}server.".format(ctx.prefix)

        elif topic == "corrupted" or topic == "the corrupted":
            title="The Corrupted"
            description="The Corrupted originally came from a relatively peaceful race of dragons. Their emerald green scales became a very wanted loot amongst adventurers. The adventurers betrayed the race it's trust and slaughtered almost all of the dragons. The survivors went into a frenzy. No longer able to tell any difference between living beings. The Corrupted kill blindly. Their snake like fangs have teared trough many houses and castles alike. Their horns grow as they kill, and their roaring can be heard from afar. Now they roam the ruins of Saker Keep."
            footer="Submitted by AceTheBear223#4562 | Submit your wiki acticle using {}server.".format(ctx.prefix)

        elif topic == "fire golem" or topic == "fire":
            title="Fire Golem"
            description="The fire golem's name speaks for itself. The golems arose from the depths of a volcano, summoned by an ancient group of druids to protect the Golden Temple. The golem's bodies are made from magnetized lava rock. built to withstand high pressure and has strong resistance against piercing attacks. Long have the golems been asleep. But the increase of wandering adventurers have woken them once more. The golems have no feelings and only one objective in mind. To kill tresspassers."
            footer="Submitted by AceTheBear223#4562 | Submit your wiki acticle using {}server.".format(ctx.prefix)

        try:
            em = discord.Embed(title=title, description=description, color=discord.Colour(0xffffff))
            em.set_footer(text=footer)
            await self.bot.say(embed=em)
        except:
            try:
                await self.bot.send_message(ctx.message.channel, "I cound't send the message.")
            except:
                return


def setup(bot):
    n = wiki(bot)
    bot.add_cog(n)