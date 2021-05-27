from solyxsupport import SolyxSupportClient
import discord
import asyncio
intents = discord.Intents.default()
intents.reactions = True

if __name__ == '__main__':
    TOKEN = 'NTcwNTE4MTcxODY2MzY1OTUz.XMAWcw.X_zwzgutYO4f9j3L-m3ZC9QWe68'     # bot token old | NDk1OTI4OTE0MDQ1MzA0ODQ3.D3kRGQ.MbcVySIomiC67lydfbSPfyAwc1o
    PREFIXES = ['!', '<@570518171866365953>']      # default GLOBAL prefixes to use for Solyx. mentions and server-specific prefixes are handled by SolyxClient
    COGS = ['general', 'giveaway', 'botstats']    # Default cogs to load on start-up

    bot = SolyxSupportClient(default_prefixes = PREFIXES, default_cogs = COGS, intents=intents)
  

    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.launch(TOKEN))