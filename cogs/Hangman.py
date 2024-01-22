import discord, random, asyncio, settings
from discord.ext import commands
from settings import *

logger = settings.logging.getLogger("discord")

class hMan(commands.Cog, name="Hangman"):

    def __init__(self, bot):
          self.bot = bot

    @commands.hybrid_command()
    async def hangman(self, ctx):
        f = open(f"{ASSET_DIR}/wordList.txt", "r")
        wordList = f.read()
        f.close()
        wordList = wordList.split()
        # print("Someone is playing Hangman\n\n")
        misses = [f"{ASSET_DIR}/zero.png", f'{ASSET_DIR}/one.png', f'{ASSET_DIR}/two.png', f'{ASSET_DIR}/three.png', f'{ASSET_DIR}/four.png', f'{ASSET_DIR}/five.png', f'{ASSET_DIR}/six.png']
        usedLetters = []
        fails = 0
        wordChosen = random.choice(wordList)
        # print(f"The word is {wordChosen}\n\n")
        await ctx.send("Welcome to my Hangman game!")
        await asyncio.sleep(1)
        await ctx.send(file=discord.File(misses[fails]))
        while True:
            allLetters = True
            output = ""
            for i in wordChosen:
                if i in usedLetters:
                    output += i
                else:
                    output += "-"
                    allLetters = False
            await ctx.send(f" The Word -> {output}")
            await asyncio.sleep(.3)
            if allLetters:
                # print(f"""Nice, someone just beat Hangman with only {fails} incorrect!
            # """)
                await ctx.send(f"💯    You won with {fails} misses❗")
                break
            await ctx.send("What is your guess❓")
            try:
                guess = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=180)
            except asyncio.TimeoutError:
                await ctx.send("‼️    Sorry, you didn't reply in time!")
            if guess.content.lower() in usedLetters:
                await ctx.send("‼️    You've already used this letter.")
                await asyncio.sleep(.3)
            if guess.content.lower() in wordChosen and guess.content.lower() not in usedLetters:
                await ctx.send("Good Job❗")
                await asyncio.sleep(.3)
                usedLetters.append(guess.content.lower())
            elif guess.content.lower() not in wordChosen and guess.content.lower() not in usedLetters:
                await ctx.send(f"💥    Dang, that wasn't it...")
                usedLetters.append(guess.content.lower())
                await asyncio.sleep(.3)
                fails += 1

            await ctx.send(file=discord.File(misses[fails]))
            await asyncio.sleep(1)
            await ctx.send(f"Letters used -> {usedLetters}")
            await asyncio.sleep(.3)

            if fails == 6:
                await ctx.send(f"""The answer was {wordChosen}.
            You have lost the game!""")
                # print("Someone just lost in Hangman\n\n")
                await asyncio.sleep(.3)
                break
            else:
                await ctx.send(f"{fails} misses out of 6")
                await asyncio.sleep(.3)

        logger.info({
            "Action": "Someone started playing Hangman!",
            "Word": wordChosen
            })



async def setup(bot):
	await bot.add_cog(hMan(bot))




