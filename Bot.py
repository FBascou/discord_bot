import os
import discord
from discord.ext import commands

token = 'path/to/token'
client = commands.Bot(command_prefix = '!', case_insensitive = True)

@client.event
async def on_ready():
    print('We have logged in as Sgt. Bot {0.user}'.format(client))

path = 'path/to/cogs'
for filename in os.listdir(path):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(error)

@client.command()
@commands.has_permissions(manage_messages=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
@commands.has_permissions(manage_messages=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
@commands.has_permissions(manage_messages=True)
async def reload(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    client.unload_extension(f'cogs.{extension}')

client.run(token)








