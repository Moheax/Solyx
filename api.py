import json

import aiohttp
import dbl
from discord.ext import commands, tasks


class api(commands.Cog):
    def __init__(self, bot):

        self.bot = bot
        self.topgg_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQ5NTkyODkxNDA0NTMwNDg0NyIsImJvdCI6dHJ1ZSwiaWF0IjoxNTk2OTg1NTUyfQ.eAogWCDxTv_qYa22RVr7uaQUB6dzWGVxnzRFypDXOcY'  # top.gg token

    @tasks.loop(seconds=1800)  # 30 min
    async def post(self):
        if not self.bot.post_wait:
            self.bot.post_wait = True

            guildcount = dbl.DBLClient(self.bot, self.token, autopost=True)

            topgg_url = 'https://top.gg/api/bots/BOT_ID/stats'
            topgg_data = {"shard_count": self.bot.shard_count, "server_count": guildcount}
            topgg_headers = {'Authorization': self.topgg_token, 'Content-Type': 'application/json'}
            try:
                async with aiohttp.ClientSession() as aioclient:
                    response = await aioclient.post(topgg_url, data=json.dumps(topgg_data), headers=topgg_headers)
            except:
                pass


def setup(bot):
    n = api(bot)
    bot.add_cog(n)
