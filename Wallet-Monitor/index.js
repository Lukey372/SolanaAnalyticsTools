const axios = require('axios')
const Discord = require('discord.js');
const config = require('./config.json');
const { Client, GatewayIntentBits, EmbedBuilder, WebhookClient } = require('discord.js');

//Config
const wallet = config.wallet
const name = config.name
const webhook = config.webhook

//Prevent Startup Webhook
let run_count = 0

//API
//Edit this to use just recent events instead of listing and sale
const api_url = "https://api.helius.xyz/v0/addresses"
const resource = "nft-events"
const options = `api-key=4f87c21f-e412-4d7d-9cb9-28424c83508b`

const webhookClient = new WebhookClient({ url: webhook });

//Empty var for most recent TX
let most_recent = "" 

//Wallet Vars
let latest = ""
let temp = ""


const init = async () => {
    try {
        const { data } = await axios.get(`${api_url}/${wallet}/${resource}?${options}&until=${most_recent}`)
        latest = data[0].description
        temp = data[0].description
        console.log("Initialized Monitor -> Listnening for TX Events: Most Recent List: " + latest.replace(wallet, name))
    }
    catch (err) {
        console.log(err)
    }
}

const monitor  = async () => {
    try {
        const { data } = await axios.get(`${api_url}/${wallet}/${resource}?${options}&until=${most_recent}`)
        latest = data[0].description
        mint = data[0].nfts[0].mint
        image_url = await getImage(mint)
        buyer = data[0].buyer
        seller = data[0].seller
        
        if (latest !== temp && run_count != 0) {
            const embed = new EmbedBuilder()
                .setTitle(`New Transaction`)
                .setDescription(`${latest.replace(wallet, name)}`)
                .setAuthor({ name: 'Overseer', iconURL: 'https://img.icons8.com/nolan/512/visible.png'})
                .setColor(0x00AE86)
                .setThumbnail(image_url)
                .addFields(
                    { name: 'Buyer', value: `[Click](https://solana.fm/address/${buyer}?cluster=mainnet-genesysgo)`, inline: true },
                    { name: 'Seller', value: `[Click](https://solana.fm/address/${seller}?cluster=mainnet-genesysgo)`, inline: true } ,
                    { name: 'Transaction', value: `[Click](https://www.solana.fm/tx/${data[0].signature}?cluster=mainnet-genesysgo)`, inline: true }
                )
                .setFooter({ text: 'Created by colley#8131' });
            
            webhookClient.send({ embeds: [embed] });
            temp = latest
        }
    }
    catch (err) {
        console.log(err)
    } 
} 

const getImage = async (mint) => {
    try {
        const url = "https://api.helius.xyz/v0/tokens/metadata?api-key=4f87c21f-e412-4d7d-9cb9-28424c83508b"
        const nftAddresses = [
            mint,
        ]
        const { data } = await axios.post(url, { mintAccounts: nftAddresses} )
        let image = data[0].offChainData.image
        if (image === undefined){
            image = ""
        }
        return image
    }
    catch (err) {
        console.log(err)
    }
}

function setTerminalTitle(title)
{
  process.stdout.write(
    String.fromCharCode(27) + "]0;" + title + String.fromCharCode(7)
  );
}

const startMonitor = async () => {
    try{
        monitor()
        run_count++
    }
    catch(err){
        console.log(err)
    }
    
}

async function main() {
    console.clear()
    setTerminalTitle(`Scythe - ${name} - ${wallet}`)
    console.log('\x1b[34m%s\x1b[0m','   ██████  ▄████▄▓██   ██▓▄▄▄█████▓ ██░ ██ ▓█████  \n ▒██    ▒ ▒██▀ ▀█ ▒██  ██▒▓  ██▒ ▓▒▓██░ ██▒▓█   ▀ \n ░ ▓██▄   ▒▓█    ▄ ▒██ ██░▒ ▓██░ ▒░▒██▀▀██░▒███   \n   ▒   ██▒▒▓▓▄ ▄██▒░ ▐██▓░░ ▓██▓ ░ ░▓█ ░██ ▒▓█  ▄ \n ▒██████▒▒▒ ▓███▀ ░░ ██▒▓░  ▒██▒ ░ ░▓█▒░██▓░▒████▒\n  ▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░ ██▒▒▒   ▒ ░░    ▒ ░░▒░▒░░ ▒░ ░\n ░ ░▒  ░ ░  ░  ▒  ▓██ ░▒░     ░     ▒ ░▒░ ░ ░ ░  ░')
    console.log('\x1b[34m%s\x1b[0m', `Loaded Config: \nName: ${name}\nWebhook: ${webhook}\nWallet: ${wallet}\n====================================================================================================================\n`)
    init()
    //add zero back after test
    setInterval(startMonitor, 150000)
}

main()
