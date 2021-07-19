from discord.ext import commands


class Images(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def cultured(self, context):
        await context.send('https://i.kym-cdn.com/entries/icons/original/000/022/506/7c6.jpg')

    @commands.command()
    async def lewder(self, context):
        await context.send('https://i.kym-cdn.com/photos/images/facebook/000/901/438/5f4.jpg')

    @commands.command()
    async def loli(self, context):
        await context.send('https://i.imgur.com/ZVBLnPR.gif')

    @commands.command()
    async def yes(self, context):
        await context.send('https://i.imgur.com/Qgl3Q2K.gif')


def setup(client):
    client.add_cog(Images(client))
