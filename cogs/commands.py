import discord
from discord.ext import commands
import requests
from random import choice
from random import shuffle
import time
import asyncio
from datetime import datetime, timedelta
from csv import DictReader
import pytz
import io
import aiohttp

client = commands.Bot(command_prefix = '!', case_insensitive = True)

class Commands(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def dad(self, ctx):
        url = "https://icanhazdadjoke.com/search"
        res = requests.get(
            url,
            headers={"Accept": "application/json"},
            params={"term": ""}
        ).json()
        input = res["results"]
        await ctx.send(choice(input)["joke"])

    @commands.command()
    async def time(self, ctx):
        embed = discord.Embed(title='Timezones', description='', colour=discord.Colour.blue())

        today = datetime.now()
        PRT = today.astimezone(pytz.timezone('UTC')).strftime("%H:%M:%S")
        PDT = today.astimezone(pytz.timezone('PST8PDT')).strftime("%H:%M:%S")
        ART = today.astimezone(pytz.timezone('America/Buenos_Aires')).strftime("%H:%M:%S")
        CET = today.astimezone(pytz.timezone('Europe/Berlin')).strftime("%H:%M:%S")

        embed.add_field(name="CET Central European Time(UTC +2)", value=CET, inline=False)
        embed.add_field(name="PRT Project Reality Time (UTC +0)", value=PRT, inline=False)
        embed.add_field(name="ART Argentina Time (UTC -3)", value=ART, inline=False)
        embed.add_field(name="PDT Pacific Daylight Time (UTC -7)", value= PDT, inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def tz(self, ctx, time, timezone):
        embed = discord.Embed(title='Timezone Converter', description='', colour=discord.Colour.blue())

        fmt = "%H:%M"
        timezones = {
            'CET': {'PRT': -2, 'ART': -5, 'PDT': -9},
            'PRT': {'CET': +2, 'ART': -3, 'PDT': -7},
            'ART': {'CET': +5, 'PRT': +3, 'PDT': -4},
            'PDT': {'CET': +9, 'PRT': +7, 'ART': +4},
        }

        local = datetime.strptime(time, "%H%M")

        if timezone in timezones:
            embed.add_field(name=timezone, value=local.strftime(fmt), inline=False)
            for tz in timezones[timezone]:
                other = int(timezones[timezone][tz])
                d = timedelta(hours=other)
                embed.add_field(name=tz, value=(local + d).strftime(fmt), inline=False)
            await ctx.send(embed=embed)

class Guessing_Game(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def game(self, ctx):
        game_intro_list = [
        "**Welcome to the WWII Guessing Game (Alpha)!**", 
        "+ For now the objects to guess are land vehicles.", 
        "+ A new image is posted every 24hrs (whether answered correctly or not).",
        "+ There are a total of 2 hints. Each will be posted every 8 hours.",
        "+ Please don't cheat, don't look at the image link."'\n',
        "**Reminder**",
        "+ The names may be written in a specific way! You may have the correct guess, but the names may be for example acronymed (i.e. PanzerKampfWagen = PzKpfw).",
        "+ Most of the German and British numbers (from 1-10) are written in Roman letters, other nations use numeric numbers.",
        "+ Capitalization (lower/upper case) is not important",
        "+ Some photos may not come with certain hints (mainly Manufacturer). Tough luck.",
        '\n'
        ]
        await ctx.send('\n'.join(game_intro_list))

        with open("data_archive.csv", "r", newline='') as file:
            csv_reader = DictReader(file)
            data_file = list(csv_reader)
            shuffle(data_file)

        while True:
            for i in data_file:
                embed = discord.Embed(title='Guess this photo:', description='', colour=discord.Colour.blue())
                embed.set_image(url=i['Picture'])
                await ctx.send(embed=embed)
                time.sleep(28800)
                await ctx.send(f'Country: {i["Country"]}')
                time.sleep(28800)
                try:
                    await ctx.send(f'Manufacturer: {i["Manufacturer"]}')
                except:
                    await ctx.send("Manufacturer Not Available")
                time.sleep(28800)
            time.sleep(86400)

def setup(client):
    client.add_cog(Commands(client))
    client.add_cog(Guessing_Game(client))