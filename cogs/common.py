import random
import discord
from discord.ext import commands
from PyDictionary import PyDictionary

dictionary = PyDictionary()


class Common(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(help='Flips a coin')
    async def flip(self, context):
        responses = ['Heads', 'Tails']
        await context.send(f'**{random.choice(responses)}**')

    @commands.command(help='Rolls a dice, add number to indicate range (default 6) | .roll 18')
    async def roll(self, context, num=6):
        rand = random.randint(1, num)
        await context.send(f'**{rand}**')

    @commands.command(help='Deletes your recent messages in channel (Default 100) | .prune 20')
    async def prune(self, context, limit=100):
        def is_message_author(message):
            return message.author == context.message.author

        await context.channel.purge(check=is_message_author, limit=limit)

    @commands.command(help='Arknights operator search | .ak exusiai')
    async def ak(self, context, name):
        await context.send('https://gamepress.gg/arknights/operator/' + name)

    @commands.command(help='Sends enlarged image of custom emoji | .enlarge :pepehands: :pog:')
    async def enlarge(self, context, *emojis: discord.PartialEmoji):
        message = ''
        for emoji in emojis:
            message += str(emoji.url) + ' '
            await context.send(emoji.url)

    @commands.command(help='Searches for word meanings, synonyms, and antonyms | .dict example')
    async def dict(self, context, word):
        results = dictionary.meaning(word)
        if results is None:
            await context.send('**No result found**')
        else:
            embed = discord.Embed(color=discord.Color.red(), title='Results for: ' + word)
            for key, values in results.items():
                meaning = ''
                for value in values:
                    meaning += '-' + value + '.\n'
                embed.add_field(name=key, value=meaning, inline=False)

            synonyms_results = dictionary.synonym(word)
            synonyms = ''
            for syn in synonyms_results:
                synonyms += syn + ', '
            synonyms = synonyms[:-2]
            embed.add_field(name='Synonyms', value=synonyms, inline=False)

            antonym_results = dictionary.antonym(word)
            antonyms = ''
            for ant in antonym_results:
                antonyms += ant + ', '
            antonyms = antonyms[:-2]

            embed.add_field(name='Antonyms', value=antonyms, inline=False)
            await context.send(embed=embed)


def setup(client):
    client.add_cog(Common(client))
