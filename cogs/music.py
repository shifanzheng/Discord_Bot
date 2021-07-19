import discord
from discord.ext import commands
from youtube import YoutubeSearch, YTDLSource, YTDLError
import youtube_dl

youtube_dl.utils.bug_reports_message = lambda: ''


class Music(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')
        return True

    @commands.command(aliases=['youtube'],
                      help='Searches Youtube for videos and returns top 5 results | .yt fate')
    async def yt(self, context, *, search):
        result = YoutubeSearch(search, 5).videos

        embed = discord.Embed(color=discord.Color.red())
        embed.set_author(name='Youtube Search Results')
        embed.add_field(name='1. ' + result[0].get('title') + ' （' + result[0].get('duration') + '）',
                        value='http://www.youtube.com' + result[0].get('url_suffix'), inline=False),
        embed.add_field(name='2. ' + result[1].get('title') + ' （' + result[1].get('duration') + '）',
                        value='http://www.youtube.com' + result[1].get('url_suffix'), inline=False),
        embed.add_field(name='4. ' + result[3].get('title') + ' （' + result[3].get('duration') + '）',
                        value='http://www.youtube.com' + result[3].get('url_suffix'), inline=False),
        embed.add_field(name='3. ' + result[2].get('title') + ' （' + result[2].get('duration') + '）',
                        value='http://www.youtube.com' + result[2].get('url_suffix'), inline=False),
        embed.add_field(name='5. ' + result[4].get('title') + ' （' + result[4].get('duration') + '）',
                        value='http://www.youtube.com' + result[4].get('url_suffix'), inline=False)

        await context.send(embed=embed)

    @commands.command(help='Moves bot into specified channel or current user channel')
    async def move(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        voice_channel = channel or ctx.author.voice.channel
        voice_client = ctx.message.guild.voice_client
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await voice_client.voice.move_to(voice_channel)

    @commands.command(help='Adjust bot volume between 0 and 100 | .volume 50')
    async def volume(self, ctx: commands.Context, *, volume: int):
        voice_client = ctx.message.guild.voice_client
        if not voice_client.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        if 0 > volume > 100:
            return await ctx.send('Volume must be between 0 and 100')

        voice_client.volume = volume / 100
        await ctx.send('Volume of the player set to {}%'.format(volume))

    @commands.command(help='Stops playing and makes the bot leave the voice channel')
    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        await voice_client.disconnect()

    @commands.command(help='Skips audio currently being played')
    async def skip(self, context: commands.Context):
        voice_client = context.message.guild.voice_client
        if voice_client.is_playing:
            voice_client.stop()
        else:
            raise commands.CommandError('There is no audio currently playing.')

    @commands.command(help='Plays audio based on query or youtube url | .play uchiage hanabi')
    async def play(self, context: commands.Context, *, search: str):
        if not context.message.author.voice:
            raise commands.CommandError('You are not connected to any voice channel.')
        else:
            voice_channel = context.message.author.voice.channel

        if context.voice_client is None:
            await voice_channel.connect()

        voice_client = context.message.guild.voice_client

        async with context.typing():
            try:
                source = await YTDLSource.create_source(context, search, loop=self.client.loop)
            except YTDLError as e:
                await context.send('An error occurred while processing this request: {}'.format(str(e)))
            else:
                voice_client.play(source)
                embed = (discord.Embed(title=source.title, color=discord.Color.red(), url=source.url)
                         .set_image(url=source.thumbnail)
                         .set_footer(text='Duration: ' + source.duration))
                await context.send(embed=embed)


def setup(client):
    client.add_cog(Music(client))
