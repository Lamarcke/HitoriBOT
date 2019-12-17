import discord
from discord.ext import commands
from jikanpy import Jikan
from icons import icon_image, thumb_gif

jikan = Jikan()


class Search(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            if message.guild is None:
                print('Bot sent a message on some channel/DM')
            else:
                print(f"Bot sent a message on {message.guild}")

        else:
            return

    @commands.command()
    async def search(self, ctx, mediatype, *, name):
        name = name.lower()
        basesearch = jikan.search(search_type=mediatype, query=name)
        # retorna sempre o primeiro valor da busca, que fica dentro de 'results'
        search = basesearch['results'][0]
        # Define o tipo de midia pesquisado (TV, Manga, One-shot) /Não confundir com o parametro mediatype.

        if mediatype == 'anime':
            media_type = search['type']
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
            embed.set_author(name='HitoriBOT Search', icon_url=icon_image)
            embed.set_thumbnail(url=thumb_gif)
            embed.set_image(url=media_image)
            embed.add_field(name='Episódios:', value=media_episodes, inline=True)
            embed.add_field(name='Nota:', value=media_score, inline=True)
            embed.set_footer(text=media_synopsis)
            await ctx.channel.send(embed=embed)

        if mediatype == 'manga':
            media_type = search['type']
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
            embed.set_author(name='HitoriBOT Search', icon_url=icon_image)
            embed.set_thumbnail(url=thumb_gif)
            embed.set_image(url=media_image)
            embed.add_field(name='Capítulos:', value=media_chapters, inline=True)
            embed.add_field(name='Volumes:', value=media_volumes, inline=True)
            embed.add_field(name='Nota:', value=media_score, inline=True)
            embed.set_footer(text=media_synopsis)
            await ctx.channel.send(embed=embed)

        if mediatype == 'character':
            name = search['name']
            url = search['url']
            await ctx.channel.send(f'{name}\n{url}')

        if mediatype == 'person':
            name = search['name']
            url = search['url']
            await ctx.channel.send(f'{name}\n{url}')


def setup(client):
    client.add_cog(Search(client))
