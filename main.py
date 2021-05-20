from solyx import SolyxClient
import discord
import asyncio
intents = discord.Intents.default()
intents.reactions = True

if __name__ == '__main__':
    TOKEN = 'token'
    PREFIXES = ['>', '-', '<@495928914045304847>']      # default GLOBAL prefixes to use for Solyx. mentions and server-specific prefixes are handled by SolyxClient
    COGS = ['general', 'statistics',]    # Default cogs to load on start-up

    bot = SolyxClient(default_prefixes = PREFIXES, default_cogs = COGS, intents=intents)
  

    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.launch(TOKEN))
