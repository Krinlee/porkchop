import os, discord
from dotenv import load_dotenv


load_dotenv()

DISCORD_API_SECRET = os.getenv("DISCORD_TOKEN")
GUILD = discord.Object(id=int(os.getenv("GUILD_ID")))
lchan = os.getenv('GOING_LIVE')
bchan = os.getenv('BOT_CHANNEL')
tchan = os.getenv('TEST_CHANNEL')
achan = os.getenv('ANS_CHANNEL')
tzone = os.getenv('TIME_ZONE')
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
DISCORD_ID = os.getenv('MY_USER_ID')
MY_ID = int(DISCORD_ID)
streamerName = os.getenv('STREAMER')
twitch_client_id = os.getenv('CLIENT_ID')
twitch_client_secret = os.getenv('CLIENT_SECRET')



