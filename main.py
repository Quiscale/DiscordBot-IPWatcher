# #############################################################################
# Imports
# #############################################################################

import asyncio

import discord
import requests

# #############################################################################
# Constants
# #############################################################################

TOKEN = "BOT TOKEN HERE"


# #############################################################################
# Instances
# #############################################################################

client = discord.Client()
saved_ip = ""


# #############################################################################
# Bot stuff
# #############################################################################

@client.event
async def on_ready():
    print("Im ready !")

    await get_ip_and_send()


# #############################################################################
# Utils
# #############################################################################

async def get_ip_and_send():
    global saved_ip

    if client.is_ready():
        print("update ip")

        # Get the application public IP
        response = requests.get(r'https://ipv4.jsonip.com/')
        ip = response.json()["ip"]

        # If IP changed
        if saved_ip != ip:
            saved_ip = ip
            print("send ip")

            # Look for all channel where IP need to be sent
            for guild in client.guilds:
                for channel in guild.channels:
                    if isinstance(channel, discord.TextChannel):
                        if channel.name == "server_ip":
                            # Send IP
                            await channel.send(f"The server's IP is {ip}:25565")
    else:
        print("client not ready")


async def get_ip_loop():
    while True:
        await get_ip_and_send()
        await asyncio.sleep(60*60*6) # wait 6 hours


# #############################################################################
# Main
# #############################################################################

if __name__ == "__main__":

    # Run bot
    client.loop.create_task(get_ip_loop())
    client.run(TOKEN)
