
from datetime import datetime
import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.utils import get
from discord.ext import tasks
from constants import keywords
from constants import file_path
import logging
from database_clients.UserDb import UserDb

load_dotenv()

guilds = []

serverIds = str(os.getenv('SERVER_IDS')).split(',')
activity = discord.Activity(type=discord.ActivityType.listening, name=f"{ keywords.listening_activity }")

logging.basicConfig(filename=f"{ file_path.logs }", level=logging.INFO, format="%(asctime)s %(message)s")

for serverId in serverIds:
    guilds.append(discord.Object(id = serverId))


class PlumaClient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.all()
        intents.message_content = True
        super().__init__(intents=intents, activity=activity)
        self.synced = False    
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            for guild in guilds:
                print("`Bot`: Commands synced to server")
                try:            
                    await tree.sync(guild = guild)
                except Exception as e:
                    print(f"`Bot` Error: { e }")
            self.synced = True

client = PlumaClient() 
tree = app_commands.CommandTree(client)

# wait until the bot logs in 


@tree.command(name = "command", description = "Set Command", guilds = guilds)
async def command(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.defer()
    # do stuff here. Always start with defer if you'll be using DB Client.


token = str(os.getenv("BOT_TOKEN"))
client.run(token)
