import os, logging, pathlib, discord
from logging.config import dictConfig
from dotenv import load_dotenv


BASE_DIR = pathlib.Path(__file__).parent

CMDS_DIR = BASE_DIR / "cmds"
COGS_DIR = BASE_DIR / "cogs"
TRIV_DIR = BASE_DIR / "trivia"
ASSET_DIR = BASE_DIR / "assets"


load_dotenv()

DISCORD_API_SECRET = os.getenv("DISCORD_TOKEN")
GUILD = discord.Object(id=int(os.getenv("GUILD_ID")))
lchan = os.getenv('GOING_LIVE')
bchan = os.getenv('BOT_CHANNEL')
tchan = os.getenv('TEST_CHANNEL')
tzone = os.getenv('TIME_ZONE')
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
DISCORD_ID = os.getenv('MY_USER_ID')
MY_ID = int(DISCORD_ID)
streamerName = os.getenv('STREAMER')
twitch_client_id = os.getenv('CLIENT_ID')
twitch_client_secret = os.getenv('CLIENT_SECRET')




LOGGING_CONFIG = {
	"version": 1,
	"disabled_existing_loggers": False,
	"formatters":{
		"verbose":{
			"format": "%(levelname)-5s - %(asctime)s - %(module)-5s : %(message)s"
		},
		"standard":{
			"format": "%(levelname)-10s - %(name)-10s : %(message)s"
		}
	},
	"handlers":{
		"console":{
			'level': "DEBUG",
			'class': "logging.StreamHandler",
			'formatter': "standard",
            'stream': "ext://sys.stdout"
		},
		"console2":{
			'level': "WARNING",
			'class': "logging.StreamHandler",
			'formatter': "standard",
            'stream': "ext://sys.stdout"
		},
		"file":{
			'level': "INFO",
			'class': "logging.FileHandler",
			'filename': f"{BASE_DIR}/logs/infos.log",
			'mode': "w",
			'formatter': "verbose"
		},
        "twitch_log":{
			'level': "INFO",
			'class': "logging.FileHandler",
			'filename': f"{BASE_DIR}/logs/twitch.log",
			'mode': "w",
			'formatter': "verbose"
		},
        "trivia_log":{
			'level': "INFO",
			'class': "logging.FileHandler",
			'filename': f"{BASE_DIR}/logs/trivia.log",
			'mode': "w",
			'formatter': "verbose"
		},
	},
	"loggers":{
		"bot": {
			'handlers': ["console"],
			"level": "DEBUG",
			"propagate": False
		},
		"discord": {
			'handlers': ["console", "file"],
			"level": "INFO",
			"propagate": False
		},
        "twitch": {
            'handlers': ['twitch_log'],
            'level': 'INFO',
            'propagate': False
		},
        "trivia": {
            'handlers': ['trivia_log'],
            'level': 'INFO',
            'propagate': False
		}
	}

}


dictConfig(LOGGING_CONFIG)

