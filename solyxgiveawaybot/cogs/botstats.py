import asyncio
import os

import discord
from discord.ext import commands

from utils.checks import developer
from utils.db import db


class botstats(commands.Cog):
    """You can display your bot stats in your game status..."""

    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        message = "Watching our giveaways :D"
        activity = discord.Game(name=message)
        await self.bot.change_presence(status=discord.Status.online, activity=activity)

def setup(bot):

    bot.add_cog(botstats(bot))
