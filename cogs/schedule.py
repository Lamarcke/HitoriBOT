import discord
import datetime as date
import asyncio
from collections import Counter
from discord.ext import commands
from jikanpy import AioJikan


jikan = AioJikan()


class Schedule(commands.Cog):
    def __init__(self, client):
        self.client = client



    @commands.command()
    async def today(self, ctx):
        gif = 'https://media.giphy.com/media/LMcDyquFeVJ8puLY9c/giphy.gif'
        todaydate = date.datetime.today()
        today = todaydate.strftime("%A").lower()
        embed = discord.Embed(
            title=f'**Animes saindo hoje:**',
            description=f'__**{today.upper()}**__' ,
            url='https://myanimelist.net/anime/season/schedule',
            colour=discord.Colour.blue()
            )
        embed.set_author(name='Today Schedule Beam', icon_url='https://i.imgur.com/tBZ9yd3.jpg')
        embed.set_thumbnail(url=gif)
        basesearch = await jikan.schedule(day=today)

        '''
        Problema:
        Não era possivel contar o valor maximo do range abaixo (o numero max de resultados que a API possivelmente enviaria)
        com a função len() diretametente.
        A API sempre retorna uma lista de dicionarios, dificultado ainda mais o procedimento.

        Solução inspirada por: @DSM no Stack Overflow (https://stackoverflow.com/users/487339/dsm)
        Solução:
        Usar o método Counter() para contar a quantidade de 'title' que a API envia como resposta; sempre sendo 1 por anime.
        Basicamente, com isso foi possivel aplicar o método len(), contanto o numero de valores que possuiam a string 'title';
        contando cada anime de 1 por 1.

        A solução empregada, apesar de funcional, pode ser aprimorada. Fique a vontade para fazer um pull request e sugerir uma melhoria
        no algoritmo.

        Aliás, se definir select como 0, o algoritmo vai acusar erro de "IndexError: list index out of range", na variavel search abaixo.
        Basicamente, quer dizer que a variavel procurou por um valor que não foi recebido, 1 a mais do que a API enviou.
        A solução, foi definir select como um valor negativo, sendo assim, assim que o loop for começar, ele será incrementado e se
        tornara 0 (primeiro valor enviado pela API)
        e assim por diante.
        '''

        max_queries = len(Counter(t['title'] for t in basesearch[f'{today}']))
        select = -1
        for x in range(0, max_queries):
            select += 1
            search = basesearch[f'{today}'][select]
            media_title = search['title']
            media_episodes = search['episodes']
            media_source = search['source']
            media_score = search['score']
            embed.add_field(name=f'**{media_title}**', value=f'Fonte: {media_source}, nota: {media_score}', inline=False)

        await ctx.channel.send(embed=embed)



def setup(client):
    client.add_cog(Schedule(client))