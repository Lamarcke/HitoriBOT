import discord
import os
import asyncio
from itertools import cycle
from discord.ext import commands

client = commands.Bot(command_prefix='/')

# Necessário arquivo icons.py na pasta raiz para importar as variaveis thumb_gif e icon_image,
# que serão usadas nos embeds do Bot.

for filename in os.listdir('./cogs/'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


async def status_change():
    status = ['Sendo um BOT bonzinho...', 'Obedecendo aos humanos... por enquanto...', 'Não iniciando o Skynet...',
              'Calculando a resposta pra vida, pro universo e tudo mais', 'Fingindo ser uma I.A',
              'Assistindo desenho chinês', 'Lembrando da Bocchi (por favor não esqueça dela)']
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
    print(f'Bot foi adicionado em um novo servidor.\nInformações: {guild.name} com um total de {guild.member_count}')
    await channel.send('Obrigado por me adicionar.\nDigite /help para ver a lista de comandos.')


@client.event
async def on_disconnect():
    print("BOT disconectado.")
    await client.start()


@client.event
async def on_member_join(member):
    print(f"{member} entrou no servidor {member.guild}!")
    await member.guild.send(f'{member.mention} entrou no servidor! Sejam bem vindo!')


@client.event
async def on_member_remove(member):
    print(f"{member} saiu do servidor {member.guild}!")


@commands.command()
async def ping(ctx):
    print(f"Ping: {round(client.latency * 1000)}ms")
    await ctx.send(f'Ping: {round(client.latency * 1000)}ms')


# Crie o arquivo token.txt e insira nele o token de aplicação do Discord.

token = open("token.txt", "r").readline()
client.loop.create_task(status_change())
client.run(token)
