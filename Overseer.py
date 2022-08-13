import discord, requests, aiohttp, time, asyncio, dataclasses
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
from dataclasses import dataclass
from discord_slash import SlashCommand

@dataclass
class Collection:
    name: str
    image: str
    update_time: str
    floor: float
    volume: float
    total_volume: float

client = commands.Bot(command_prefix='?')
client.remove_command('help')
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print('Overseer is Online')

async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command")
        print("Overseer Command Fail")

@slash.slash(description="Kicks a member from the Server.")
async def kick(ctx, user: discord.Member, *, reason="none"):
    try:
        await ctx.guild.kick(user)    
        kickembed=discord.Embed(title=":eye: User Kicked", description=f"{user} has been kicked.")
        kickembed.set_author(name="Overseer",
                        icon_url="https://img.icons8.com/nolan/64/visible.png")
        kickembed.set_footer(text="Created by colley#8131")
        await ctx.send(embed=kickembed)
        print(f"Overseer kicked {user}")
    except Exception as e:
        print('Overseer Unable to Kick User')

@slash.slash(description="Bans a member from the server.")
async def ban(ctx, user: discord.Member, *, reason="none"):
    try:
        await ctx.guild.ban(user)    
        banembed=discord.Embed(title=":eye: User Banned", description=f"{user} has been kicked.")
        banembed.set_author(name="Overseer",
                        icon_url="https://img.icons8.com/nolan/64/visible.png")
        banembed.set_footer(text="Created by colley#8131")
        await ctx.send(embed=banembed)
        print(f"Overseer kicked {user}")
    except Exception as e:
        print('Overseer Unable to Ban User')

@slash.slash(description="Clears channel and replaces it.")
async def clear(ctx, channel: discord.TextChannel = None):
    if channel == None: 
        await ctx.send("Invalid Channel")
        return
    clearembed=discord.Embed(title=":exclamation: Channel Cleared", description=f"#{channel.name} has been cleared.")
    clearembed.set_author(name="Overseer",
                        icon_url="https://img.icons8.com/nolan/64/visible.png")
    clearembed.set_footer(text="Created by colley#8131")
    clear_channel = discord.utils.get(ctx.guild.channels, name=channel.name)
    if clear_channel is not None:
        new_channel = await clear_channel.clone(reason="none")
        await clear_channel.delete()
        await new_channel.send(embed=clearembed)
        print(f"Overseer cleared the {channel.name} channel")
    else:
        await ctx.send(f"No channel named {channel.name} was found!")
        print(f"Overseer failed clear, invalid channel")

@slash.slash(description="Returns info on a launchmynft mint.")
async def checkcreator(ctx, url:str):
    info = url.split("/")
    index = len(info) - 2
    address = info[index]
    address_embed = discord.Embed(title="Creator Info", description=f"Matrica: [Click](https://www.Matrica.io/wallet/{address})\nSolscan: [Click](https://solscan.io/account/{address})\nNFTEyez: [Click](https://nfteyez.global/accounts/{address})")
    address_embed.add_field(name="Note", value="The creator of the collection may be using a burner wallet. Always practice caution when minting degen mints.")
    address_embed.set_author(name="Overseer",
                        icon_url="https://img.icons8.com/nolan/64/visible.png")
    address_embed.set_footer(text="Created by colley#8131")

    await ctx.send(embed=address_embed)
    print(f"Overseer checked {url}")

@slash.slash(description="Returns the current tps of Solana.")
async def tps(ctx):
    tps_resp = requests.get("https://api.solanart.io/get_solana_tps")
    parse_json = tps_resp.json()
    tps_embed = discord.Embed(title="TPS", description=f"Current TPS: {parse_json['tps']}")
    tps_embed.set_author(name="Overseer",
                        icon_url="https://img.icons8.com/nolan/64/visible.png")
    tps_embed.set_footer(text="Created by colley#8131")
    await ctx.send(embed=tps_embed)
    print(f"Overseer {ctx.message.author} checked TPS")

@slash.slash(description="Scrapes relevant info about a LaunchMyNFT collection.")
async def lmnft(ctx, url:str):
    try:
        info = url.split("/")
        wallet_address = index = len(info) - 2
        collection_id = index = len(info) - 1

        data_resp = requests.get(f"https://www.launchmynft.io/_next/data/oTz-rjSXIFBEBh7VzGFqx/collections/{info[wallet_address]}/{info[collection_id]}.json?userid={info[wallet_address]}&collectionid={info[collection_id]}")
        parse_json = data_resp.json()

        base_json = parse_json['pageProps']['collection']

        candy_id = base_json['newCandyMachineAccountId']
        image = base_json['collectionCoverUrl']
        owner = base_json['owner']
        collection_name = base_json['collectionName']
        minted_last_30 = base_json['mintedLast30mins']
        max_supply = base_json['maxSupply']
        total_mints = base_json['totalMints']

        
        info_embed = discord.Embed(title=f"{collection_name}", description=f"Candy ID: {candy_id}\nOwner: {owner}\nMinted Last 30mins: {minted_last_30}\nSupply: {total_mints}/{max_supply}")
        info_embed.set_author(name="Overseer",
                            icon_url="https://img.icons8.com/nolan/64/visible.png")
        info_embed.set_footer(text="Created by colley#8131")
        info_embed.set_image(url=image)
        await ctx.send(embed=info_embed)
        print(f"Overseer checked {url}")
    except Exception as e:
        print("Overseer failed to scrape info -> possible next update")

@slash.slash(description="Starts famous fox raffle watcher.")
async def start_raffle_watch(ctx):
    try:
        while True:
            url = "https://rafffle.famousfoxes.com/foxy/raffles/featured"
            obj = {
                "drift": 0,
                "sort": [
                    "end",
                    1
                ],
                "period": "featured"
            }

            headers = {
                'authority': 'rafffle.famousfoxes.com',
                'path': '/foxy/raffles/featured',
                'scheme': 'https',
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'text/plain;charset=UTF-8',
                'origin': 'https://rafffle.famousfoxes.com',
                'referer': 'https://rafffle.famousfoxes.com',
                'cookie': 'session=629145c2-0fb0-4416-8452-4e39c1335ce8; cf_clearance=_E01Qs8uIHAvoPO3g6X4jaJAjqVQxOG2l.._NpQRGBc-1659639631-0-150',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            }
            count = 0
            resp = requests.post(url, json=obj, headers=headers)
            resp_json = resp.json()
            print("Overseer is checking raffles")
            for keys in resp_json:
                nft_image = resp_json[count]['nft']['image']
                nft_name = resp_json[count]['nft']['name']
                end_time = resp_json[count]['end']
                tickets_status = f"{resp_json[count]['sold']}/{resp_json[count]['supply']}"
                token_address = resp_json[count]['mint']
                percent_remaining = resp_json[count]['left'] * 100
                percent_remaining_str = f"{percent_remaining:.2f}%"
                token_cost = resp_json[count]['cost']
                raffle_id = resp_json[count]['raffle']

                token_resp = requests.get(f"https://api.solscan.io/account?address={token_address}&cluster=")
                token_resp_json = token_resp.json()
                if resp_json[count]['left'] >= 0.9 or resp_json[count]['left'] >= 0.8:
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url('https://discord.com/api/webhooks/1004806919162187786/L2rMqeeFcG_71ul6vqIsoolDuLxAkYaBjDRempSwk2rxtEmgwVUnoq2k8lbPuID1Bvbf', adapter=AsyncWebhookAdapter(session))

                        e = discord.Embed(title="Raffle Alert", description=f"Name: {nft_name}\nEnd Time: <t:{end_time}>\nTickets Status: {tickets_status}\nPercent Remaining: {percent_remaining_str}\nCost: {token_cost} {token_resp_json['data']['tokenInfo']['symbol']}\nLink: [Click Here](https://rafffle.famousfoxes.com/raffle/{raffle_id})", color=discord.Color.purple())
                        e.set_image(url=nft_image)
                        e.set_author(name="Overseer",
                                icon_url="https://img.icons8.com/nolan/64/visible.png")
                        e.set_footer(text="Created by colley#8131")

                        await webhook.send(embed=e)
                count+=1
            print("Overseer finished checking raffle cycle -> running again in 1 hour")
            await asyncio.sleep(3600)
            print("Overseer finished sleep, loading again")
    except Exception as e:
        print("User tried to execute without admin.")
  
@slash.slash(description="Starts magic eden pumpwatch.")
async def pumpwatch5m(ctx):
    try:
        while True:
            collections_info = requests.get("https://stats-mainnet.magiceden.io/collection_stats/popular_collections/sol?limit=20")
            collections_info_json = collections_info.json()
            top5_min_volume = collections_info_json['top5m']

            first_count = 0
            collections = []
            for keys in top5_min_volume:
                collections.append(Collection(top5_min_volume[first_count]['name'],
                top5_min_volume[first_count]['image'],
                top5_min_volume[first_count]['updatedAt'],
                top5_min_volume[first_count]['fp'],
                top5_min_volume[first_count]['vol'],
                top5_min_volume[first_count]['totalVol']
                ))
                first_count+=1
            
            second_count = 0
            for keys in collections:
                e = discord.Embed(title="Pump Alert", 
                description=f"Name: {collections[second_count].name}\nFP: {(collections[second_count].floor)/1000000000}\n5m Volume: {collections[second_count].volume}\nTotal Volume: {collections[second_count].total_volume:.2f}", color=discord.Color.purple())
                e.set_image(url=collections[second_count].image)
                e.set_author(name="Overseer",
                                icon_url="https://img.icons8.com/nolan/64/visible.png")
                e.set_footer(text="Created by colley#8131")
                if collections[second_count].volume > 10 and (collections[second_count].floor / 1000000000) != collections[second_count].volume and collections[second_count].volume - (collections[second_count].floor / 1000000000) > 1:
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url('https://discord.com/api/webhooks/1005635289387110460/YvcD_FRAsuCMwRSD2Lo317FUQgCiMns2U1jVt8g23EJaktkKlgGBq0BBy9RwWF6Z9qsl', adapter=AsyncWebhookAdapter(session))
                        await webhook.send(embed=e)
                        print('Pump Alert Sent')
                second_count+=1
            await asyncio.sleep(240)
    except Exception as e:
        print("User tried to execute without admin.")

@slash.slash(description="Starts magic eden pumpwatch.")
async def pumpwatch10m(ctx):
    try:
        while True:
            collections_info = requests.get("https://stats-mainnet.magiceden.io/collection_stats/popular_collections/sol?limit=20")
            collections_info_json = collections_info.json()
            top5_min_volume = collections_info_json['top10m']

            first_count = 0
            collections = []
            for keys in top5_min_volume:
                collections.append(Collection(top5_min_volume[first_count]['name'],
                top5_min_volume[first_count]['image'],
                top5_min_volume[first_count]['updatedAt'],
                top5_min_volume[first_count]['fp'],
                top5_min_volume[first_count]['vol'],
                top5_min_volume[first_count]['totalVol']
                ))
                first_count+=1
            
            second_count = 0
            for keys in collections:
                e = discord.Embed(title="Pump Alert", 
                description=f"Name: {collections[second_count].name}\nFP: {(collections[second_count].floor)/1000000000}\n10m Volume: {collections[second_count].volume}\nTotal Volume: {collections[second_count].total_volume:.2f}", color=discord.Color.purple())
                e.set_image(url=collections[second_count].image)
                e.set_author(name="Overseer",
                                icon_url="https://img.icons8.com/nolan/64/visible.png")
                e.set_footer(text="Created by colley#8131")
                if collections[second_count].volume > 10 and (collections[second_count].floor / 1000000000) != collections[second_count].volume and collections[second_count].volume - (collections[second_count].floor / 1000000000) > 1:
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url('https://discord.com/api/webhooks/1007806571302092831/BZ6LaTvBJMA5Wvtdpr4y8xJZc4UUQNJEkreiw_NenMXpaoyica-bDmrMGLwT1K_mvMJ9', adapter=AsyncWebhookAdapter(session))
                        await webhook.send(embed=e)
                        print('Pump Alert Sent')
                second_count+=1
            await asyncio.sleep(240)
    except Exception as e:
        print("User tried to execute without admin.")

@slash.slash(description="Starts magic eden pumpwatch.")
async def dailysol(ctx, bearer:str):
    count = 0
    headers = {
    'authorization': f'{bearer}'
    } 
    daily_mints = requests.get('https://us-central1-nft-discord-relay.cloudfunctions.net/api/getTodaysMints', headers=headers)
    daily_mints_json = daily_mints.json()
    date = daily_mints_json['data']['date']
    daily = discord.Embed(title="Daily Mints", description=f"Mints for {date}", color=discord.Color.purple())
    await ctx.send(embed=daily)
    green_react = "🟢"
    yellow_react = "🟡"
    red_react = "🔴"
    
    for keys in daily_mints_json['data']['mints']:
        image = daily_mints_json['data']['mints'][count]['image']
        name = daily_mints_json['data']['mints'][count]['project']
        twitter = daily_mints_json['data']['mints'][count]['twitterLink']
        discord_link = daily_mints_json['data']['mints'][count]['discordLink']
        mint_time = daily_mints_json['data']['mints'][count]['time']
        supply = daily_mints_json['data']['mints'][count]['count']
        mint_price = daily_mints_json['data']['mints'][count]['price']
        if image == "":
            image = "https://img.icons8.com/nolan/512/visible.png"
        mint_embed = discord.Embed(title=f"{name}", description=f"Twitter: [Click]({twitter})\nDiscord: [Click]({discord_link})\nMint Time: {mint_time}\nSupply: {supply}\nPrice: {mint_price} ◎", color=discord.Color.purple())
        mint_embed.set_image(url=image)
        msg = await ctx.send(embed=mint_embed)
        await msg.add_reaction(green_react)
        await msg.add_reaction(yellow_react)
        await msg.add_reaction(red_react)
        count+=1


client.run('MTAwNDUzNjcyNTQ5MTY5NTY4Ng.GyS4EW.sa0KnpPcZO2HSn0srzw60KCbsMzo92rAXEu6xw')