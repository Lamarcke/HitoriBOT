import discord
from discord.ext import commands
from jikanpy import AioJikan

jikan = AioJikan()


class Search(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            print(f"Bot sent a message on {message.guild}")
            
        else:
            return



    @commands.command()
    async def search(self, ctx, mediatype, *, name):
        basesearch = await jikan.search(search_type=mediatype, query=name, parameters={'limit': 1})
        # retorna sempre o primeiro valor da busca, que fica dentro de 'results'
        search = basesearch['results'][0]
        # Define o tipo de midia pesquisado (TV, Manga, One-shot) /Não confundir com o parametro mediatype.
        media_type = search['type']
        if mediatype == 'anime':
            media_status = search['airing']
            if media_status:
                status = 'Em lançamento'
            else:
                status = 'Concluido'

            media_name = search['title']
            media_url = search['url']
            media_image = search['image_url']
            media_synopsis = search['synopsis']
            media_episodes = search['episodes']
            media_score = search['score']

            embed = discord.Embed(
                title=media_name,
                description=f'Tipo: {media_type}\nStatus: {status}',
                url=media_url,
                colour=discord.Colour.blue()
            )
            embed.set_author(name='Search Beam', icon_url='https://i.imgur.com/ZChDWnL.png')
            embed.set_thumbnail(url='https://media.giphy.com/media/LMcDyquFeVJ8puLY9c/giphy.gif')
            embed.set_image(url=media_image)
            embed.add_field(name='Episódios:', value=media_episodes, inline=True)
            embed.add_field(name='Nota:', value=media_score, inline=True)
            embed.set_footer(text=media_synopsis)
            await ctx.channel.send(embed=embed)

        if mediatype == 'manga':
            manga_status = search['publishing']
            if manga_status:
                status = 'Em lançamento'
            else:
                status = 'Concluido'

            media_name = search['title']
            media_url = search['url']
            media_image = search['image_url']
            media_synopsis = search['synopsis']
            media_chapters = search['chapters']
            media_volumes = search['volumes']
            media_score = search['score']

            embed = discord.Embed(
                title=media_name,
                description=f'Tipo: {media_type}\nStatus: {status}',
                url=media_url,
                colour=discord.Colour.blue()
            )
            embed.set_author(name='HitoriBOT Search Beam', icon_url='https://i.imgur.com/tBZ9yd3.jpg')
            embed.set_thumbnail(url='https://media.giphy.com/media/LMcDyquFeVJ8puLY9c/giphy.gif')
            embed.set_image(url=media_image)
            embed.add_field(name='Capítulos:', value=media_chapters, inline=True)
            embed.add_field(name='Volumes:', value=media_volumes, inline=True)
            embed.add_field(name='Nota:', value=media_score, inline=True)
            embed.set_footer(text=media_synopsis)
            await ctx.channel.send(embed=embed)

        if mediatype == 'character':
            name = search['name']
            url = search['url']
            print(name)
            print(url)
            await ctx.channel.send(f'{name}\n{url}')

        if mediatype == 'person':
            name = search['name']
            url = search['url']
            print(name)
            print(url)
            await ctx.channel.send(f'{name}\n{url}')


def setup(client):
    client.add_cog(Search(client))
