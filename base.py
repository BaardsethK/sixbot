import discord
from discord.ext import tasks, commands
from discord.ext.commands import bot
import requests
import base64
import json

import os
from os.path import join, dirname

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.getenv('DISCORD_TOKEN')
STAT_USERNAME = os.getenv('STATSDB_USERNAME')
STAT_PASSWORD = os.getenv('STATSDB_PASSWORD')
BOT_PREFIX = ('!6 ')

LOOP_TIME=60

description = '''Bot for playerstats and data for Rainbow 6 Siege Discord-servers'''
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = BOT_PREFIX, description=description, intents=intents)

rankings = {
    0 : "Unranked",
    1 : "Copper V",
    2 : "Copper IV",
    3 : "Copper III",
    4 : "Copper II",
    5 : "Copper I",
    6 : "Bronze V",
    7 : "Bronze IV",
    8 : "Bronze III",
    9 : "Bronze II",
    10 : "Bronze I",
    11 : "Silver V",
    12 : "Silver IV",
    13 : "Silver III",
    14 : "Silver II",
    15 : "Silver I",
    16 : "Gold III",
    17 : "Gold II",
    18 : "Gold I",
    19 : "Platinum III",
    20 : "Platinum II",
    21 : "Platinum I",
    22 : "Diamond",
    23 : "Champion" 
}

# Has to be set manually on server.
rank_roles = [
    "Unranked",
    "Copper",
    "Bronze",
    "Silver",
    "Gold",
    "Platinum",
    "Diamond",
    "Champion"
]

def get_role_by_name(ctx, role_name):
    try:
        role = [role for role in ctx.guild.roles if role.name == role_name]
        return role
    except:
        print(f"Role with name {role_name} does not exist")
    else:
        return None

async def get_player_stats(player_name):
    url = 'https://api.statsdb.net/r6/pc/player/{}'.format(player_name)
    auth_data = STAT_USERNAME+":"+STAT_PASSWORD
    auth_b64 = base64.b64encode(auth_data.encode("utf-8"))
    headers = {'Authorization': 'Basic {}'.format(str(auth_b64, "utf-8"))}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        response_json = json.loads(r.text)
        return response_json
    except requests.HTTPError as exceptption:
        print(exceptption)

async def set_role_by_rank(ctx, member, rank):
    print("Setting player rank")

    rank = rank.split(' ', 1)[0]
    try:
        role = get_role_by_name(ctx, rank)
        if role == None:
            raise Exception("Failed to find role by rank name")
        
        await member.edit(roles=[], reason="Rank roles autoremoved by SixBot")
        await member.edit(roles=role, reason="Rank role autoadd by SixBot")
    except discord.HTTPException as e:
        print("Changing roles failed", e)
    except discord.Forbidden as e:
        print("Permission error when changing roles")


@bot.command(name='hi', description='Author info', aliases=['hello'], pass_context=True)
async def bot_info(ctx):
    msg = f'''Hello {str(ctx.author.display_name)}, I get stats for Rainbow 6 players.
    The github repo: https://github.com/BaardsethK/discord.py-base-bot'''
    await ctx.send(msg)

@bot.command(name='stats', description='Get player stats', pass_context=True)
async def player_stats(ctx):
    await ctx.message.delete()
    player = ctx.author.display_name

    response = await get_player_stats(player)

    rank = rankings[int(response["payload"]["stats"]["seasonal"]["ranked"]["rank"])]
    mmr = response["payload"]["stats"]["seasonal"]["ranked"]["mmr"]
    kills = response["payload"]["stats"]["seasonal"]["ranked"]["kills"]
    deaths = response["payload"]["stats"]["seasonal"]["ranked"]["deaths"]
    wins = response["payload"]["stats"]["seasonal"]["ranked"]["wins"]
    losses = response["payload"]["stats"]["seasonal"]["ranked"]["losses"]

    if deaths == 0:
        deaths = 1

    if (wins + losses) == 0:
        msg = f'''```Player: {player}
        Rank: {rank} ({mmr}p)
        No matches played```
        '''
    else:
        msg = f'''```Player: {player}
        Rank: {rank} ({mmr}p)
        K/D: {format(kills / deaths, '.2f')} [{kills}/{deaths}]
        W/L: {format(100 / (wins + losses) * wins, '.2f')}% [{wins}/{losses}]```
        '''
    await ctx.send(msg)
    await set_role_by_rank(ctx, ctx.author, rank)


@bot.command(name='allstats', pass_context=True)
async def test_all_player_stats(ctx):
    members = ctx.channel.members
    msg = 'Current player rankings:```'
    players = {}
    for member in members:
        if not member.bot: 
            player_name = member.display_name
            try: 
                response = await get_player_stats(player_name)
                rank = rankings[int(response["payload"]["stats"]["seasonal"]["ranked"]["rank"])]
                mmr = response["payload"]["stats"]["seasonal"]["ranked"]["mmr"]
                players[player_name] = [rank,mmr]
                await set_role_by_rank(ctx, member, rank)
            except:
                print("Error setting player rank/stats")                

    ordered = dict(sorted(players.items(), key=lambda item: item[1][1], reverse=True))

    for player in ordered.items():
        msg += f"\n\t{player[0]} : {player[1][0]}"
        msg += f"\n\t\tMMR : {player[1][1]}\n"

    msg += "```"
    await ctx.channel.send(msg)

@bot.event
async def on_message(message):
    if not message.author.bot:
        await bot.process_commands(message)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(TOKEN)