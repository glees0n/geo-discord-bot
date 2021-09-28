import discord

from util import *
from streetview import StreetViewer

auth = read_yml("auth/auth.yml")

class GeoBot(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print('------')

streetviewer = StreetViewer(api_key=auth["GOOGLE_API_KEY"], location="10 Clifford Street, Torrensville SA")
streetviewer.generateRandomLongLat()

client = GeoBot()
client.run(auth["DISCORD_TOKEN"])