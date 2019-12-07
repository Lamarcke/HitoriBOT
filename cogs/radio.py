import discord
import asyncio
import youtube_dl
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


def radiochooser(radionum):
    urlradios = {
        1: 'http://momori.animenfo.com:8000/?type=http&nocache=6391',  # Anime NFO, Japan
        2: 'http://curiosity.shoutca.st:8019/stream',  # Vocaloid Radio, Japan
        3: 'http://stm11.srvstm.com:8356/app128/',  # Anime Night, Brasil
        4: 'http://cast.animu.com.br:9021/autodj',  # Animu FM, Brasil
        5: 'http://stream2.laut.fm/animefm'  # Anime FM, Brasil
    }
    return urlradios.get(radionum, 'http://momori.animenfo.com:8000/?type=http&nocache=6391')


def radionaming(radionum):
    nameradios = {
        1: 'Anime NFO',
        2: 'Vocaloid Radio',
        3: 'Anime Night',
        4: 'Animu FM',
        5: 'Anime FM'
    }
    return nameradios.get(radionum, 'Desconhecido')


def radiocountryget(radionum):
    countryradios = {
        1: 'Japão',
        2: 'Japão',
        3: 'Brasil',
        4: 'Brasil',
        5: 'Brasil'
    }
    return countryradios.get(radionum, 'Desconhecido')


async def radioupdater(client):
    # noinspection PyGlobalUndefined
    global radiourl, radioname, radiocountry, counter
    while not client.is_closed():

        for x in range(1, 6):
            counter = x
            radiourl = radiochooser(x)
            radioname = radionaming(x)
            radiocountry = radiocountryget(x)
            await asyncio.sleep(2700)


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

        if command == 'next' and not None:
            if voiceclient.is_playing() and voiceclient.is_connected():
                if counter >= 5:
                    counter = 0
                counter += 1
                num = counter

                localurl = (radiochooser(num))
                localname = (radionaming(num))
                voiceclient.stop()

                # Pode-se usar voiceclient.source para alterar o valor do que se está reproduzindo atualmente.

                radiolocal = discord.FFmpegPCMAudio(source=localurl, **ffmpeg_options)
                voiceclient.play(radiolocal)
                return await ctx.channel.send(f"```Você agora está ouvindo a estação: **{localname}**!```")

            else:
                await ctx.channel.send('Você precisa estar sintonizado a rádio para poder avançar estações!')

        elif command == 'update' and not None:
            counter = 1
            try:
                if voiceclient.is_playing() and voiceclient.is_connected() and command == 'update' or 'up':
                    voiceclient.stop()
                    radio = discord.FFmpegPCMAudio(source=radiourl, **ffmpeg_options)
                    voiceclient.play(radio)

                    await ctx.channel.send("```Rádio atualizada!```")
                    return await ctx.channel.send(embed=embed)
                else:
                    return await ctx.channel.send("Você precisa estar sintonizado à rádio para poder atualizar "
                                                  "estações!")
            except AttributeError:
                pass

        try:
            if voiceclient.is_playing() and voiceclient.is_connected():
                await ctx.channel.send("```Você já está ouvindo a rádio HitoriBOT nesse servidor!\n"
                                       f"Estação atual da rádio: {radioname}\n"
                                       "Digite /radio update para sintonizar com a estação atual!```")
                return await voiceclient.move_to(channel)

        except AttributeError:
            await channel.connect()

        counter = 1
        async with ctx.typing():
            radio = discord.FFmpegPCMAudio(source=radiourl, **ffmpeg_options)
            ctx.voice_client.play(radio)
            return await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(Radio(client))
    client.loop.create_task(radioupdater(client))
