import discord, pymongo, requests, aiohttp, time, asyncio, dataclasses
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
from dataclasses import dataclass
from discord_slash import SlashCommand

client = commands.Bot(command_prefix='?')
client.remove_command('help')
slash = SlashCommand(client, sync_commands=True)
#mongo = pymongo.MongoClient("mongodb+srv://backend_user:Faggoted123@discordwhitelistbot.53exszw.mongodb.net/?retryWrites=true&w=majority")
#db = mongo.test

@client.event
async def on_ready():
    print('Bot Online')

@slash.slash(description="Submits user's wallet")
async def submit(ctx, wallet:str):
    print(f'{ctx.author_id} - wallet -> {wallet}')

@slash.slash(description="Returns the submitted wallet")
async def check(ctx):
    print(f'{ctx.author_id}')

@slash.slash(description="Remove submitted wallet")
async def delete(ctx, wallet:str):
    print(f'{ctx.author_id}')

@slash.slash(description="[DEV] Returns user's wallet to developer.")
async def get(ctx, user: discord.Member):
    print(f'{ctx.author_id}')

@slash.slash(description="[ADMIN] Starts giveaway")
async def startgiveaway(ctx, wallet:str):
    print(f'{ctx.author_id}')

client.run('MTAxMDE5NTUyNjYwNTYxNTIwNA.GRghpd.boPfQY2ZANM9JUe9o4AjfL6oa6lEumStdq0g1E')

