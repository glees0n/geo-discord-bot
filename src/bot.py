import discord

from util import *

auth = loadYML("auth/auth.yml")

class GeoBot(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print('------')

client = GeoBot()
client.run(auth["DISCORD_TOKEN"])