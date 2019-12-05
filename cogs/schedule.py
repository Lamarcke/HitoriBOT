import discord
import datetime
import asyncio
from icons import *
from collections import Counter
from discord.ext import commands
from jikanpy import AioJikan


jikan = AioJikan()

def weekdia(dia):
    week = {
        1: 'Segunda-Feira',
        2: 'Terça-Feira',
        3: 'Quarta-Feira',
        4: 'Quinta-Feira',
        5: 'Sexta-Feira',
        6: 'Sábado',
        7: 'Domingo'
    }
    return week.get(dia)

def diasemananome(diasemana):
    dianome = {
        'segunda': 'monday',
        'terça': 'tuesday',
        'terca': 'tuesday',
        'quarta': 'wednesday',
        'quinta': 'thursday',
        'sexta': 'friday',
        'sabado': 'saturday',
        'domingo': 'sunday'
    }
    return dianome.get(diasemana)


class Schedule(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def today(self, ctx):
        todaydate = datetime.datetime.today()
        date = todaydate.strftime("%A").lower()
        dia = todaydate.isoweekday()
        basesearch = await jikan.schedule(day=date)

        embed = discord.Embed(
            title=f'**Animes saindo hoje:**',
            description=f'**Dia: {weekdia(dia)}**',
            url='https://myanimelist.net/anime/season/schedule',
            colour=discord.Colour.blue()
            )
        embed.set_thumbnail(url=thumb_gif)
        embed.set_author(name='Schedule Beam', icon_url=icon_image)

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
        '''

        search = basesearch[date]
        max_queries = len(Counter(t['title'] for t in search))
        for x in range(0, max_queries):
            # Também é possivel usar dict.get() para ACESSAR OS VALORES ao invés de dict['key'] nesses casos.
            # A vantagem é que a o método .get() retorna um valor padrão caso o valor especificado não seja encontrado.
            media = search[x]
            media_title = media['title'] # Ou: media_title = search.get('title')
            media_episodes = media['episodes'] #Ou: media_episodes = search.get('episodes')
            media_source = media['source']
            media_score = media['score']
            if media_score == None:
                score = ''
            else:
                score = f'| Nota: {media_score}'
            embed.add_field(name=f'__**{media_title}**__', value=f'Fonte: {media_source} {score}', inline=False)
            await asyncio.sleep(0.05)
        
        await ctx.channel.send(embed=embed)


    @commands.command()
    async def tomorrow(self, ctx):
        '''
        Dica: impossivel enviar o ctx desse comando para o comando today e re-aproveitar o código do mesmo.
        Objetos "Command" não podem ser chamados como funções.
        Resultando no seguinte erro:
        TypeError: 'Command' object is not callable
        '''
        today = datetime.datetime.today()
        tomorrowdate = today + datetime.timedelta(days=1)
        date = tomorrowdate.strftime("%A").lower()
        basesearch = await jikan.schedule(day=date)
        dia = tomorrowdate.isoweekday()

        embed = discord.Embed(
            title=f'**Animes saindo amanhã:**',
            description=f'**Dia: {weekdia(dia)}**',
            url='https://myanimelist.net/anime/season/schedule',
            colour=discord.Colour.blue()
            )

        embed.set_thumbnail(url=thumb_gif)
        embed.set_author(name='Schedule Beam', icon_url=icon_image)

        search = basesearch[date]
        max_queries = len(Counter(t['title'] for t in search))
        for x in range(0, max_queries):
            media = search[x]
            media_title = media['title'] 
            media_episodes = media['episodes']
            media_source = media['source']
            media_score = media['score']
            if media_score == None:
                score = ''
            else:
                score = f'| Nota: {media_score}'
            embed.add_field(name=f'__**{media_title}**__', value=f'Fonte: {media_source} {score}', inline=False)
            await asyncio.sleep(0.05)
        
        
        await ctx.send(embed=embed)

    @commands.command()
    async def schedule(self, ctx, diasemana):
        if diasemana == 'domingo':
            titleshow = f'Animes saindo no: {diasemana.capitalize()}'
        elif diasemana == 'sabado':
            titleshow = f'Animes saindo no: {diasemana.capitalize()}'
        elif diasemana == 'sábado':
            titleshow = f'Animes saindo no: {diasemana.capitalize()}'
        else:
            titleshow = f'Animes saindo na {diasemana.capitalize() + "-Feira"}'
        date = diasemananome(diasemana)
        basesearch = await jikan.schedule(day=date)
        search = basesearch[date]

        embed = discord.Embed(
            title=f'**{titleshow}**',
            description='',
            url='https://myanimelist.net/anime/season/schedule',
            colour=discord.Colour.blue()
            )

        embed.set_thumbnail(url=thumb_gif)
        embed.set_author(name='Schedule Beam', icon_url=icon_image)

        search = basesearch[date]
        max_queries = len(Counter(t['title'] for t in search))
        for x in range(0, max_queries):
            media = search[x]
            media_title = media['title'] 
            media_episodes = media['episodes']
            media_source = media['source']
            media_score = media['score']
            if media_score == None:
                score = ''
            else:
                score = f'| Nota: {media_score}'
            embed.add_field(name=f'__**{media_title}**__', value=f'Fonte: {media_source} {score}', inline=False)
            await asyncio.sleep(0.05)
        await ctx.channel.send(embed=embed)

def setup(client):
    client.add_cog(Schedule(client))