import discord, pymongo, requests, aiohttp, time, asyncio, dataclasses
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
from dataclasses import dataclass
from discord_slash import SlashCommand

client = commands.Bot(command_prefix='?')
client.remove_command('help')
slash = SlashCommand(client, sync_commands=True)
mongo = pymongo.MongoClient("mongodb+srv://backend_user:Faggoted123@discordwhitelistbot.53exszw.mongodb.net/?retryWrites=true&w=majority")
db = mongo['Server']
info = db['Wallets']

@client.event
async def on_ready():
    print('Bot Online')

@slash.slash(description="Submits user's wallet")
async def submit(ctx, wallet:str):
    query = {"id": f"{ctx.author_id}"}
    do_query = info.find(query, {"_id": 0, "id": 0 })
    result = list(do_query)
    try:
        if len(result)!=0:
            wallet_return = result[0]['address'].replace("'","")
            await ctx.send(f"```Wallet is already submtted: {wallet_return}```", hidden=True)
        else:
            new_wallet = { "id": f"{ctx.author_id}", "address": f"{wallet}" }
            info.insert_one(new_wallet)
            await ctx.send(f"```{wallet} submitted for {ctx.author}```", hidden=True)

    except Exception as e:
        print(e)

@slash.slash(description="Returns the submitted wallet")
async def check(ctx):
    query = {"id": f"{ctx.author_id}"}
    do_query = info.find(query, {"_id": 0, "id": 0 })
    result = list(do_query)
    try:
        if len(result)==0:
            await ctx.send("```User has not submitted wallet, please submit using /submit```", hidden=True)
        else:
            wallet_return = result[0]['address'].replace("'","")
            await ctx.send(f"```{wallet_return}```", hidden=True)

    except Exception as e:
        print(e)

@slash.slash(description="Remove submitted wallet")
async def delete(ctx):
    query = {"id": f"{ctx.author_id}"}
    do_query = info.find(query, {"_id": 0, "id": 0 })
    result = list(do_query)
    try:
        if len(result) == 0:
            await ctx.send(f"```No wallet has been submitted, submit one using /submit```", hidden=True)
        else:
            await ctx.send("```Wallet has been removed, you may resubmit using /submit```", hidden=True)
            info.delete_one(query)
    except Exception as e:
        print(e)

@slash.slash(description="[ADMIN] Returns user's wallet to developer.")
async def get(ctx, id:str):
    query = {"id": f"{id}"}
    do_query = info.find(query, {"_id": 0, "id": 0 })
    result = list(do_query)
    try:
        if len(result) == 0:
            await ctx.send(f"```User has not submitted a wallet```", hidden=True)
        else:
            wallet_return = result[0]['address'].replace("'","")
            await ctx.send(f"```{wallet_return}```", hidden=True)
    except Exception as e:
        print(e)

@slash.slash(description="[ADMIN] Returns all submitted wallets as a text file")
async def txt(ctx):
    data = info.find({}, {"_id": 0, "id": 0})
    result = list(data)

    with open("./result.txt", "w") as file:
        for i in range(len(result)):
            file.write(str(result[i]['address']).replace(",","")+ "\n")

    with open("./result.txt", "rb") as file:
            await ctx.send("```Address File:```", file=discord.File(file, "./result.txt"), hidden=True)

client.run('MTAxMDE5NTUyNjYwNTYxNTIwNA.GRghpd.boPfQY2ZANM9JUe9o4AjfL6oa6lEumStdq0g1E')

