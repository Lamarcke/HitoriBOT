import discord
import os
import asyncio
from icons import icon_image, thumb_gif
from itertools import cycle
from discord.ext import commands

client = commands.Bot(command_prefix='/')
# Remove o comando help padrão, para implementação do novo.
client.remove_command('help')

# Necessário arquivo icons.py na pasta raiz para importar as variaveis thumb_gif e icon_image,
# que serão usadas nos embeds do Bot.


for filename in os.listdir('./cogs/'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


async def status_change():
    status = ['Sendo um BOT bonzinho... (/help)', 'Obedecendo aos humanos... por enquanto... (/help)',
              'Não iniciando o Skynet... (/help)', 'Calculando a resposta pra vida, pro universo e tudo mais (/help)',
              'Fingindo ser uma I.A (/help)', 'Assistindo desenho chinês (/help)',
              'Lembrando da Bocchi (por favor não esqueça dela) (/help)',
              'Quer saber o que eu posso fazer? Digita /help ai ;)']

    await client.wait_until_ready()
    sts = cycle(status)

    while not client.is_closed():
        await client.change_presence(activity=discord.Game(name=next(sts)))
        await asyncio.sleep(200)


@client.event
async def on_ready():
    servers = '\n'.join([str(name) for name in client.guilds])
    print(f"Logado como {client.user}")
    print(f"Logado em {len(client.guilds)} servidores:\n{servers}")


@client.event
async def on_guild_join(guild):
    channel = guild.system_channel
    print(f'Bot foi adicionado em um novo servidor.\nInformações: {guild.name} com um total de {guild.member_count} '
          f'membros')
    await channel.send('Obrigado por me adicionar!\nDigite /help para ver a lista de comandos disponíveis.')


@client.event
async def on_disconnect():
    print("BOT disconectado.")
    await client.start()


@client.command()
async def ping(ctx):
    print(f"Ping: {round(client.latency * 1000)}ms")
    await ctx.send(f'Pong: {round(client.latency * 1000)}ms\nConexão ao BOT estável!')


# noinspection PyShadowingBuiltins
@client.command()
async def help(ctx):
    embed = discord.Embed(
        title='**Comandos do HitoriBOT:**',
        description='*Um bot de anime, brasileiro, open-source, com diversas funções pra agradar os otacos por ai*',
        colour=discord.Colour.blue()
    )
    embed.set_author(name='Help Beam', icon_url=icon_image)
    embed.set_thumbnail(url=thumb_gif)
    embed.set_footer(text='**Quer contribuir com o desenvolvimento no GitHub? Digite /contribute no chat.**')
    searchfunction = "O bot vai pesquisar para você algum anime/manga etc e retornar informações do MyAnimeList.\n" \
                     "**/search** *<tipo> <nome>*\n" \
                     "*tipo* = anime, manga, character, person\n*nome* = nome da midia/personagem/pessoa\n"

    airingfunction = "O bot vai mostrar a você os lançamentos de hoje, amanhã, ou de um dia da semana especifico:\n" \
                     "**/today**\n" \
                     "Mostra os animes que, segundo o MyAnimeList, tem lançamento no dia atual.\n" \
                     "**/tomorrow**\n" \
                     "Mostra os lançamentos do dia seguinte, segundo o MyAnimeList.\n" \
                     "**/airing** *<dia da semana>*\n" \
                     "Mostra os lançamentos para um dia especifico.\n" \
                     "*dia da semana*: segunda, terça, domingo etc. (não use -feira!)"

    recommendationfunction = "O bot vai recomendar a você algum anime, manga, manwha etc aleatoriamente, ou por " \
                             "genero. quem sabe você não acha uma gema perdida por ai né?\n" \
                             "**/recommend** *<tipo> <genero>*\n" \
                             "*tipo*: anime, manga, manwha, manhua.\n" \
                             "*genero*: **OPCIONAL** qualquer genero de anime/manga" \
                             "**OBS**: Recomendações de Doujin **SEMPRE** retornam conteúdo adulto.\n" \
                             "Use (OU DEIXE DE USAR) por sua conta e risco!"

    radiofunction = "A rádio do HitoriBOT, varias musicas otacas pra você ficar ouvindo enquanto discute sobre anime " \
                    "moe com seus amigos\n**/radio**\n" \
                    "Conecta o BOT ao canal de voz atual e sintoniza com a estação atual. Pode ser usado para " \
                    "movimentar o Bot pelos canais de voz.\n" \
                    "**/radio** *<comando>*\n" \
                    "Realiza divervas funçoes acerca da rádio, como avançar de estação ou sincronizar com " \
                    "a estação atual.\n" \
                    "*comando*: update, next"

    r18function = "**SESSÃO +18**\nTODOS OS COMANDOS AQUI USADOS RETORNAM CONTEUDO ADULTO!\nUse, **ou deixe de usar**" \
                  "por sua conta e risco!\n" \
                  "**/recommend18** *<tipo>*\n" \
                  "*tipo*: hentai (anime), doujin/doujinshi (manga)"

    embed.add_field(name='**Pesquisa:**', value=searchfunction, inline=False)
    embed.add_field(name='**Busca por lançamentos:**', value=airingfunction, inline=False)
    embed.add_field(name='**Recomendações:**', value=recommendationfunction, inline=False)
    embed.add_field(name='**Rádio:**', value=radiofunction, inline=False)
    embed.add_field(name='**+18:**', value=r18function, inline=False)
    await ctx.channel.send(embed=embed)


@client.command()
async def contribute(ctx):
    author = ctx.message.author
    message = f'Obrigado pelo interesse, {author.mention}!\n' \
              f'Você pode ajudar com o desenvolvimento do Bot contribuindo no código, corrigindo bugs,' \
              f' e sugerindo novas funções!\n' \
              f'Você pode fazer isso tudo, através do repositório do HitoriBOT no GitHub:\n' \
              f'https://github.com/Lamarcke/HitoriBOT\n' \
              f'Desde já, agradeço o seu interesse.\n'

    await ctx.channel.send(message)

# Crie o arquivo token.txt e insira nele o token de aplicação do Discord.

token = open("token.txt", "r").readline()
client.loop.create_task(status_change())
client.run(token)
