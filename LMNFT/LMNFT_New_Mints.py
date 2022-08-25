import requests, time, json, logging
from colorama import init,Fore
from discord_webhook import DiscordWebhook, DiscordEmbed
from dataclasses import dataclass

@dataclass
class Collection:
    name: str
    supply: int
    minted: int
    image: str

logging.basicConfig(format='[%(asctime)s] - %(message)s', level=logging.INFO)
init(autoreset=True, convert=True)

def get_new():
    while True:
        logging.info(Fore.LIGHTBLUE_EX + 'Monitoring . . . ')
        found_collections = open('./found.txt').read()


        data = requests.post('https://search.launchmynft.io/indexes/collections/search', json={"facetsDistribution":["type"],"attributesToCrop":["description:50"],"filter":[["type=\"Solana\""],"soldOut = false"],"attributesToHighlight":["*"],"limit":200,"sort":["deployed:desc"],"q":""}, headers={'X-Meili-API-Key': '3ee2cafe84ad0f0a28b2e8aea31df1f0e7adeed45973b24f0ab60307da150383'}, timeout=5).json()
        for i in range(len(data['hits'])):
            
            try:
                d = data['hits'][i]['description']
            except:
                d = ''
            
            current_id = data['hits'][i]['id']
            if data['hits'][i]['id'] not in found_collections:
                cover_image = 'https://pbs.twimg.com/profile_images/1479822011102863369/g8hTJXqg_400x400.jpg'
                logging.info(['Found -> Sent To Webhook'])
                internal_data = json.loads(str(requests.get('https://www.launchmynft.io/collections/' + data['hits'][i]['owner'] + '/' + data['hits'][i]['id']).text).split('type="application/json">')[1].split('</')[0])
                collection_url = 'https://www.launchmynft.io/collections/' + data['hits'][i]['owner'] + '/' + data['hits'][i]['id'] + ''
                try:   
                    if 'collectionCoverUrl' in internal_data['props']['pageProps']['collection']:
                        cover_image = str(internal_data['props']['pageProps']['collection']['collectionCoverUrl'])
                        cover_image = cover_image.replace('"', '')
                except KeyError:
                        continue

                collection_unix = internal_data['props']['pageProps']['collection']['launchDate']
                collection_seconds_unix = int((int(collection_unix) / 1000))

                deployment_unix = internal_data['props']['pageProps']['collection']['deployed']
                deployment_seconds_unix = int((int(deployment_unix) / 1000))

                hook_d = f"""
                Name - **{data['hits'][i]['collectionName']}**
                Link -  [Click Here]({collection_url})
                Chain - {data['hits'][i]['type']} ◎
                Supply - {str(data['hits'][i]['maxSupply'])}
                Price - {internal_data['props']['pageProps']['collection']['cost']} SOL
                Description - {d}
                
                LaunchDate - <t:{collection_seconds_unix}>
                Deployed - <t:{deployment_seconds_unix}>
                """
                webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1012223423826645092/m5RlSuASPWEU9R3SpvK4TOqpj-SLjkieNBbVPg7KjCkClsmKer64jlJnQO4I9YeymYPi')
                embed = DiscordEmbed(title='New LMNFT Collection', description=str(hook_d), color='0000')
                embed.set_timestamp()
                embed.set_thumbnail(url=cover_image)
                embed.set_footer(text='Created by colley#8131')
                webhook.add_embed(embed)
                webhook.execute()
                time.sleep(2)

def monitor_hot():
    data = requests.post('https://search.launchmynft.io/indexes/collections/search', json={"facetsDistribution":["type"],"attributesToCrop":["description:50"],"filter":[["type=\"Solana\""],"soldOut = false"],"attributesToHighlight":["*"],"limit":200,"sort":["deployed:desc"],"q":""}, headers={'X-Meili-API-Key': '3ee2cafe84ad0f0a28b2e8aea31df1f0e7adeed45973b24f0ab60307da150383'}, timeout=5).json()

get_new()