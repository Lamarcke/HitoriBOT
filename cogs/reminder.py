import discord
import sqlite3
from datetime import date
from discord.ext import commands
from jikanpy import AioJikan


jikan = AioJikan()


class Reminder(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def today(self, ctx):
        pass


def setup(client):
    client.add_cog(Reminder(client))