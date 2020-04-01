import discord
from discord.ext import commands, tasks
import random
import pymongo
from pymongo import MongoClient




class Memory(commands.Cog):

    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(Memory(client))