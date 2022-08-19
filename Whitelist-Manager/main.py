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
    #if query for ctx.author_id returns wallet -> return discord interaction already submitted with wallet
    #else submit ctx.author_id as search column and wallet as the value
    print(f'{ctx.author_id} - wallet -> {wallet}')

@slash.slash(description="Returns the submitted wallet")
async def check(ctx):
    #query for ctx.author_id and return wallet
    #else query returns empty return suggestion to submit their wallet using /submit
    print(f'{ctx.author_id}')

@slash.slash(description="Remove submitted wallet")
async def delete(ctx, wallet:str):
    #query for ctx.author_id -> if there is a value for wallet, remove the entry from db -> return success to user
    #else query does not return -> return to user that they should submit their wallet
    print(f'{ctx.author_id}')

@slash.slash(description="[DEV] Returns user's wallet to developer.")
async def get(ctx, id:int):
    #query for id parameter -> if user has submitted wallet return the query
    #else query returns nothing -> return user has not submitted wallet
    print(f'{ctx.author_id}')

@slash.slash(description="[ADMIN] Starts giveaway")
async def startgiveaway(ctx, wallet:str):
    #add parameters to this
    #use parameters to form new embed
    #add reaction for users to react to
    #when user reacts add them to array
    #use winners# parameter to pick that amount of people and add them to array, if a user is selected twice, do not add them to array again
    #refrence giveaway bot source for some of the logic
    print(f'{ctx.author_id}')

client.run('MTAxMDE5NTUyNjYwNTYxNTIwNA.GRghpd.boPfQY2ZANM9JUe9o4AjfL6oa6lEumStdq0g1E')

