import asyncio
import javascript
import time
import requests
import main
import datetime; print(datetime.datetime.now())
import importlib; importlib.reload(main)
import discord
from discord import app_commands
from discord.ext import commands
import logging
from javascript import require, On, Once
from dotenv import load_dotenv
import os
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log',encoding='utf-8',mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

mineflayer = require("mineflayer")
MC_BOT_ARGS = {
    "username": "Administrator",
    "host": "test25.aternos.me",
    "port": 21407,
    "version": "1.19.4",
    "hideErrors": False
}

reconnect = True

print(print("Connecting bot to Minecraft..."))
time.sleep(4)
mc_bot = mineflayer.createBot(MC_BOT_ARGS)

@On(mc_bot, "login")
def login(this):
    print(f"Connected: Bot Player '{mc_bot.username}'")

@On(mc_bot, "end")
def end(this, reason):
    print(f"Disconnected: Bot Player '{mc_bot.username}', {reason}")
    time.sleep(30)
    mineflayer.createBot(MC_BOT_ARGS)

@bot.event
async def on_ready():
    print(f"Loaded - {bot.user}")
    await bot.tree.sync()

@bot.event
async def on_member_join(member):
    await member.send("Welcome to the Server, {member.name}")

async def send_mc_chat_to_discord(username, message):
    channel = bot.get_channel(1563889414428426274)
    if channel is not None:
        await channel.send(f"**<{username}>** {message}")
    else:
        print("Discord channel not found; check the channel ID and bot access.")

@On(mc_bot, "chat")
def on_chat(this, username, message, *args):
    print(f"{username}: {message}")
    
    # Schedule the Discord send on the bot's asyncio loop.
    bot.loop.call_soon_threadsafe(
        lambda: asyncio.create_task(send_mc_chat_to_discord(username, message))
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "shit" in message.content:
        await message.author.send(f"{message.author.mention}, don't you dare use that word")
        await message.delete()
    await bot.process_commands(message)
    time.sleep(0.1)
    mc_bot.chat(message)

@bot.hybrid_command()
async def say(ctx: commands.Context, text: str):
    f"Makes {mc_bot.username} say a message of your hands"
    if text.startswith("/"):
        pass
    else:
        await ctx.send(f"{mc_bot.username} says {text}")
        time.sleep(0.1)
        mc_bot.chat(text)

@bot.hybrid_command()
async def run(ctx: commands.Context, text: str):
    f"Makes {mc_bot.username} runs a command of your choice"
    await ctx.send(f"{mc_bot.username} ran {text}")
    time.sleep(0.1)
    mc_bot.chat(f"/{text}")

@bot.hybrid_command()
async def disconnect(ctx: commands.Context):
    f"Disconnects {mc_bot.username}"
    time.sleep(0.1)
    mc_bot.kick()

@bot.hybrid_command()
async def jump(ctx: commands.Context):
    f"Makes {mc_bot.username} Jump"
    await ctx.send(f"{mc_bot.username} Jumped")
    time.sleep(0.1)
    mc_bot.setControlState('jump', True)
    mc_bot.setControlState('jump', False)

@bot.hybrid_command()
async def walk_forward(ctx: commands.Context):
    f"Makes {mc_bot.username} Walk Forward"
    await ctx.send(f"{mc_bot.username} Walked Forward")
    time.sleep(0.1)
    mc_bot.setControlState('forward', True)
    mc_bot.setControlState('forward', False)

@bot.hybrid_command()
@commands.has_permissions(kick_members=True)
async def kick(ctx: commands.Context, member: discord.Member, *, reason: str = "No Reason Provided"):
    "Kicks specified member (if you have permission)"
    try:
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member.mention}. Reason {reason}")
    except discord.Forbidden:
        await ctx.send(f"I don't have permissions to kick {member.mention}")
    except discord.HTTPException:
        await ctx.kick(reason="YOU'RE NOTHING MY MAN!, GIVE UP AND ABANADON YOUR LIFE!!!!!!!!!!!!!!!!!!!!, BECAUSE TONITGHTS THE FIGHT!")

@bot.hybrid_command()
async def member_list(ctx: commands.Context):
    "Shows the member list"
    if ctx.guild.chunked is False:
        await ctx.guild.chunk()

    member_list = [member.name for member in ctx.guild.members]
    members_string = ", ".join(member_list)
    
    if len(members_string) > 2000:
        await ctx.send("The member list is too long to send in a single message!")
    else:
        await ctx.send(f"**Members in this server:**\n{members_string}")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)