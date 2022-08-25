Instructions:

Requirements:
Webhook for Raffle: Replace in line 186 of overseer.py
Webhook for 5m Pumpwatch: Replace in line 234 of overseer.py
Webhook for 10m Pumpwatch: Replace in line 274 of overseer.py

Bot Permissions:
application.commands
Bot
Administrator

Commands:
/checkcreator (link to lmnft collection) - Returns the creator of a LaunchMyNft Collection, this command exists to stop people from shilling their own mints in dao chats.
/tps - Returns the current Solana TPS
/lmnft (link to lmnft collection) - Scrapes relevant information about a LaunchMyNft Collection.
/start_raffle_watch - Starts the FFF raffle watch and begins sending embeds to the webhook.
/pumpwatch5m - Starts 5m pumpwatch
/pumpwatch10m - Starts 10m pumpwatch
/dailysol (bearer) - Scrapes daily mints from SOLDecoder

LaunchMyNFT New Collections Scraper:
You can just replace the webhook on line 60, then run it via cmd. Fair warning this is a bit of a spammy feature, it sends a ton of embeds to the given channel.

Wallet-Monitor:
You can run multiple instances of this at the same time. I'm going to commit to index.js after I finish writing this to make sure the sleep time won't get you ratelimited. Each instance of the console application needs to be ran after updating config.json. Each wallet tracked needs it's own webhook, or you can keep it all in one channel with different name configured.

