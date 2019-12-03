import discord
import random
from discord.ext import commands
from jikanpy import AioJikan

jikan = AioJikan()


class Recommendation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def recommendme(self, ctx, mediatype=''):
        if mediatype == '':
            await ctx.channel.send(f'{ctx.author.mention}'
                                   f' Recomendar o quê amigão? especifica ai que eu sou meio burrinho :(\n'
                                   'Eu posso recomendar: Anime, Manga, Movie, Manhwa e Manhua!')
        else:
            pagenum = random.randint(0, 20)
            hitori = random.randint(0, 20)
            hitori_url = 'https://myanimelist.net/anime/37614/Hitoribocchi_no_Marumaru_Seikatsu'

            if mediatype == 'movie':
                media_type = 'anime'
                subtype = 'movie'
            elif mediatype == 'manhwa':
                media_type = 'manga'
                subtype = 'manhwa'
            elif mediatype == 'manhua':
                media_type = 'manga'
                subtype = 'manhua'
            elif mediatype == 'doujin':
                media_type = 'manga'
                subtype = 'doujin'
            else:
                media_type = mediatype
                subtype = 'bypopularity'

            basesearch = await jikan.top(type=media_type, page=pagenum, subtype=subtype)
            search = basesearch['top'][random.randint(0, 50)]
            print(search)
            media_name = search['title']
            media_url = search['url']
            frases_anime = [f"Sei não em, parece que a galera ta de olho nesse **{media_name}** aqui ó:\n",
                            f'Da uma chance pra esse tal de **{media_name}** aqui, vê se é bão:\n',
                            f'Eu talvez esteja recomendando **{media_name}**, talvez não...\n',
                            f'Eu, se fosse um ser humano e não um bot forçado a assistir hitoribocchi 24/7'
                            f'com certeza estaria assistindo isso aqui: (eu acho)\n',
                            f'Assista **{media_name}**\nAssista **{media_name}** agora\n']
            selectfrases_anime = random.choice(frases_anime)
            frases_anime_lowtier = [f'Tem gente que ta assistindo esse tal de **{media_name}**... tem gosto pra tudo né'
                                    f'\n',
                                    f'Quem liga pra popularidade? esse tal de **{media_name}** ',
                                    f'parece ser bom, apesar de que eu, como um bot, não sei diferenciar isso...\n',
                                    f'Que tal dar uma chance pra esse tal de **{media_name}**? Parece legalzinho:']
            selectfrases_anime_lowtier = random.choice(frases_anime_lowtier)
            frases_manga = [f'Tem uma galera lendo esse tal de **{media_name}**, parece bom em:',
                            f'Da uma olhada nesse tal de **{media_name}**, ta famosinho e pa:\n',
                            f'Olha, se fosse um ser humano e não um bot forçado a assistir hitoribocchi 24/7, '
                            f'com certeza estaria lendo isso aqui: (eu acho)\n',
                            f'Leia **{media_name}**\nLeia **{media_name}** agora\n']
            selectfrases_manga = random.choice(frases_manga)
            frases_manga_lowtier = [f'Achei essa perola aqui especialmente pra você: \n',
                                    f'Fique sabendo que uma galera anda lendo esse tal de **{media_name}**, '
                                    f'se é bom eu não sei:\n',
                                    f'Acho que na hora de você ler **{media_name}** '
                                    f'e pagar de cult pros seus amigos né não?\n']
            selectfrases_manga_lowtier = random.choice(frases_manga_lowtier)
            frases_hitori = ['ASSISTA HITORIBOCCHI AGORA: \n',
                             'Pra que perder tempo com isso quando você poderia estar assistindo Hitoribocchi? Pois é:\n',
                             'Segundo meus calculos, você deveria deixar isso pra la e ir assistir Hitoribocchi.',
                             'Tentei pesquisar pelo que você pediu, mas achei melhor te recomendar esse tal de '
                             'Hitoribocchi:',
                             '**FALHA NO SISTEMA**\nRecomendação emergencial automatica de Hitoribocchi realizada: \n']
            selectfrases_hitori = random.choice(frases_hitori)

            if hitori == 1:
                print('Hitoribocchi recomendado.')
                await ctx.channel.send(f'{selectfrases_hitori}{hitori_url}')

            else:
                if mediatype == 'anime' or 'movie':
                    if pagenum > 8:
                        await ctx.channel.send(f'{selectfrases_anime_lowtier}{media_url}')

                    else:
                        await ctx.channel.send(f'{selectfrases_anime}{media_url}')

                elif mediatype == 'manga' or 'manhwa' or 'manhua':
                    if pagenum > 8:
                        await ctx.channel.send(f'{selectfrases_manga_lowtier}{media_url}')

                    else:
                        await ctx.channel.send(f'{selectfrases_manga}{media_url}')


def setup(client):
    client.add_cog(Recommendation(client))
