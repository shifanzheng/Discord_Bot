import discord
from discord.ext import commands


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.has_permissions(administrator=True)
    @commands.command(hidden=True)
    async def kick(self, context, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)

    @commands.has_permissions(administrator=True)
    @commands.command(hidden=True, help='Deletes messages from text channel | .purge 100')
    async def purge(self, context, lines: int):
        await context.channel.purge(limit=lines)

    @commands.has_permissions(administrator=True)
    @commands.command(hidden=True, help='Deletes messages from user (default 100) | .purge_user @User 100')
    async def purge_user(self, context, user: discord.User, limit=100):
        def is_message_author(message):
            return message.author == user

        await context.channel.purge(check=is_message_author, limit=limit)

    @purge.error
    async def purge_error(self, context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await context.send('Please specify messages to delete')


def setup(client):
    client.add_cog(Admin(client))
