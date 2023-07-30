import discord
from discord import app_commands
from discord.ext import commands
# from config import token
token = 'MTEzNDUzNDIwNDczMDkxNjk0NA.GG4R8F.JOhlGifs3etRpzS_dptsLA7-y9YQ1ji7L3CqAE'



import logging
import os
import platform
import random
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context


"""	
Setup bot intents (events restrictions)
For more information about intents, please go to the following websites:
https://discordpy.readthedocs.io/en/latest/intents.html
https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents


Default Intents:
intents.bans = True
intents.dm_messages = True
intents.dm_reactions = True
intents.dm_typing = True
intents.emojis = True
intents.emojis_and_stickers = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_scheduled_events = True
intents.guild_typing = True
intents.guilds = True
intents.integrations = True
intents.invites = True
intents.messages = True # `message_content` is required to get the content of the messages
intents.reactions = True
intents.typing = True
intents.voice_states = True
intents.webhooks = True

Privileged Intents (Needs to be enabled on developer portal of Discord), please use them only if you need them:
intents.members = True
intents.message_content = True
intents.presences = True
"""

intents = discord.Intents.default()

"""
Uncomment this if you want to use prefix (normal) commands.
It is recommended to use slash commands and therefore not use prefix commands.

If you want to use prefix commands, make sure to also enable the intent below in the Discord developer portal.
"""
intents.message_content = True
intents.members = True

bot = Bot(
    command_prefix=commands.when_mentioned_or("!"),
    intents=intents,
    help_command=None,
)

# Setup both of the loggers


class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


logger = logging.getLogger("egregious")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())

# Add the handlers
logger.addHandler(console_handler)
bot.logger = logger


@bot.event
async def on_ready() -> None:
    """
    The code in this event is executed when the bot is ready.
    """
    bot.logger.info(f"Logged in as {bot.user.name}")
    bot.logger.info("-------------------")
    bot.logger.info("How to use:")
    bot.logger.info("1. Join a voice call")
    bot.logger.info("2. Right click yourself")
    bot.logger.info("3. App > Get Mod UwU")
    bot.logger.info("4. Enjoy Mod")
    status_task.start()
    await bot.tree.sync()


@tasks.loop(minutes=1.0)
async def status_task() -> None:
    """
    Setup the game status task of the bot.
    """
    statuses = ["with you!", "with Krypton!", "with humans!"]
    await bot.change_presence(status=discord.Status.offline, activity=discord.Game(random.choice(statuses)))

# role_id = 1001928373712453632
role_id = 1132788742483087411 # normal server

# @bot.tree.command()
# async def hello(ctx):
#     """Says hello!"""
#     await ctx.response.send_message(f'Hi, {ctx.user.mention}')
    

# @bot.tree.context_menu(name='Get Moderator')
# async def show_join_date(interaction: discord.Interaction, member: discord.Member):
#     # The format_dt function formats the date time into a human readable representation in the official client
#     await interaction.response.send_message(f'{member} joined at {discord.utils.format_dt(member.joined_at)}')

@bot.tree.context_menu(name='Get Mod UwU')
async def grant_mod(ctx, penis: discord.Member):
    role = ctx.guild.get_role(role_id)
    if role is not None:
        try:
            await ctx.user.add_roles(role)
            await ctx.response.send_message(f'{ctx.user.mention} claimed the "{role.name}" role, also watch date alvie')
            bot.logger.info(f'{ctx.user} claimed the "{role.name}" role, also watch date alvie')
        except discord.Forbidden:
            await ctx.response.send_message("I don't have the necessary permissions to give roles.")
    else:
        await ctx.response.send_message("The specified role was not found on this server.")

@bot.tree.context_menu(name='Remove all Mods')
async def remove_allmod(ctx, a: discord.Member):
	nomoremodders = []
	role = ctx.guild.get_role(role_id)
	for guild in bot.guilds:
		for member in guild.members:
			try:
				if member.get_role(role_id):
					await member.remove_roles(role)
					nomoremodders.append(member)
					bot.logger.info(f"Removing role from {member.name}...")
				else:
					pass
			except discord.Forbidden:
				await ctx.response.send_message("I don't have the necessary permissions to remove roles.")
			except discord.HTTPException:
				await ctx.response.send_message("An Error occured hahaaa")
		await ctx.response.send_message(f'Removed mod from {[m.name for m in nomoremodders]}')
		bot.logger.info(f'Removed mod from\n{[print(m) for m in nomoremodders]}')
#     a
# # @bot.tree.context_menu(name='Disable this bot for 20 minutes')
# # async def grant_mod(ctx, penis: discord.Member):
# #     role = ctx.guild.get_role(role_id)
# #     if role is not None:
# #         try:
# #             await ctx.user.add_roles(role)
# #             await ctx.response.send_message(f'{ctx.user.mention} claimed the "{role.name}" role, also watch date alvie')
# #         except discord.Forbidden:
# #             await ctx.response.send_message("I don't have the necessary permissions to give roles.")
# #     else:
# #         await ctx.response.send_message("The specified role was not found on this server.")
    # if role is not None:
    #     try:
    #         await ctx.user.add_roles(role)
    #         await ctx.response.send_message(f'You have been given the "{role.name}" role!')
    #     except discord.Forbidden:
    #         await ctx.response.send_message("I don't have the necessary permissions to give roles.")
    # else:
    #     await ctx.response.send_message("The specified role was not found on this server.")

@bot.event
async def on_message(message: discord.Message) -> None:
    """
    The code in this event is executed every time someone sends a message, with or without the prefix

    :param message: The message that was sent.
    """
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)
    bot.logger.info(f"[{message.author}]: {message.content}")

@bot.command()
async def ping(ctx):
    await ctx.send('pong')



@bot.event
async def on_command_completion(context: Context) -> None:
    """
    The code in this event is executed every time a normal command has been *successfully* executed.

    :param context: The context of the command that has been executed.
    """
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    if context.guild is not None:
        bot.logger.info(
            f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})"
        )
    else:
        bot.logger.info(
            f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs"
        )


@bot.event
async def on_command_error(context: Context, error) -> None:
    """
    The code in this event is executed every time a normal valid command catches an error.

    :param context: The context of the normal command that failed executing.
    :param error: The error that has been faced.
    """
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            description=f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            description="You are missing the permission(s) `"
            + ", ".join(error.missing_permissions)
            + "` to execute this command!",
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(
            description="I am missing the permission(s) `"
            + ", ".join(error.missing_permissions)
            + "` to fully perform this command!",
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            # We need to capitalize because the command arguments have no capital letter in the code.
            description=str(error).capitalize(),
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    else:
        raise error




bot.run(token)
      