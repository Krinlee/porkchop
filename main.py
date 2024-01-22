import discord, settings, random, asyncio
from discord.ext import commands
from discord import app_commands
from settings import *
# from twitchAPI.twitch import Twitch
from cogs.RockPaperScissors import rPs
from cogs.Trivia import trivAnswer
from cogs.Hangman import hMan
from cogs.cgpt import gpt

logger = settings.logging.getLogger("bot")

target_channel_id = settings.tchan

# ************************************** TESTING AREA BEGINS ************************************



# ************************************** TESTING USE AREA ENDS **********************************


def run():
	intents = discord.Intents.all()

	bot = commands.Bot(command_prefix="-", intents=intents)

	@bot.event
	async def on_ready():

		for cog_file in settings.COGS_DIR.glob("*.py"):
			if cog_file != "__init__.py":
				await bot.load_extension(f"cogs.{cog_file.name[:-3]}")

		bot.tree.copy_global_to(guild=settings.GUILD)
		await bot.tree.sync(guild=settings.GUILD)
	
	
		
	
	logger.info({
		"User": f"{settings.streamerName} - {settings.DISCORD_ID}",
		"Bot": "Porkchop"
		})

	bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
	run()