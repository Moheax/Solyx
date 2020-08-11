from solyx import SolyxClient
import asyncio

if __name__ == '__main__':
  TOKEN = 'NDk1OTI4OTE0MDQ1MzA0ODQ3.D3kRGQ.MbcVySIomiC67lydfbSPfyAwc1o'     # bot token
  PREFIXES = ['>', '-', '<@495928914045304847>']      # default GLOBAL prefixes to use for Solyx. mentions and server-specific prefixes are handled by SolyxClient
  COGS = ['general', 'statistics',]    # Default cogs to load on start-up

  bot = SolyxClient(default_prefixes = PREFIXES, default_cogs = COGS)
  

  loop = asyncio.get_event_loop()
  loop.run_until_complete(bot.launch(TOKEN))