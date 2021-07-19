import discord
from discord.ext import commands


class Bot(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game(name="with Master"))
        print('Bot is online.')

    @commands.command()
    async def ping(self, context):
        await context.send(f'**Latency: {round(self.client.latency * 1000)}ms**')

    @commands.command(help='Deletes recent bot messages (Default 100) | .clear 50')
    async def clear(self, context, limit=100):
        def is_bot(message):
            return message.author == self.client.user

        await context.channel.purge(check=is_bot, limit=limit)


def setup(client):
    client.add_cog(Bot(client))
