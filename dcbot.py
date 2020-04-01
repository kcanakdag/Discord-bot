import discord
from discord.ext import commands
import os


client = commands.Bot(command_prefix='!')

@commands.has_permissions(manage_channels=True)
@client.command()
async def load(ctx, extension):  # extension is the cog we want to load
    client.load_extension(f'cogs.{extension}')

@commands.has_permissions(manage_channels=True)
@client.command()
async def unload(ctx, extension):  # extension is the cog we want to unload
    client.unload_extension(f'cogs.{extension}')


@commands.has_permissions(manage_channels=True)
@client.command()
async def reload(ctx, extension):  # extension is the cog we want to unload
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')  # Cutting of last 3 characters (.py)



client.run('Enter bot token')
