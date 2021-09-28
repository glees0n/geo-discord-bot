import discord

from util import *
from streetview import StreetViewer

auth = read_yml("auth/auth.yml")

class GeoBot(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print('------')

streetviewer = StreetViewer(api_key=auth["GOOGLE_API_KEY"], location="47.5763831,-122.4211769")
streetviewer.fetchImageMetaData()
streetviewer.fetchImage()

client = GeoBot()
client.run(auth["DISCORD_TOKEN"])