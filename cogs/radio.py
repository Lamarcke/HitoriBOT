import discord
import asyncio
import youtube_dl
import random
from icons import icon_image
from discord.ext import commands

ytdl_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

yt = youtube_dl.YoutubeDL(ytdl_options)


# Necessário definir porquê o youtube não permite um endereço fixo com duração ilimitada a um video.

def lofipicker(num):
    lofi = {
        1: 'https://d3ctxlq1ktw2nl.cloudfront.net/staging/2019-9-28/31375264-44100-2-7d39fe5d47031.m4a',
        2: 'https://d3ctxlq1ktw2nl.cloudfront.net/production/2018-10-3/5561807-44100-2-7813a3d0a6094.m4a',
        3: 'https://d3ctxlq1ktw2nl.cloudfront.net/staging/2019-9-1/25597566-44100-2-1b43168193cf9.m4a',
        4: 'https://d3ctxlq1ktw2nl.cloudfront.net/staging/2018-9-4/4949236-44100-2-48d3b15bb73bd.m4a'
    }
    return lofi.get(num)


def radiochooser(radionum):
    urlradios = {
        1: 'http://momori.animenfo.com:8000/?type=http&nocache=6391',  # Anime NFO, Japan
        2: 'http://curiosity.shoutca.st:8019/stream',  # Vocaloid Radio, Japan
        3: 'http://stm11.srvstm.com:8356/app128/',  # Anime Night, Brasil
        4: 'http://cast.animu.com.br:9021/autodj',  # Animu FM, Brasil
        5: 'http://stream2.laut.fm/animefm',  # Anime FM, Brasil
        6: lofipicker(random.randint(1, 4))
    }
    return urlradios.get(radionum, 'http://momori.animenfo.com:8000/?type=http&nocache=6391')


def radionaming(radionum):
    nameradios = {
        1: 'Anime NFO',
        2: 'Vocaloid Radio',
        3: 'Anime Night',
        4: 'Animu FM',
        5: 'Anime FM',
        6: 'Lofi Hip Hop Radio'
    }
    return nameradios.get(radionum, 'Desconhecido')


def radiocountryget(radionum):
    countryradios = {
        1: 'Japão',
        2: 'Japão',
        3: 'Brasil',
        4: 'Brasil',
        5: 'Brasil',
        6: 'EUA'
    }
    return countryradios.get(radionum, 'Desconhecido')


async def radioupdater(client):
    # noinspection PyGlobalUndefined
    global radiourl, radioname, radiocountry, counter
    while not client.is_closed():
        # Loop for para alterar o valor de x do 1 ao 6 (ultimo valor do for não é atribuido):
        for x in range(1, 7):
            counter = x
            radiourl = radiochooser(x)
            radioname = radionaming(x)
            radiocountry = radiocountryget(x)
            await asyncio.sleep(3600)


class Radio(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.channel.send("Desconectado da rádio.\nSe quiser sintonizar novamente, basta digitar /radio okay ;)")

    @commands.command()
    async def radio(self, ctx, command=None):
        # noinspection PyGlobalUndefined
        global counter
        if ctx.message.author.voice is None:
            return await ctx.channel.send("Parece que você não está em nenhum canal de voz...\n"
                                          "Por favor entre em algum e tente sintonizar novamente!")
        if command is not None:
            command = command.lower()
        voiceclient = ctx.voice_client
        channel = ctx.message.author.voice.channel
        embed = discord.Embed(
            title='',
            description='',
            colour=discord.Colour.blue()
        )
        embed.set_author(name='HitoriBOT Radio', icon_url=icon_image)
        embed.add_field(name=f'**Estação:**', value=f'{radioname}', inline=True)
        embed.add_field(name='**País:**', value=f'{radiocountry}', inline=True)
        radio = discord.FFmpegPCMAudio(source=radiourl, **ffmpeg_options)
        if command == 'next' and not None:
            if voiceclient.is_connected():
                if counter >= 6:
                    counter = 0
                localcounter = counter+1

                localurl = (radiochooser(localcounter))
                localname = (radionaming(localcounter))
                voiceclient.stop()
                message = await ctx.channel.send(f'Sintonizando com a estação **{localname}**')

                # Pode-se também usar voiceclient.source para alterar o valor do que se está reproduzindo atualmente.
                # Define uma rádio local e conecta a ela ao invés da rádio global.

                radiolocal = discord.FFmpegPCMAudio(source=localurl, **ffmpeg_options)
                await asyncio.sleep(5)
                try:
                    voiceclient.play(radiolocal)
                except discord.ClientException:
                    pass
                await message.delete()
                return await ctx.channel.send(f"```Você agora está ouvindo a estação: {localname}!```")

            else:
                await ctx.channel.send('Você precisa estar sintonizado a rádio para poder avançar estações!')

        elif command == 'update' and not None:
            counter = 1
            try:
                # Executa se o bot estiver conectado a um canal de voz e a uma estação.
                if voiceclient.is_playing() and voiceclient.is_connected() and command is not None:
                    voiceclient.stop()
                    radio = discord.FFmpegPCMAudio(source=radiourl, **ffmpeg_options)
                    voiceclient.play(radio)
                    await ctx.channel.send("```Conectado a estação da rádio atual!```")
                    return await ctx.channel.send(embed=embed)
                if voiceclient.is_connected() and not voiceclient.is_playing and command is not None:
                    await ctx.channel.send('Re-sintonizando com a estação da rádio...')

                else:
                    return await ctx.channel.send("Você precisa estar sintonizado à rádio para poder atualizar "
                                                  "estações!")
            except AttributeError:
                pass
        counter = 1
        try:
            # Executa se o bot estiver conectado a um canal de voz e a uma estação.
            if voiceclient.is_playing() and voiceclient.is_connected():
                await ctx.channel.send("```Você já está ouvindo a rádio HitoriBOT nesse servidor!\n"
                                       f"Estação atual da rádio: {radioname}\n"
                                       "Digite /radio update para sintonizar com essa estação!```")
                return await voiceclient.move_to(channel)

            if voiceclient.is_connected() and not voiceclient.is_playing():
                await ctx.channel.send("Sintonizando com a rádio principal novamente...")
                voiceclient.play(radio)

        # Quando o bot não está conectado, o VoiceClient sempre retorna erro ao tentar ser atribuido a uma variavel
        # Então, nesse caso, me aproveitei do erro para conectar o bot ao canal atual em cima dele.
        except AttributeError:
            await channel.connect()
            async with ctx.typing():
                radio = discord.FFmpegPCMAudio(source=radiourl, **ffmpeg_options)
                ctx.voice_client.play(radio)
                return await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(Radio(client))
    client.loop.create_task(radioupdater(client))
