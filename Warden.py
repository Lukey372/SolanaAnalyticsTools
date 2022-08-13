import asyncio
import base64
from tkinter import E
import base58
import json
import time
import discord
import discord.ext
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.api import Client
from solana.rpc.async_api import AsyncClient
from solana.system_program import create_account, CreateAccountParams
from spl.token.instructions import InitializeMintParams, MintToParams, create_associated_token_account, get_associated_token_address, initialize_mint, initialize_mint, mint_to, ApproveParams, approve
from solana.transaction import Transaction, TransactionInstruction, AccountMeta
from solana.rpc.types import TokenAccountOpts
from solana.rpc.commitment import Commitment
from solana.rpc.types import TxOpts
from solana.blockhash import Blockhash
from anchorpy import Program, Provider, Wallet
from datetime import datetime
from discord.ext import commands
from discord_slash import SlashCommand

client = commands.Bot(command_prefix='?')
client.remove_command('help')
slash = SlashCommand(client, sync_commands=True)

@slash.slash(description="Mints directly from a cmid")
async def cmid_mint(ctx, private_key: str, cmid:str, amount:int, rpc:str):
    try:
        SECRET_KEY = private_key
        CANDY_MACHINE_PUBLIC_ID = cmid
        RPC_ADDRESS = rpc
        SYSTEM_RECENT_BLOCKHASH_PROGRAM = 'SysvarRecentB1ockHashes11111111111111111111'
        SYSTEM_INSTRUCTIONS_PROGRAM = 'Sysvar1nstructions1111111111111111111111111'
        TOKEN_PROGRAM_ID = 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'
        ASSOCIATED_TOKEN_ID = 'ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL'
        CANDY_MACHINE_PROGRAM_ID = 'cndy3Z4yapfJBmL3ShUp5exZKqR3z33thTzeNMm2gRZ'
        SOLANA_CLIENT = Client(RPC_ADDRESS,timeout=120)
        METADATA_PUBLIC_KEY = 'metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s'
        SYSTEM_PROGRAM_ID = '11111111111111111111111111111111'
        SYSTEM_RENT_PROGRAM = 'SysvarRent111111111111111111111111111111111'
        SYSTEM_CLOCK_PROGRAM = 'SysvarC1ock11111111111111111111111111111111'
        OPTS = TxOpts(skip_preflight = True)
        MINT_LEN = 82

        def get_blockhash(client):
            while True:
                res = client.get_recent_blockhash(Commitment('recent'))
                blockhash = Blockhash(res['result']['value']['blockhash'])
                return blockhash
        
        payer = Keypair.from_secret_key(base58.b58decode(SECRET_KEY))
        mint_account = Keypair.generate()
        associated_token_account = get_associated_token_address(owner= payer.public_key, mint= mint_account.public_key)

        metadata_program_address = PublicKey.find_program_address(
            seeds=['metadata'.encode('utf-8'),
            bytes(PublicKey(METADATA_PUBLIC_KEY)),
            bytes(mint_account.public_key)
            ],
            program_id= PublicKey(METADATA_PUBLIC_KEY)
        )

        edition_program_address = PublicKey.find_program_address(
            seeds=['metadata'.encode('utf-8'),
            bytes(PublicKey(METADATA_PUBLIC_KEY)),
            bytes(mint_account.public_key),
            'edition'.encode('utf-8')
            ],
            program_id= PublicKey(METADATA_PUBLIC_KEY)
        )

        candy_machine_creator = PublicKey.find_program_address(
            seeds=[
                'candy_machine'.encode('utf-8'),
                bytes(PublicKey(CANDY_MACHINE_PUBLIC_ID))
            ],
            program_id= PublicKey(CANDY_MACHINE_PROGRAM_ID)
        )

        async def get_update_authority():
            client = AsyncClient(RPC_ADDRESS)
            provider = Provider(client, Wallet(Keypair.generate()))
            candyMachineAddress = CANDY_MACHINE_PUBLIC_ID
 
            program_id = PublicKey(CANDY_MACHINE_PROGRAM_ID)
 
            idl = await Program.fetch_idl(
                program_id,
                provider
            )
 
            program = Program(
                idl,
                program_id,
                provider
            )
 
            anchorProgram = program
 
            candyMachine = anchorProgram.account['CandyMachine'].fetch(candyMachineAddress)
 
            await program.close()
            return candyMachine.wallet

        candy_machine_authority = await get_update_authority()
        transaction = Transaction(fee_payer=payer.public_key)

        transaction.add(
            create_account(
                CreateAccountParams(
                    from_pubkey= payer.public_key,
                    new_account_pubkey= mint_account.public_key,
                    lamports= SOLANA_CLIENT.get_minimum_balance_for_rent_exemption(MINT_LEN)['result'],
                    space= MINT_LEN,
                    program_id= PublicKey(TOKEN_PROGRAM_ID)
                )
            )
        )

        transaction.add(
            initialize_mint(
                InitializeMintParams(
                    program_id= PublicKey(TOKEN_PROGRAM_ID),
                    mint= mint_account.public_key,
                    decimals= 0,
                    mint_authority= payer.public_key,
                    freeze_authority= payer.public_key
                )
            )
        )

        transaction.add(
            create_associated_token_account(
                payer= payer.public_key,
                owner= payer.public_key,
                mint = mint_account.public_key
            )
        )

        transaction.add(
            mint_to(
                MintToParams(
                    program_id= PublicKey(TOKEN_PROGRAM_ID),
                    mint= mint_account.public_key,
                    dest = associated_token_account,
                    mint_authority= payer.public_key,
                    amount= amount
                )
            )
        )

        async def get_wl_mint():
            client = AsyncClient(RPC_ADDRESS)
            provider = Provider(client, Wallet(Keypair.generate()))
            candyMachineAddress = CANDY_MACHINE_PUBLIC_ID
 
            program_id = PublicKey(CANDY_MACHINE_PROGRAM_ID)
 
            idl = await Program.fetch_idl(
                program_id,
                provider
            )
 
            program = Program(
                idl,
                program_id,
                provider
            )
 
            anchorProgram = program
 
            candyMachine = anchorProgram.account['CandyMachine'].fetch(candyMachineAddress)
 
            await program.close()
            ts = time.time()
            cmstockminused = str(candyMachine.data.items_available - candyMachine.items_redeemed)
            print('[' + datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') + '] '  + '\033[93m' + 'Items Redeemed: ' + str(candyMachine.items_redeemed)  + ' | Items Available: ' + str(candyMachine.data.items_available) + ' | Items Left: ' + cmstockminused + '\033[0m')
            return candyMachine.authority

        mint_wl = asyncio.run(get_wl_mint())
        associated_token_account = get_associated_token_address(owner=payer.public_key,mint=mint_account.public_key)
        whitelist_burn = Keypair.generate()
        whitelist_associated_acc = get_associated_token_address(owner=payer.public_key,mint=PublicKey(mint_wl))
        custom_program_id = PublicKey(CANDY_MACHINE_PROGRAM_ID)

        keys = [
            AccountMeta(pubkey=PublicKey(CANDY_MACHINE_PUBLIC_ID), is_signer= False, is_writable= True),
            AccountMeta(pubkey=PublicKey(candy_machine_creator[0]), is_signer= False, is_writable= False),
            AccountMeta(pubkey=payer.public_key, is_signer= True, is_writable= True),
            AccountMeta(pubkey=candy_machine_authority, is_signer= False, is_writable= True),
            AccountMeta(pubkey=metadata_program_address[0], is_signer= False, is_writable= True),
            AccountMeta(pubkey=mint_account.public_key, is_signer= True, is_writable= True),
            AccountMeta(pubkey=payer.public_key, is_signer= True, is_writable= True),
            AccountMeta(pubkey=payer.public_key, is_signer= True, is_writable= True),
            AccountMeta(pubkey=edition_program_address[0], is_signer= False, is_writable= True),
            AccountMeta(pubkey=PublicKey(METADATA_PUBLIC_KEY),is_signer= False, is_writable= False),
            AccountMeta(pubkey=PublicKey(TOKEN_PROGRAM_ID), is_signer= False, is_writable= False),
            AccountMeta(pubkey=PublicKey(SYSTEM_PROGRAM_ID), is_signer= False, is_writable= False),
            AccountMeta(pubkey=PublicKey(SYSTEM_RENT_PROGRAM), is_signer= False, is_writable= False),
            AccountMeta(pubkey=PublicKey(SYSTEM_CLOCK_PROGRAM), is_signer= False, is_writable= False),
            AccountMeta(pubkey=PublicKey(SYSTEM_RECENT_BLOCKHASH_PROGRAM), is_signer= False, is_writable= False),
            AccountMeta(pubkey=PublicKey(SYSTEM_INSTRUCTIONS_PROGRAM), is_signer= False, is_writable= False),
            AccountMeta(pubkey=PublicKey(whitelist_associated_acc), is_signer= False, is_writable= True),
            AccountMeta(pubkey=PublicKey(mint_wl), is_signer= False, is_writable= True),
            AccountMeta(pubkey=PublicKey(whitelist_burn.public_key), is_signer= True, is_writable= False)
        ]

        candy_machine_creator = PublicKey.find_program_address(
                    seeds=[
                    'candy_machine'.encode('utf-8'),
                    bytes(PublicKey(CANDY_MACHINE_PUBLIC_ID))
                        ],
                    program_id= PublicKey(CANDY_MACHINE_PROGRAM_ID)
        )

        numero = candy_machine_creator[1]
        numero = hex(numero)
        numero = numero.replace("0x","")
        to_convert= "d33906a70fdb23fb"+numero
        data = base58.b58encode(bytes.fromhex(to_convert))
        data = base58.b58decode(data.decode("utf-8"))

        transaction.add(
            TransactionInstruction(
                keys= keys,
                program_id= custom_program_id,
                data= data
            )
        )

        signers = [
            payer,
            mint_account,
            whitelist_burn
        ]

        transaction.recent_blockhash = get_blockhash(SOLANA_CLIENT)
        transaction.sign(*signers)
        transaction = transaction.serialize()

        txn_response = SOLANA_CLIENT.send_raw_transaction(transaction,OPTS)
        ts = time.time()
        print('[' + datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') + '] '  + '\033[92m' + 'Overseer Sent TX: ' + str(txn_response['result']) + '\033[0m')
    except Exception as e:
        print(e)

print("Client Started")
client.run('MTAwNzA1ODI1ODIzMTU1ODIyOA.GHdlmZ.J85jdb-bCDqYK8RyP7NoG4TvdN07QHo2pLZty8')

