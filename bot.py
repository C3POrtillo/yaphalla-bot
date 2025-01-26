import datetime

import discord
from discord.ext import tasks

BOT_TOKEN = "bot-token-that-has-been-redacted"
SERVER_ID = 1332875298668154900
LOG_CHANNEL_ID = 1332878709870301287

CHANNEL_IDS = [1332875747416870974,
               1332875766194638898,
               1332875812222930944,
               1332876430371192833,
               1332876459592781884,
               1332876517256069200,
               1332876541499146240,
               1332876612135292959
               ]

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True

bot = discord.Client(intents=intents)

counter = 0

@bot.event
async def on_ready():
    print(bot.user)
    rotate_channels.start()

@tasks.loop(seconds=15)
async def rotate_channels():
    global counter

    START_DATE = datetime.datetime(2025, 1, 24)
    elapsed_days = (datetime.datetime.utcnow() - START_DATE).days

    real_channel_idx = elapsed_days % len(CHANNEL_IDS)
    real_active_channel_id = CHANNEL_IDS[(real_channel_idx + 1) % len(CHANNEL_IDS)]

    channel_idx = counter % len(CHANNEL_IDS)
    counter += 1

    inactive_channel_id = CHANNEL_IDS[channel_idx]
    active_channel_id = CHANNEL_IDS[(channel_idx + 2) % len(CHANNEL_IDS)]

    guild = bot.get_guild(SERVER_ID)
    if guild is None:
        print("Server not found.")
        return

    log_channel = guild.get_channel(LOG_CHANNEL_ID)
    if log_channel is None:
        print("Log channel not found.")
        return

    try:
        real_active_channel = guild.get_channel(real_active_channel_id)
        
        await log_channel.send("------")
        await log_channel.send("Activating channels for demonstration purposes")
        await log_channel.send("Real channel based on today's date should be {}.".format(real_active_channel.name))
        await log_channel.send("------")
    
    except Exception as e:
        print("Failed to send message: {}".format(e))

    for channel_id in [active_channel_id, inactive_channel_id]:
        channel = guild.get_channel(channel_id)
        if channel is None:
            continue

        try:
            if channel_id == active_channel_id:
                await channel.set_permissions(guild.default_role, view_channel=True)
                await log_channel.send("Showing channel: {}".format(channel.name))
            
            elif channel_id == inactive_channel_id:
                await channel.set_permissions(guild.default_role, view_channel=False)
                await log_channel.send("Hiding channel: {}".format(channel.name))
        except Exception as e:
            await log_channel.send("Failed to update channel {}: {}".format(channel.name, e))

bot.run(BOT_TOKEN)
