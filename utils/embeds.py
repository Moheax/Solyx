import inspect

from discord.ext.commands.formatter import HelpFormatter, Paginator
from discord.ext.commands.core import Command
from discord import Embed
from datetime import datetime
from cogs.utils.colors import BOT
from cogs.utils.chat_formatting import inline_list


class Formatter(HelpFormatter):
	def __init__(self):
		super().__init__()

	"""Override for the default format method.
	"""
	def format(self):
		self._paginator = Paginator()

		description = self.command.description if not self.is_cog() else None

		if description:
			# <description> portion
			self._paginator.add_line(description, empty=True)

		if isinstance(self.command, Command):
			# <signature portion>
			signature = self.get_command_signature()
			self._paginator.add_line(signature, empty=True)

			# end it here if it's just a regular command
			if not self.has_subcommands():
				self._paginator.close_page()
				return self._paginator.pages

		max_width = self.max_name_size

		self._paginator.add_line('Commands:')
		self._add_subcommands_to_page(max_width, self.filter_command_list())

		self._paginator.add_line()
		return self._paginator.pages


class RichEmbed(Embed):
	def __init__(self, ctx, **kwargs):
		message = ctx.message
		bot = ctx.bot
		self.set_footer(text="Requested by: {}".format(message.author.name),
						icon_url=message.author.avatar_url)
		self.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

		if kwargs['color'] is 'bot':
			kwargs['color'] = BOT
		elif kwargs['color'] is 'author':
			kwargs['color'] = message.author.colour

		super().__init__(**kwargs, timestamp=datetime.utcnow(), type='rich')

	# You can ignore this.
	def __len__(self):
		def clean(arr):
			return [v for v in arr if v]

		values = ([f.name for f in self.fields] + 
				  [f.value for f in self.fields] + 
				  [self.title, self.description, self.author.name, self.footer.text])
		
		return sum(clean([len(v) for v in values]))


class HelpEmbed(RichEmbed):
	"""Basic embed for the help command, 
	returned when [p]help is called (without any arguments)
	"""
	def __init__(self, ctx):
		bot = ctx.bot
		msg = ctx.message
		g_prefixes = ",  ".join(inline_list(bot.settings.prefixes))
		s_prefixes = ",  ".join(inline_list(bot.settings.get_server_prefixes(msg.server)))
		s_prefixes = s_prefixes if s_prefixes != g_prefixes else "--/--"

		cogs = [type(c).__name__ for c in bot.cogs.values()]
			
		super().__init__(ctx, title="Help",
						  description="""
									To get more info about a commands, use `{0}help <command>`
									For more information about the bot, use `{0}help`
									""".format(ctx.prefix),
						  color='bot')

		self.set_thumbnail(url=bot.user.avatar_url)
		self.add_field(name="Prefix", value=g_prefixes)
		self.add_field(name="Server Prefixes", value=s_prefixes)


class CmdHelpEmbed(RichEmbed):
	"""Help embed for bot commands"""
	def __init__(self, ctx, command):
		formatter = Formatter()

		longdoc = command.help
		base = command.full_parent_name.split(' ')[0]
		base_cmd = "{0}{1}".format(ctx.prefix, base) if base else '--/--'

		codeblock = "\n".join(formatter.format_help_for(ctx, command))

		super().__init__(ctx, title="Help",
							  description=longdoc,
							  color='bot')

		self.add_field(name="Base Command:", value=base_cmd)
		self.add_field(name="Command Usage:", value=codeblock, inline=False)
		
class CmdUsageEmbed(RichEmbed):
	"""Command Usage embed"""
	def __init__(self, ctx, command):
		formatter = Formatter()

		codeblock = "\n".join(formatter.format_help_for(ctx, command))

		super().__init__(ctx, title="Command Usage:",
							  description=codeblock,
							  color='bot')

class CogHelpEmbed(RichEmbed):
	"""Help embed for cogs"""
	def __init__(self, ctx, cog):
		formatter = Formatter()

		descrip = inspect.getdoc(cog)

		codeblock = "\n".join(formatter.format_help_for(ctx, cog))

		super().__init__(ctx, title="Help [{.__class__.__name__}]".format(cog),
							  description="""
										{0}
										{1}
										  """.format(descrip, codeblock),
							  color='bot')

CHANGELOG = ("+ The help command.")

class BotHelpEmbed(RichEmbed):
	"""Help embed for the bot itself"""
	def __init__(self, ctx):
		
		super().__init__(ctx, title="Help",
							  description="""
										Ara. is a multi-purpose Discord bot made by and for server owners.
										  """, color='bot')

		self.set_thumbnail(url=ctx.bot.user.avatar_url)