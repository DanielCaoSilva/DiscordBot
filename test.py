# bot.py
import os
import random
import string
from _ast import arg
from asyncio import sleep

import discord
import requests
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import asyncio
from discord import FFmpegPCMAudio
from discord.utils import get as dget
from youtube_dl import YoutubeDL
from requests import get


bot = commands.Bot(command_prefix=';')
# @bot.command()
# async def foo(ctx, arg):
#     await discord.message.channel.send('yo yo dawg')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()

stringMat = [r"C:\Users\dcaos\PycharmProjects\DiscordBot\babies.mp3",
             r"C:\Users\dcaos\PycharmProjects\DiscordBot\Oh_Baby_A_Triple.mp3",
             r"C:\Users\dcaos\PycharmProjects\DiscordBot\alright.mp3",
             r"C:\Users\dcaos\PycharmProjects\DiscordBot\breath-stinks.mp3",
             r"C:\Users\dcaos\PycharmProjects\DiscordBot\donkey.mp3",
             r"C:\Users\dcaos\PycharmProjects\DiscordBot\donkey.mp3"]



mp3Dict= {
    "babies": r"C:\Users\dcaos\PycharmProjects\DiscordBot\babies.mp3",
    "3": r"C:\Users\dcaos\PycharmProjects\DiscordBot\Oh_Baby_A_Triple.mp3",
    "alright":  r"C:\Users\dcaos\PycharmProjects\DiscordBot\alright.mp3",
    "donkey": r"C:\Users\dcaos\PycharmProjects\DiscordBot\donkey.mp3",
    "breath": r"C:\Users\dcaos\PycharmProjects\DiscordBot\breath-stinks.mp3",
    "ace": r"C:\Users\dcaos\PycharmProjects\DiscordBot\aceu.mp3"
}

#Get videos from links or from youtube search
def search(arg):
    with YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'}) as ydl:
        try: requests.get(arg)
        except: info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
        else: info = ydl.extract_info(arg, download=False)
    return info, info['formats'][0]['url']

# def get_Audio_Path(arg):
#     switcher = {
#         1: r"C:\Users\dcaos\PycharmProjects\DiscordBot\babies.mp3",
#         2: r"C:\Users\dcaos\PycharmProjects\DiscordBot\Oh_Baby_A_Triple.mp3",
#     }
#     return switcher.get(arg, "nothing")






@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)
    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')


@client.event
async def on_message(message):
    if message.content == "join":
        channel = message.author.voice.channel
        # await client.user.join_voice_channel(channel)
        await message.channel.send('Im trying')


@bot.command()
async def join(ctx):
    # author = ctx.message.author
    channel = ctx.author.voice.channel
    print('trying to join channel')
    await channel.connect()


@bot.command()
async def leave(ctx):
    print('leaving channel')
    await ctx.voice_client.disconnect()


# @bot.command()
# async def stream(ctx,arg):
#     print('trying to stream')

# @bot.command()
# async def play(ctx):
#     #guild = ctx.guild
#     guild = discord.utils.get(client.guilds, name=GUILD)
#     voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
#     #audio_source = discord.FFmpegOpusAudio(executable="C:/path/ffmpeg.exe", source="mp3.mp3"))
#     audio_source = discord.FFmpegPCMAudio('babies.mp3')
#     if not voice_client.is_playing():
#         voice_client.play(audio_source, after=None)


@bot.command()
async def play(ctx, *, query):
    #"""Plays a file from the local filesystem"""
    #Sample Command: ;play <path_name>
    audioPath = str(mp3Dict[str(query)])
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(audioPath))
    ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

    await ctx.send(f'Now playing: {query}')


@bot.command()
async def plays(ctx, *, query):
    FFMPEG_OPTS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    video, source = search(query)
    # guild = discord.utils.get(bot.guilds, name=GUILD)
    voice = dget(bot.voice_clients, guild=ctx.guild)

    #await join(ctx)
    #await ctx.send(f'Now playing {info['title']}.')
    voice.play(discord.FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: print('done', e))
    voice.is_playing()









#client.run(TOKEN)
bot.run(TOKEN)


