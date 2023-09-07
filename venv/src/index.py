import discord
import config
import asyncio
import os
import src.config
from src.cogs import goal_cog

import src.config
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=src.config.BOT_PREFIX, intents=intents, application_id=src.config.BOT_ID)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}')


@bot.event
async def on_message(message):
    await bot.process_commands(message)

async def load():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')

async def main():
    await load()
    await bot.start(src.config.BOT_TOKEN)

asyncio.run(main())
