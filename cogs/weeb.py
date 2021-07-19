from discord.ext import commands
import discord
from jikanpy import Jikan
import datetime
import calendar

jikan = Jikan()
now = datetime.datetime.now()


class Weeb(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(help='Searches for an anime | .anime code geass')
    async def anime(self, context, *, query):
        anime = jikan.anime(resource_id_search('anime', query))
        embed = create_media_embed(anime)
        await context.send(embed=embed)

    @commands.command(help='Searches for a manga | .manga berserk')
    async def manga(self, context, *, query):
        manga = jikan.manga(resource_id_search('manga', query))
        embed = create_media_embed(manga)
        await context.send(embed=embed)

    @commands.command(help='Shows most popular anime of current season | .season # (default 5)')
    async def season(self, context, limit: int = 5):
        result = jikan.season(year=now.year, season='fall')
        # result = jikan.season(year=now.year, season=current_anime_season())
        animes = result.get('anime')
        fields = 0
        await context.send('**' + result.get('season_name') + ' ' + str(result.get('season_year'))
                           + ' Most Popular Anime**')
        for anime in animes:
            if fields == limit:
                break
            fields += 1
            embed = create_media_embed(anime, airing=True)
            await context.send(embed=embed)

    @commands.command(help='Shows currently airing anime for today')
    async def today(self, context):
        day = calendar.day_name[now.weekday()]
        result = jikan.schedule(day.lower())
        animes = result.get(day.lower())
        embed = discord.Embed(color=discord.Color.dark_blue(), title=day + ' Anime')
        for anime in animes:
            embed.add_field(name=anime.get('title') + ' (' + str(anime.get('score')) + ')', value=anime.get('url'),
                            inline=False)

        await context.send(embed=embed)

    @commands.command(help='Searches for a character | .chara Naruto')
    async def chara(self, context, *, query):
        chara = jikan.character(resource_id_search('character', query))
        va_data = chara.get('voice_actors')
        voice_actor_name = None
        for va in va_data:
            if va.get('language') == 'Japanese':
                voice_actor_name = va.get('name')
                break

        nicknames_list = chara.get('nicknames')
        nicknames = ''
        if nicknames_list is not None:
            for name in nicknames_list:
                nicknames += name + ', '
            nicknames = nicknames[:-2]

        anime = chara.get('animeography')[0].get('name')
        manga = chara.get('mangaography')[0].get('name')
        source = anime
        if source is None:
            source = manga

        details = chara.get('about')
        details = details.replace('\\n', '')
        if len(details) > 1024:
            details = details[:1024] + '...'

        embed = discord.Embed(color=discord.Color.dark_blue(), title=chara.get('name'), url=chara.get('url'))
        embed.add_field(name='Source', value=source)
        if nicknames != '':
            embed.add_field(name='Nicknames', value=nicknames)
        embed.add_field(name='VA', value=voice_actor_name)
        embed.add_field(name='Details', value=details, inline=False)
        embed.set_image(url=chara.get('image_url'))
        await context.send(embed=embed)


def create_media_embed(media, airing: bool = False) -> discord.embeds:
    if airing:
        airing = calculate_day_of_week(media.get('airing_start'))

    genres = ''
    for genre in media.get('genres'):
        genres += genre.get('name') + ', '
    genres = genres[:-2]

    studios = ''
    if media.get('studios') is not None:
        for studio in media.get('studios'):
            studios += studio.get('name') + ', '
        studios = studios[:-2]

    serializations = ''
    if media.get('serializations') is not None:
        for serialization in media.get('serializations'):
            serializations += serialization.get('name') + ', '
        serializations = serializations[:-2]

    synopsis = media.get('synopsis')
    if len(synopsis) >= 1024:
        synopsis = synopsis[:500] + '...'

    footer = 'Score: ' + str(media.get('score'))
    if media.get('episodes') is not None:
        footer += ' | Episodes: ' + str(media.get('episodes'))
    if media.get('chapters') is not None:
        footer += ' | Chapters: ' + str(media.get('chapters'))

    embed = discord.Embed(color=discord.Color.dark_blue(), title=media.get('title'), url=media.get('url'))
    embed.add_field(name="Genres", value=genres)

    # Anime Fields
    if studios != '':
        embed.add_field(name="Studio", value=studios)
    if media.get('aired') is not None:
        embed.add_field(name="Aired", value=media.get('aired').get('string'))
    if airing:
        embed.add_field(name='Airs', value=airing)

    # Manga Fields
    if serializations != '':
        embed.add_field(name="Serializations", value=serializations)
    if media.get('published') is not None:
        embed.add_field(name="Published", value=media.get('published').get('string'))

    embed.add_field(name="Synopsis", value=synopsis, inline=False)
    embed.set_image(url=media.get('image_url'))
    embed.set_footer(text=footer)

    return embed


def resource_id_search(resource_type: str, query: str) -> int:
    search = jikan.search(resource_type, query, page=1)
    mal_id = search.get('results')
    return mal_id[0].get('mal_id')


def current_anime_season() -> str:
    if now.month <= 3:
        season = 'winter'
    elif now.month <= 6:
        season = 'spring'
    elif now.month <= 9:
        season = 'summer'
    else:
        season = 'fall'
    return season


def calculate_day_of_week(data: str) -> str:
    date, time_data = data.split('T')
    year, month, day = (int(x) for x in date.split('-'))
    day_of_week = datetime.date(year, month, day).strftime("%A")
    time = time_data[0:5]
    return day_of_week + ' at ' + str(time)


def setup(client):
    client.add_cog(Weeb(client))
