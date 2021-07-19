import discord
import os
import logging
from discord.ext import commands
import traceback
import sys

logging.basicConfig(level=logging.INFO)

# Replace token with your bot's personal token
TOKEN = ''

# Configure your bot command prefix. Default is a period '.'
COMMAND_PREFIX = '.'

client = commands.Bot(command_prefix=COMMAND_PREFIX)


# client.remove_command('help')


@client.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandNotFound):
        await context.send('**Command not found.**')
    elif isinstance(error, commands.MissingPermissions):
        await context.send('**You do not have permission to use this command.**')
    elif isinstance(error, commands.NSFWChannelRequired):
        await context.send('**Command can only be used in nsfw channel.**')
    elif isinstance(error, commands.BadArgument):
        await context.send('**Invalid arguments received for this command.**')
    else:
        # All other Errors not returned come here. And we can just print the default TraceBack.
        print('Ignoring exception in command {}:'.format(context.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        await context.send('**'+str(error)+'**')


@client.event
async def on_member_join(context):
    role = discord.utils.get(context.guild.roles, name='random')
    await context.add_roles(role)


# @client.command()
# async def help(context):
#     author = context.message.author
#     embed = discord.Embed(color=discord.Color.red())
#
#     embed.set_author(name='Available Commands')
#     embed.add_field(name='ping', value='Sends bot ping in ms', inline=False)
#
#     await author.send(embed=embed)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)
