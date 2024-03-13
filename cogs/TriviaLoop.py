import discord, os, random, asyncio, json, datetime, random, settings as settings
from discord.ext import commands, tasks
from settings import *
from config import secrets
from urllib.request import urlopen
from assets.account import Account

logger = settings.logging.getLogger('trivia')

target_channel_id = secrets.bchan
utc = datetime.timezone.utc
time = datetime.time(hour=12, minute=5)

def give_points(ctx):
    account = Account.fetch(ctx.message)
    account.amount += 10
    account.save()

def get_trivia():
    global choices, question, answer, participants
    participants = []
    url = 'https://opentdb.com/api.php?amount=1&type=multiple'
    trivia_url = urlopen(url)
    trivia = json.loads(trivia_url.read())
    question = trivia["results"][0]["question"].replace('&quot;', '"').replace("&#039;", "'")
    answer = trivia["results"][0]["correct_answer"].replace('&quot;', '"').replace("&#039;", "'")
    wrong_one = trivia["results"][0]["incorrect_answers"][0].replace('&quot;', '"').replace("&#039;", "'")
    wrong_two = trivia["results"][0]["incorrect_answers"][1].replace('&quot;', '"').replace("&#039;", "'")
    wrong_three = trivia["results"][0]["incorrect_answers"][2].replace('&quot;', '"').replace("&#039;", "'")
    answers = [answer, wrong_one, wrong_two, wrong_three]
    random.shuffle(answers)
    choices = answers
    f = open(f'{TRIV_DIR}/question.txt', 'w')
    f.write(f"{question}")
    f.close()
    f = open(f'{TRIV_DIR}/answer.txt', 'w')
    f.write(f"{answer}")
    f.close()


# Trivia loop
class tRivia(commands.Cog, name = 'Trivia'):

    def __init__(self, bot):
        self.bot = bot
        self.trivia.start()

    def cog_unload(self) -> None:
        self.trivia.stop()
        

    @tasks.loop(time=time)
    async def trivia(self):
        message_channel = self.bot.get_channel(int(target_channel_id))
        f = open(f'{TRIV_DIR}/question.txt', 'r')
        o_question = f.read()
        f.close()
        f = open(f'{TRIV_DIR}/answer.txt', 'r')
        o_answer = f.read()
        f.close()
        await message_channel.send(f"""@everyone
                                   
                                   Yesterday's question was:
            
        ¯\_(ツ)_/¯  {o_question}  ¯\_(ツ)_/¯

                                       ---------------------------------------------------------

        The answer is		(っ ͡ ͡º - ͡ ͡º ς)		 -> {o_answer} <-
        
                                       
                                                    (人❛ᴗ❛)♪тнайк　чоц♪(❛ᴗ❛*人)
                                       
                                       ---------------------------------------------------------""")
        await asyncio.sleep(1)
        get_trivia()
        await message_channel.send(f""" 
        
        As always, post your answers to the trivia in the trivia-answers channel.

        (っ'ヮ'c)	The answer will be posted here on the next day before the next trivia question.
                                   
                                   ---------------------------------------------------------
        
                                   
        (∩｀-´)⊃━☆ﾟ.*･｡ﾟ                 🧠	🧠	-> {question} <-	🧠	🧠
                                   
                                   Use the /answer command to get your answer choices.
        
                                    ---------------------------------------------------------""")
    @commands.hybrid_command()
    async def answer(self, ctx):
        global participant
        participant = ctx.author.id

        if participant in participants:
            await ctx.send("You already answered today!")
            return
        else:
            class SimpleView(discord.ui.View):
                participants = []
                
                foo : bool = None

                async def disable_all_items(self):
                    for item in self.children:
                        item.disabled = True
                    await self.message.edit(view=self)

                async def on_timeout(self) -> None:
                    await self.disable_all_items()

                @discord.ui.button(label=choices[0], style=discord.ButtonStyle.primary)
                async def button_one(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if choices[0] == answer:
                        await interaction.response.send_message("You got it!")
                        participants.append(participant)
                        give_points(ctx)
                    else:
                        await interaction.response.send_message("That wasn't it homie")
                    await view.disable_all_items()
                    trivia_player_logger()

                @discord.ui.button(label=choices[1], style=discord.ButtonStyle.primary)
                async def button_two(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if choices[1] == answer:
                        await interaction.response.send_message("You got it!")
                        participants.append(participant)
                        give_points(ctx)
                    else:
                        await interaction.response.send_message("That wasn't it homie")
                    await view.disable_all_items()
                    trivia_player_logger()

                @discord.ui.button(label=choices[2], style=discord.ButtonStyle.primary)
                async def button_three(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if choices[2] == answer:
                        await interaction.response.send_message("You got it!")
                        participants.append(participant)
                        give_points(ctx)
                    else:
                        await interaction.response.send_message("That wasn't it homie")
                    await view.disable_all_items()
                    trivia_player_logger()

                @discord.ui.button(label=choices[3], style=discord.ButtonStyle.primary)
                async def button_four(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if choices[3] == answer:
                        await interaction.response.send_message("You got it!")
                        participants.append(participant)
                        give_points(ctx)
                    else:
                        await interaction.response.send_message("That wasn't it homie")
                    await view.disable_all_items()
                    trivia_player_logger()
        def trivia_player_logger():
            if participant in participants:
                logger.info({
                    "User": f"{ctx.author.name} got it right!"
                    })
            else:
                logger.info({
                    "User": f"{ctx.author.name} get to try again."
                })

        view = SimpleView(timeout=30)
        message = await ctx.send(view=view)
        view.message = message
        await view.wait()

    @trivia.before_loop
    async def before_trivia(self):
        await self.bot.wait_until_ready()

    
async def setup(bot):
    await bot.add_cog(tRivia(bot))








    

