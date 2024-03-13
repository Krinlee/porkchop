import settings
from discord.ext import commands
from assets.account import Account

logger = settings.logging.getLogger('discord')

class PlayerPoints(commands.Cog, name = 'Player'):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command()
    async def points(self, ctx):
        account = Account.fetch(ctx.message)
        await ctx.send(f"You ahve {account.amount} points")

async def setup(bot):
    await bot.add_cog(PlayerPoints(bot))