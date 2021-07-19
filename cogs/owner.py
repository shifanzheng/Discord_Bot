from discord.ext import commands


class Owner(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.is_owner()
    @commands.command(name='load', hidden=True)
    async def load(self, ctx, cog: str):
        try:
            self.client.load_extension(f'cogs.{cog}')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.is_owner()
    @commands.command(name='unload', hidden=True)
    async def unload(self, ctx, cog: str):
        try:
            self.client.unload_extension(f'cogs.{cog}')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.is_owner()
    @commands.command(name='reload', hidden=True)
    async def reload(self, ctx, cog: str):
        try:
            self.client.unload_extension(f'cogs.{cog}')
            self.client.load_extension(f'cogs.{cog}')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')


def setup(client):
    client.add_cog(Owner(client))
