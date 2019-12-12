import discord
import random
from discord.ext import commands
import jikanpy
from collections import Counter

jikan = jikanpy.AioJikan()


def genrechoosermanga(genrename):
    genre = {
        'Action': 1,
        'Adventure': 2,
        'Cars': 3,
        'Comedy': 4,
        'Mystery': 7,
        'Drama': 8,
        'Ecchi': 9,
        'Fantasy': 10,
        'Horror': 14,
        'Martial Arts': 17,
        'Mecha': 18,
        'Samurai': 21,
        'Romance': 22,
        'School': 23,
        'Sci fi': 24,
        'Sci-fi': 24,
        'Scifi': 24,
        'Shoujo': 25,
        'Shoujo ai': 26,
        'Shoujo-ai': 26,
        'Shounen': 27,
        'Sports': 30,
        'Vampire': 32,
        'Yaoi': 33,
        'Yuri': 34,
        'Harem': 35,
        'Slice Of Life': 36,
        'Supernatural': 37,
        'Police': 39,
        'Psychological': 40,
        'Seinen': 41,
        'Josei': 42,
        'Gender bender': 44,
        'Thriller': 45

    }
    return genre.get(genrename, 'Error')


def genrechooser(genrename):
    genre = {
        'Action': 1,
        'Adventure': 2,
        'Cars': 3,
        'Comedy': 4,
        'Mystery': 7,
        'Drama': 8,
        'Ecchi': 9,
        'Fantasy': 10,
        'Horror': 14,
        'Martial Arts': 17,
        'Mecha': 18,
        'Samurai': 21,
        'Romance': 22,
        'School': 23,
        'Sci fi': 24,
        'Sci-fi': 24,
        'Scifi': 24,
        'Shoujo': 25,
        'Shoujo ai': 26,
        'Shoujo-ai': 26,
        'Shounen': 27,
        'Sports': 30,
        'Vampire': 32,
        'Yaoi': 33,
        'Yuri': 34,
        'Harem': 35,
        'Slice Of Life': 36,
        'Sol': 36,
        'Slice-of-life': 36,
        'Supernatural': 37,
        'Police': 39,
        'Psychological': 40,
        'Thriller': 41,
        'Seinen': 42,
        'Josei': 43

    }
    return genre.get(genrename, 'Error')


class Recommendation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def recommend(self, ctx, mediatype=None, *, genre=None):
        # noinspection PyGlobalUndefined
        global frases, media_url
        mediatype = mediatype.lower()
        if mediatype is None and genre is not None:
            return await ctx.channel.send(f'{ctx.author.mention}, eu posso até te recomendar isso ai, mas você quer'
                                          f'anime ou mangá? especifica ai, por favor.\nSintaxe correta:\n'
                                          f'**/recommend** *<tipo> <genero>*\n'
                                          f'*tipo*: anime, manga')
        elif mediatype is None:
            return await ctx.channel.send(f'{ctx.author.mention}'
                                          f' Recomendar o quê amigão? especifica ai que eu sou meio burrinho :(\n'
                                          'Eu posso recomendar: Anime, Manga, Movie, Manhwa e Manhua!')

        elif mediatype is not None and genre is None:
            pagenum = random.randint(0, 75)
            hitori = random.randint(1, 25)
            hitori_url = 'https://myanimelist.net/anime/37614/Hitoribocchi_no_Marumaru_Seikatsu'

            # Pode ser reduzido usando uma função, mas achei desnecessario no momento.
            if mediatype == 'movie':
                media_type = 'anime'
                subtype = 'movie'
            elif mediatype == 'manhwa':
                media_type = 'manga'
                subtype = 'manhwa'
            elif mediatype == 'manhua':
                media_type = 'manga'
                subtype = 'manhua'
            else:
                media_type = mediatype
                subtype = 'bypopularity'

            basesearch = await jikan.top(type=media_type, page=pagenum, subtype=subtype)
            search = basesearch['top'][random.randint(0, 50)]
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
                                    f'Que tal dar uma chance pra esse tal de **{media_name}**? Parece legalzinho:\n']
            selectfrases_anime_lowtier = random.choice(frases_anime_lowtier)
            frases_manga = [f'Tem uma galera lendo esse tal de **{media_name}**, parece bom em:\n',
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
                             'Pra que perder tempo com isso quando você poderia estar assistindo Hitoribocchi? '
                             'Pois é:\n', 'Segundo meus calculos, você deveria deixar isso pra la e ir '
                                          'assistir Hitoribocchi.',
                             'Tentei pesquisar pelo que você pediu, mas achei melhor '
                             'te recomendar esse tal de Hitoribocchi:',
                             '**FALHA NO SISTEMA**\nRecomendação emergencial automatica de Hitoribocchi realizada: \n']
            selectfrases_hitori = random.choice(frases_hitori)

            if hitori == 1:
                print('Hitoribocchi recomendado.')
                return await ctx.channel.send(f'{selectfrases_hitori}{hitori_url}')

            else:
                if mediatype == 'anime' or 'movie':
                    if pagenum > 35:
                        return await ctx.channel.send(f'{selectfrases_anime_lowtier}{media_url}')

                    else:
                        return await ctx.channel.send(f'{selectfrases_anime}{media_url}')

                elif mediatype == 'manga' or 'manhwa' or 'manhua':
                    if pagenum > 35:
                        return await ctx.channel.send(f'{selectfrases_manga_lowtier}{media_url}')

                    else:
                        return await ctx.channel.send(f'{selectfrases_manga}{media_url}')

        else:
            oggenre = genre
            genre = genre.lower()
            if mediatype == 'anime':
                genre = genrechooser(genre.capitalize())
            if mediatype == 'manga':
                genre = genrechoosermanga(genre.capitalize())
            if genre == 'Error':
                return await ctx.channel.send(f'Olha amigo, nunca ouvi falar desse tal de {oggenre} não, tem certeza'
                                              f'que você digitou direitinho?')

            try:
                basesearch = await jikan.genre(type=mediatype, genre_id=genre, page=random.randint(0, 3))
            except jikanpy.exceptions.APIException:
                basesearch = await jikan.genre(type=mediatype, genre_id=genre)

            if mediatype == 'manga':
                max_queries = len(Counter(t['title'] for t in basesearch['manga']))
                search = basesearch['manga'][random.randint(1, max_queries)]
            else:
                max_queries = len(Counter(t['title'] for t in basesearch['anime']))
                search = basesearch['anime'][random.randint(1, max_queries)]

            media_name = search['title']
            media_url = search['url']
            if mediatype == 'anime':
                frases = [f"Sei não em, parece que a galera ta de olho nesse **{media_name}** aqui ó:\n",
                          f'Da uma chance pra esse tal de **{media_name}** aqui, vê se é bão:\n',
                          f'Eu talvez esteja recomendando **{media_name}**, talvez não...\n',
                          f'Eu, se fosse um ser humano e não um bot forçado a assistir hitoribocchi 24/7'
                          f'com certeza estaria assistindo isso aqui: (eu acho)\n',
                          f'Assista **{media_name}**\nAssista **{media_name}** agora\n']

            elif mediatype == 'manga':
                frases = [f'Tem uma galera lendo esse tal de **{media_name}**, parece bom em:',
                          f'Da uma olhada nesse tal de **{media_name}**, tem uma galera que curte:\n',
                          f'Olha, se fosse um ser humano e não um bot forçado a assistir hitoribocchi 24/7, '
                          f'com certeza estaria lendo isso aqui: (eu acho)\n',
                          f'Leia **{media_name}**\nLeia **{media_name}** agora\n']

            fraseselect = random.choice(frases)

            await ctx.channel.send(f'{fraseselect}{media_url}')

    @commands.command()
    async def recommend18(self, ctx, mediatype=None):
        # noinspection PyGlobalUndefined
        global hfrases, media_url
        if mediatype is None:
            return await ctx.channel.send(f'{ctx.author.mention} O que você quer exatamente amigo?\n'
                                          'Especifica se é doujin ou hentai pra eu ter uma ideia ;)')

        mediatype = mediatype.lower()

        if mediatype == 'hentai':
            basesearch = await jikan.genre(type='anime', genre_id=12, page=random.randint(1, 12))
            maxqueries = len(Counter(t['title'] for t in basesearch['anime']))
            search = basesearch['anime'][random.randint(0, maxqueries)]
            media_name = search['title']
            media_url = search['url']
            hfrases = ['Porquê você faz isso comigo? Sabe o quanto de NTR eu tive que assistir pra '
                       'te recomendar esse topzera?\nÉ bom tu conferir em...\n',
                       'Ta aqui, não se preocupa, não vou contar pra ninguém ;)\n',
                       'Uma pena que não tem como apagar o historico do BOT né?, '
                       'Mas calma, eu não conto pra ninguém:\n',
                       f'Esse tal de {media_name} parece ser bom, se eu pudesse assistir algo além de '
                       f'Hitoribocchi, eu assistiria, escondido.\n',
                       f'Eu não posso abrir uma aba anônima, mas você pode, então vai aproveita, eu acho:\n',
                       f'Peguei esse na sorte, especialmente pra você: ~~tomara que não seja NTR~~\n',
                       f'*julgando você silenciosamente...*\n']

        elif mediatype == 'doujin' or 'doujinshi':
            basesearch = await jikan.genre(type='manga', genre_id=12, page=random.randint(1, 88))
            maxqueries = len(Counter(t['title'] for t in basesearch['manga']))
            search = basesearch['manga'][random.randint(0, maxqueries)]
            media_name = search['title']
            media_url = search['url']
            hfrases = ['Porquê você faz isso comigo? Sabe o quanto de NTR eu tive que ler pra '
                       'te recomendar esse topzera?\nÉ bom tu conferir em...\n',
                       'Ta aqui, não se preocupa, não vou contar pra ninguém ;)\n',
                       'Uma pena que não tem como apagar o historico do BOT né?, '
                       'Mas calma, eu não conto pra ninguém ;)\n',
                       f'Esse tal de {media_name} parece ser bom, se eu pudesse ler algo além de '
                       f'Hitoribocchi, eu com certeza estaria lendo ele, **escondido**.\n',
                       f'Eu não posso abrir uma aba anônima, mas você pode, então vai aproveita, eu acho:\n',
                       f'Peguei esse na sorte, especialmente pra você: ~~tomara que não seja NTR~~\n',
                       f'*julgando você silenciosamente...*\n']
        else:
            return await ctx.channel.send(f'{ctx.author.mention}Acho que você digitou algo errado amigo, '
                                          f'da uma conferida ai por favor')
        selecthfrase = random.choice(hfrases)
        return await ctx.channel.send(f'{selecthfrase}{media_url}')


def setup(client):
    client.add_cog(Recommendation(client))
