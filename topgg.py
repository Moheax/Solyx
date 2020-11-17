import dbl
import discord
from discord.ext import commands, tasks

import asyncio
import logging


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQ5NTkyODkxNDA0NTMwNDg0NyIsImJvdCI6dHJ1ZSwiaWF0IjoxNTk2OTg1NTUyfQ.eAogWCDxTv_qYa22RVr7uaQUB6dzWGVxnzRFypDXOcY' # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, webhook_path='/dblwebhook', webhook_auth='password', webhook_port=65001)

    # The decorator below will work only on discord.py 1.1.0+
    # In case your discord.py version is below that, you can use self.bot.loop.create_task(self.update_stats())



   

def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(TopGG(bot))