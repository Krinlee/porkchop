import discord, requests, json, pytz, settings as settings
from discord.ext import tasks, commands
from twitchAPI.twitch import Twitch
from discord.utils import get
from datetime import datetime
from datetime import date
from settings import *
global userid, stream_data
from config import secrets

logger = settings.logging.getLogger('twitch')

timezone = pytz.timezone(secrets.tzone)
datetime_ = datetime.now(timezone)
today = date.today()
target_channel_id = int(secrets.lchan)
streamer_name = secrets.streamerName
client_id = secrets.twitch_client_id
client_secret = secrets.twitch_client_secret
twitch = Twitch(client_id, client_secret)
TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/helix/streams"

body = {
    'client_id':client_id,
    'client_secret':client_secret,
    'grant_type':'client_credentials'
}
r = requests.post('https://id.twitch.tv/oauth2/token', body)
keys = r.json()
API_HEADERS = {
	'Client-ID': client_id,
	'Authorization':'Bearer ' + keys['access_token']
}

async def authenticate():
	await twitch.authenticate_app([])



def checkuser(user):
    url = TWITCH_STREAM_API_ENDPOINT_V5.format(userid)
    
    try:
        if len(stream_data['data']) == 1:
            return True
        else:
            return False
    except Exception as e:
        return False

class twitchLive(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.live_notifs_loop.start()

    def cog_unload(self) -> None:
        self.live_notifs_loop.stop()

    @tasks.loop(seconds=15)
    async def live_notifs_loop(self):
        global userid, stream_data
        await twitch.authenticate_app([])
        userid = requests.get(f'https://api.twitch.tv/helix/streams?user_login={streamer_name}', headers=API_HEADERS)
        stream_data = userid.json()
        with open(f'{ASSET_DIR}/streamers.json', 'r') as file:
            streamers = json.loads(file.read())
        guild = self.bot.get_guild(secrets.GUILD)
        channel = self.bot.get_channel(target_channel_id)
        for user_id, twitch_name in streamers.items():
            status = checkuser(twitch_name)
            user = self.bot.get_user(int(user_id))
            if status is True:
                async for message in channel.history(limit=200):
                    if str(user.mention) in message.content and "is now streaming" in message.content:
                        break
                    else:
                        await channel.send(
                            f":red_circle: **LIVE**\nHey everyone !!!\n{user.mention} is now streaming on Twitch!"
                            f"\nhttps://www.twitch.tv/{twitch_name}")
                        logger.info({
                            "Streamer": twitch_name,
                            "Status": 'Online',
                            "Message": "Krinlee just went live"
                            })
                        break
            else:
                async for message in channel.history(limit=200):
                    if str(user.mention) in message.content and "is now streaming" in message.content:
                        logger.info({
                            "Streamer": twitch_name,
                            "Status": 'Offline',
                            "Message": "Krinlee just went dark"
                            })
                        await message.delete()
        
            
    @commands.command()
    async def start_live_notifs(self,ctx):
        if ctx.author.id != secrets.MY_ID:
            await ctx.send("You don't have permission to do this!")
            logger.info({
                f"{ctx.author.name} tried to start Twitch notifications!"
            })
        else:
            self.trivia.start()
            logger.info({
                f"{ctx.author.name} started trivia"
            })
    
        
    @commands.command()
    async def stop_live_notifs(self,ctx):
        if ctx.author.id != secrets.MY_ID:
            await ctx.send("You don't have permission to do this!")
            logger.info({
                f"{ctx.author.name} tried to stop Twitch notifications!"
            })
        else:
            self.trivia.start()
            logger.info({
                f"{ctx.author.name} started trivia"
            })

    @live_notifs_loop.before_loop
    async def before_live_notifs_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(twitchLive(bot))












