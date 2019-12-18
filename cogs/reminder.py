import discord
import asyncio
import sqlite3
import datetime
import aioschedule as schedule
import random
from discord.ext import commands
from jikanpy import AioJikan
from collections import Counter
from icons import icon_image

jikan = AioJikan()

conn = sqlite3.connect("./data/hitoridata.db")
c = conn.cursor()


async def alertairingtoday(client):
    c.execute("SELECT DISTINCT userid FROM airingtoday")
    dataresults = c.fetchall()
    max_queries = len(dataresults)
    embed = discord.Embed(
        title='**Animes que você acompanha saindo hoje:**',
        description='*Horarío Padrão de Brasília (UTC-3)*',
        colour=discord.Colour.blue()
    )
    embed.set_author(name='HitoriBOT Reminder', icon_url=icon_image)
    for x in range(0, max_queries):
        results = dataresults[x]
        userid = results[0]
        userobj = client.get_user(userid)
        if userobj.dm_channel is not None:
            userdm = userobj.dm_channel
        else:
            userdm = await userobj.create_dm()

        c.execute("SELECT animeid, launchhour FROM airingtoday WHERE userid=:userid", {'userid': userid})
        userresults = c.fetchall()

        frases = [
            f"N-Não é como se eu tivesse acordado cedo pra te lembrar que tem anime saindo hoje ou algo assim >-<\n",
            f"Te liga, esses animes saem hoje em, como sou um bot gente boa, vou te avisar quando lançar ;)\n",
            f"Esses animes tão quase saindo la no japão em... Mas calma que eu te aviso quando sair ;)\n"]
        selectfrase = random.choice(frases)
        for y in range(0, len(userresults)):
            usermedia = userresults[y]
            mediaid = usermedia[0]
            launchhour = usermedia[1]
            media = await jikan.anime(mediaid)
            mediatitle = media['title']
            embed.add_field(name=f'**{mediatitle}**', value=f'{launchhour}', inline=False)
            await asyncio.sleep(5)

        await userdm.send(content=selectfrase, embed=embed)
        print("Alerta de lançamentos diario enviado.")


async def alertairingnow(client):
    now = datetime.datetime.now()
    nowplus1 = now + datetime.timedelta(minutes=15)
    c.execute("SELECT * FROM airingtoday WHERE launchhour >= ? AND launchhour <= ?", (now.strftime("%X"),
                                                                                      nowplus1.strftime("%X")))
    dataresults = c.fetchall()
    if not dataresults:
        return print("Nenhum novo lançamento.")

    max_queries = len(dataresults)
    for x in range(0, max_queries):
        results = dataresults[x]
        userid = results[0]
        userobj = client.get_user(userid)
        if userobj.dm_channel is not None:
            userdm = userobj.dm_channel
        else:
            userdm = await userobj.create_dm()
        mediaid = results[1]
        media = await jikan.anime(mediaid)
        media_title = media['title']
        media_url = media['url']
        launchhour = results[2]
        frases = [f"Se liga, {media_title} ta saindo às {launchhour}, fica ligado em!\n",
                  f"Ei, esse tal de {media_title} ta saindo agora no japão, às {launchhour}.\n",
                  f"To te mandando mensagem só pra lembrar que esse tal de {media_title} ja ta saindo às {launchhour}"
                  f"...\nN-não é como se eu quisesse falar com você ou algo assim >-<\n"]
        selectfrase = random.choice(frases)
        await userdm.send(f'{selectfrase}{media_url}')
        print('Alerta de lançamentos enviado.')
        await asyncio.sleep(5)


async def verifyairing():
    print('Verificação de lançamentos diaria em andamento...')
    today = datetime.datetime.today().strftime("%A").capitalize()

    basesearch = await jikan.schedule(day=today.lower())
    airing = basesearch[today.lower()]
    c.execute("SELECT userid, animeid, launchhour FROM animedata WHERE launchday=:today AND airing=1", {'today': today})
    results = c.fetchall()
    print(results)
    max_queries_data = len(results)
    max_queries = len(Counter(t['title'] for t in airing))
    for x in range(0, max_queries):
        media = airing[x]
        airingid = media['mal_id']
        for y in range(0, max_queries_data):
            datamedia = results[y]
            userid = datamedia[0]
            dataid = datamedia[1]
            launchhour = datamedia[2]
            if airingid == dataid:
                c.execute("INSERT INTO airingtoday VALUES (?, ?, ?)", (userid, dataid, launchhour))
                conn.commit()


async def verifycompleted():
    print("Verificando animes com lançamento finalizado...")
    c.execute("SELECT DISTINCT animeid FROM animedata WHERE airing = 1")
    dataresults = c.fetchall()
    print(dataresults)
    max_queries = len(dataresults)
    for x in range(0, max_queries):
        datamedia = dataresults[x]
        dataid = datamedia[0]
        print(dataid)
        search = await jikan.anime(dataid)
        mediaid = search['mal_id']
        mediastatus = search['status']
        if mediastatus == 'Finished Airing':
            print("Anime finalizado detectado.")
            c.execute("UPDATE animedata SET airing = 0 WHERE animeid = :animeid", {'animeid': mediaid})
            conn.commit()
        else:
            pass
        await asyncio.sleep(5)
    print('Verificação completa.\nDeletando animes completos da database.')
    c.execute("DELETE FROM animedata WHERE airing = 0")
    conn.commit()
    print('Dados deletados da database.')


def createdata():
    c.execute("""CREATE TABLE IF NOT EXISTS animedata(
    userid INTEGER,
    animename TEXT,
    animeid INTEGER,
    launchday TEXT,
    launchhour TEXT,
    airing INTEGER
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS airingtoday(
    userid INTEGER,
    animeid INTEGER,
    launchhour TEXT
    )""")

    conn.commit()


async def deletedata():
    c.execute("DELETE FROM airingtoday")
    conn.commit()
    print('Limpando lançamentos do dia...')


def diasemana(launchday):
    dianome = {
        'monday': 'segunda',
        'tuesday': 'terça',
        'wednesday': 'quarta',
        'thursday': 'quinta',
        'friday': 'sexta',
        'saturday': 'sábado',
        'sunday': 'domingo'
    }
    return dianome.get(launchday)


def weekdia(dia):
    week = {
        1: 'monday',
        2: 'tuesday',
        3: 'wednesday',
        4: 'thursday',
        5: 'friday',
        6: 'saturday',
        7: 'sunday'
    }
    return week.get(dia)


async def scheduler(client):
    schedule.every(15).minutes.do(alertairingnow, client)
    schedule.every().day.at("00:15").do(verifyairing)
    schedule.every().day.at("07:00").do(alertairingtoday, client)
    schedule.every().day.at("23:59").do(deletedata)
    schedule.every().sunday.at("23:30").do(verifycompleted)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(10)


class Reminder(commands.Cog):
    def __init__(self, client):
        self.client = client
        createdata()

    @commands.command()
    async def remind(self, ctx, *, medianame):
        # noinspection PyGlobalUndefined
        global mediapage, media_id, media_status
        today = datetime.datetime.today().strftime("%A").lower()  # dia da semana em inglês

        try:
            basesearch = await jikan.search(search_type='anime', query=medianame, parameters={'status': 'airing'})
            search = basesearch['results'][0]
            media_status = search['airing']
            media_id = search['mal_id']
            mediapage = await jikan.anime(media_id)

        except IndexError:
            return await ctx.channel.send(
                'Não consegui achar nenhum anime que está em lançamento com esse nome amigo...\n'
                'Tem certeza que digitou corretamente?')

        userid = ctx.author.id
        media_name = mediapage['title']
        media_url = mediapage['url']
        launchday = mediapage['broadcast'][:-16]  # Retira alguns caracteres a partir do final
        jplaunchhour = mediapage['broadcast'][-11:-6]
        jphour = datetime.datetime.strptime(jplaunchhour, '%H:%M')
        oglaunchhour = (jphour + datetime.timedelta(hours=12)).strftime("%X")
        launchhour = str(oglaunchhour)[:-3]

        c.execute("SELECT userid, animeid FROM animedata WHERE userid=:userid", {'userid': userid})
        userresults = c.fetchall()
        for x in range(0, len(userresults)):
            results = userresults[x]
            userprevious = results[0]
            idprevious = results[1]
            if userid == userprevious and idprevious == media_id:
                return await ctx.channel.send("Ei! parece que você já adicionou esse anime a sua lista de lembretes!"
                                              "\nNão se preocupa, não vou esquecer ;)")

        c.execute("INSERT INTO animedata VALUES(?, ?, ?, ?, ?, ?)",
                  (userid, media_name, media_id, launchday, launchhour, media_status))
        conn.commit()

        if diasemana(launchday.lower()) == 'domingo' or 'sábado':
            dayshow = 'todo'
        else:
            dayshow = 'toda'

        await ctx.channel.send(
            f'Certo, {dayshow} **{diasemana(launchday.lower())}** eu vou avisa-lo que **{media_name}** está'
            f' saindo.\nHorário: {launchhour} (UTC-3)\n{media_url}')

    @commands.command()
    async def reminder(self, ctx):
        username = ctx.author.name
        userid = ctx.author.id
        c.execute("SELECT animename, launchday, launchhour FROM animedata WHERE userid=:userid", {'userid': userid})
        dataresult = c.fetchall()
        if not dataresult:
            return await ctx.channel.send("Parece que você não está acompanhando nenhum anime no momento...\n"
                                          "*Dica: para adicionar um novo anime, use /remind <nome do anime>*")
        embed = discord.Embed(title=f'Lista de Animes de {username}',
                              description='*Eu estou programado para alertá-lo sobre novos episódios nos seguintes '
                                          'animes:*',
                              colour=discord.Colour.blue()
                              )

        max_queries = len(dataresult)
        for x in range(0, max_queries):
            results = dataresult[x]
            animename = results[0]
            launchday = results[1]
            launchhour = results[2]
            embed.add_field(name=f'**{animename}**', value=f"Saindo {diasemana(launchday.lower())}, às {launchhour}.")
        return await ctx.channel.send(content=ctx.author.mention, embed=embed)

    @commands.command()
    async def forget(self, ctx, *, medianame):
        try:
            basesearch = await jikan.search(search_type='anime', query=medianame, parameters={'status': 'airing'})
            search = basesearch['results'][0]
            animestatus = search['airing']
            animeid = search['mal_id']
            animename = search['title']

        except IndexError:
            return await ctx.channel.send(
                'Não consegui achar nenhum anime que está em lançamento com esse nome...\n'
                'Tem certeza que digitou corretamente?')

        userid = ctx.author.id
        c.execute("SELECT userid, animeid FROM animedata WHERE userid=:userid AND animeid=:animeid",
                  {'userid': userid, 'animeid': animeid})
        results = c.fetchall()
        if not results:
            return await ctx.channel.send(f"Não consegui achar esse tal de {animename} "
                                          f"com seu usuario no meu sistema...\n"
                                          f"Se por um acaso pesquisei o anime errado, "
                                          f"por favor, escreva de uma forma que fique mais "
                                          f"facil para mim identificá-lo, sou meio burrinho ;)")
        else:
            c.execute("DELETE FROM animedata WHERE userid=:userid AND animeid=:animeid",
                      {'userid': userid, 'animeid': animeid})
            conn.commit()
            await ctx.channel.send(f'Tudo bem, acabei de apagar o lembrete de {animename} para você no meu sistema.')


def setup(client):
    client.add_cog(Reminder(client))
    client.loop.create_task(scheduler(client))
