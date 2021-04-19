import discord
from discord.ext import commands
from discord.ext.commands import bot

import os
from os.path import join, dirname

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = ('')

description = '''Base project for discord.py-based Discord bots'''
bot = commands.Bot(command_prefix = BOT_PREFIX, description=description)

@bot.command(name='hi', description='Author info', aliases=['hello'], pass_context=True)
async def bot_info(ctx):
    msg = f'''Hello {str(ctx.message.author)}, this is a basic bot setup file for discord.py, by KeyBee#0811.
    The github repo: https://github.com/BaardsethK/discord.py-base-bot'''
    await ctx.send(msg)

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