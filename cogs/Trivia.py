import discord, random, asyncio, settings as settings
from discord.ext import commands
from settings import *
from config import secrets

logger = settings.logging.getLogger("trivia")

class trivAnswer(commands.Cog, name = "Trivia"):

        def __init__(self, bot):
            self.bot = bot


        @commands.hybrid_command()
        async def cheat(self, ctx):
            if ctx.author.id == secrets.MY_ID:
                f = open(f'{TRIV_DIR}/answer.txt', 'r')
                trivia_ans = f.read()
                f.close()
                await ctx.send(trivia_ans)
            else:
                await ctx.send("You can't have the answer yet!")
            
            logger.info({
                 "User": ctx.author.id,
                 
            })
        
        
async def setup(bot):
    await bot.add_cog(trivAnswer(bot))







