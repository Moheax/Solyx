import discord
from discord.ext import commands
import datetime
import asyncio
import os
import logging

from utils.chat_formatting import pagify
from utils.checks import developer
from utils.dataIO import dataIO
from utils.db import db

log = logging.getLogger("red.admin")


class admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._announce_msg = None
        self._announce_guild = None
        self._settings = dataIO.load_json('data/admin/settings.json')
        self._settable_roles = self._settings.get("ROLES", {})

    def _is_guild_locked(self):
        return self._settings.get("SERVER_LOCK", False)

    def _save_settings(self):
        dataIO.save_json('data/admin/settings.json', self._settings)

    def _set_guildlock(self, lock=True):
        self._settings["SERVER_LOCK"] = lock
        self._save_settings()

    @commands.command(pass_context=True, no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.check(developer)
    async def staffcommands(self, ctx):
        """Lists of commands for staff"""

        user = ctx.message.author

        userinfo = db.users.find_one({"_id": user.id})

        guild = ctx.guild

        channel = ctx.message.channel

        user = ctx.message.author

        now = datetime.datetime.now()

        current_time = now.strftime("%H:%M:%S")

        print(current_time + " | " + guild.name + " | " + channel.name + " | " + user.name + "#" + user.discriminator,
              "Has checked staff commands.")

        em = discord.Embed(color=discord.Colour(0xffffff))
        em.set_author(name="Solyx staff commands!", icon_url=user.avatar_url)
        em.add_field(name="\n_ _\n**\u27a4** -blacklist".format(ctx.prefix),
                     value="ban command for users, user cant play anymore.", inline=False)
        em.add_field(name="\n_ _\n**\u27a4** -give".format(ctx.prefix),
                     value="give users items roles race class anything (- amount subtracts)", inline=False)
        em.add_field(name="\n_ _\n**\u27a4** -clear".format(ctx.prefix), value="clear certain amount of text.",
                     inline=False)
        em.add_field(name="\n_ _\n**\u27a4** -dashboard".format(ctx.prefix), value="check bot / cog status",
                     inline=False)
        em.add_field(name="\n_ _\n**\u27a4** -cogs".format(ctx.prefix), value="check cog status", inline=False)
        em.add_field(name="\n_ _\n**\u27a4** -load / unload / reload".format(ctx.prefix),
                     value="load unload or reload cogs", inline=False)
        em.add_field(name="\n_ _\n**\u27a4** -py".format(ctx.prefix), value="run python code", inline=False)
        em.add_field(name="\n_ _\n**\u27a4** -shutdown".format(ctx.prefix), value="shut down the bot......",
                     inline=False)
        try:
            await ctx.send(embed=em)
        except:
            try:
                await ctx.send(":pencil2: | Please give me permissions to send embedded messages.")
            except:
                return

    @commands.command(pass_context=True)
    @commands.check(developer)
    async def announce(self, ctx, *, msg):
        """Announces a message to all guilds that a bot is in."""
        if self._announce_msg is not None:
            await ctx.send("<:Solyx:560809141766193152> | Already announcing something!")
        else:
            self._announce_msg = msg
            self._announce_guild = ctx.message.guild

    @commands.command(pass_context=True)
    @commands.check(developer)
    async def guildlock(self, ctx):
        """Toggles locking the current guild list, will not join others"""
        if self._is_guild_locked():
            self._set_guildlock(False)
            await ctx.send("Server list unlocked")
        else:
            self._set_guildlock()
            await ctx.send("Server list locked.")

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(developer)
    async def say(self, ctx, *, text):
        """Bot repeats what you tell it to, utility for scheduler."""
        channel = ctx.message.channel
        tosend = "<:Solyx:560809141766193152> | " + text
        try:
            await ctx.send(channel, tosend)
        except:
            return

        guild = ctx.guild

        channel = ctx.message.channel

        user = ctx.message.author

        now = datetime.datetime.now()

        current_time = now.strftime("%H:%M:%S")

        print(
            current_time + " | " + guild.name + " | " + channel.name + " | " + user.name + "#" + user.discriminator + "Has made me say something" + text)

    @commands.command(pass_context=True, hidden=True)
    @commands.check(developer)
    async def send(self, ctx, id, *, text):
        author = ctx.message.author

        target = discord.utils.get(self.bot.get_all_members(), id=id)
        if target is None:
            target = self.bot.get_channel(id)
            if target is None:
                target = self.bot.get_guild(id)

        prefix = "<:Solyx:560809141766193152> | "
        payload = "{}{}".format(prefix, text)

        try:
            for page in pagify(payload, delims=[" ", "\n"], shorten_by=10):
                await self.bot.send_message(target, page)
        except discord.errors.Forbidden:
            log.debug("Forbidden to send message to {}".format(id))
            await ctx.send("<:Solyx:560809141766193152> | I don't have permissions to send the message!")
        except (discord.errors.NotFound, discord.errors.InvalidArgument):
            log.debug("{} not found!".format(id))
            await ctx.send("<:Solyx:560809141766193152> | I couldn't find that user/channel!")
        else:
            await ctx.send("<:Solyx:560809141766193152> | I successfully sent the message!")

    async def announcer(self, msg):
        guild_ids = map(lambda s: s.id, self.bot.guilds)
        for guild_id in guild_ids:
            if self != self.bot.get_cog('admin'):
                break
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                continue
            if guild == self._announce_guild:
                continue
            me = guild.me
            guild_owner = guild.owner
            notice_msg = "<:Solyx:560809141766193152> **| Announcement:**"
            end_msg = "- The Solyx team"
            await self.bot.send_message(guild_owner, notice_msg)
            await self.bot.send_message(guild_owner, msg)
            await self.bot.send_message(guild_owner, end_msg)
            await asyncio.sleep(1)

    async def announce_manager(self):
        while self == self.bot.get_cog('admin'):
            if self._announce_msg is not None:
                print("Found new announce message, announcing")
                await self.announcer(self._announce_msg)
                self._announce_msg = None
            await asyncio.sleep(1)

    async def guild_locker(self, guild):
        if self._is_guild_locked():
            await self.bot.leave_guild(guild)


def check_files():
    if not os.path.exists('data/admin/settings.json'):
        try:
            os.mkdir('data/admin')
        except FileExistsError:
            pass
        else:
            dataIO.save_json('data/admin/settings.json', {})


def setup(bot):
    check_files()
    n = admin(bot)
    bot.add_cog(n)
    bot.add_listener(n.guild_locker, "on_guild_join")
    bot.loop.create_task(n.announce_manager())
