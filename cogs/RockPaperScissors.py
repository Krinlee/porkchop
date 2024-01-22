import discord, random, asyncio, settings
from discord.ext import commands
from settings import *

logger = settings.logging.getLogger("discord")

# Rock Paper Scissor parts
options = ['rock', 'paper', 'scissors']
rockS = ['✊', '✊🏿', '✊🏾', '✊🏽', '✊🏼', '✊🏻']
paperS = ['✋', '✋🏿', '✋🏾', '✋🏽', '✋🏼', '✋🏻']
scissorsS = ['✌️', '✌️', '✌️', '✌️', '✌️', '✌️']


class rPs(commands.Cog, name="RPS"):
     
    def __init__(self, bot):
          self.bot = bot

    @commands.hybrid_command()
    async def rock(self, ctx):
        
        while True:
            rockR = random.choice(rockS)
            paperR = random.choice(paperS)
            scissorsR = random.choice(scissorsS)
            botMove = random.choice(options)
            await ctx.send(botMove)
            if botMove == 'rock':
                await ctx.send(f"""I choose {rockR}
            It's a tie    👔""")
                result = "Tie!"
                # print("There was a tie\n\n")
                await asyncio.sleep(1)
            elif botMove == 'paper':
                await ctx.send(f"""I choose {paperR}
            {paperR} beats   {rockR}
            Bot wins      ⚰️""")
                result = "Bot wins!"
                # print("Bot wins\n\n")
                await asyncio.sleep(1)
            elif botMove == 'scissors':
                await ctx.send(f"""I choose {scissorsR}
            {rockR}  beats   {scissorsR}
            You win   🎉""")
                result = "Player wins!"
                # print("Beat the bot\n\n")
            logger.info({
		"Player": "Rock!",
		"Bot": botMove,
        "Result": result
		})
            break
    
    @commands.hybrid_command()
    async def paper(self, ctx):
        while True:
            rockP = random.choice(rockS)
            paperP = random.choice(paperS)
            scissorsP = random.choice(scissorsS)
            botMove = random.choice(options)
            await ctx.send(botMove)
            if botMove == 'rock':
                await ctx.send(f"""I choose {rockP}
            {paperP} beats   {rockP}
            You win   🎉""")
                result = "Player wins!"
                # print("Beat the bot\n\n")
                await asyncio.sleep(1)
            elif botMove == 'paper':
                await ctx.send(f"""I choose {paperP}
            It's a tie    👔""")
                result = "Tie!"
                # print("There was a tie\n\n")
                await asyncio.sleep(1)
            elif botMove == 'scissors':
                await ctx.send(f"""I choose {scissorsP}
            {scissorsP}    beats {paperP}
            Bot wins      ⚰️""")
                result = "Bot wins!"
                # print("Bot wins\n\n")
            logger.info({
		"Player": "Paper!",
		"Bot": botMove,
        "Result": result
		})
            break
    
    @commands.hybrid_command()
    async def scissors(self, ctx):
        while True:
            rockX = random.choice(rockS)
            paperX = random.choice(paperS)
            scissorsX = random.choice(scissorsS)
            botMove = random.choice(options)
            await ctx.send(botMove)
            if botMove == 'rock':
                await ctx.send(f"""I choose {rockX}
            {rockX}  beats   {scissorsX}
            Bot wins      ⚰️""")
                result = "Bot wins!"
                # print("Bot wins\n\n")
                await asyncio.sleep(1)
            elif botMove == 'paper':
                await ctx.send(f"""I choose {paperX}
            {scissorsX}    beats {paperX}
            You win       🎉""")
                result = "Player wins!"
                # print("Beat the bot\n\n")
                await asyncio.sleep(1)
            elif botMove == 'scissors':
                await ctx.send(f"""I choose {scissorsX}
            It's a tie    👔""")
                result = "Tie!"
                # print("There was a tie\n\n")
            logger.info({
		"Player": "Scissors!",
		"Bot": botMove,
        "Result": result
		})
            break



async def setup(bot):
	await bot.add_cog(rPs(bot))





