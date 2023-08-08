
import discord, os, random, asyncio, datetime, logging, openai, re
from discord.ext import commands, tasks
from Trivia_List import *
from dotenv import load_dotenv

logging.basicConfig(level = logging.ERROR, filename = "error-file.log", filemode = "w", format = "%(asctime)s - %(levelname)s - %(message)s")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='-', intents = intents)



# Rock Paper Scissor parts

options = ['rock', 'paper', 'scissors']
rockS = ['✊', '✊🏿', '✊🏾', '✊🏽', '✊🏼', '✊🏻']
paperS = ['✋', '✋🏿', '✋🏾', '✋🏽', '✋🏼', '✋🏻']
scissorsS = ['✌️', '✌️', '✌️', '✌️', '✌️', '✌️']
f = open("wordList.txt", "r")
wordList = f.read()
f.close()

wordList = wordList.split()


# .env parts

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
tchan = os.getenv('TEST_CHANNEL')
tchan = int(tchan)
bchan = os.getenv('BOT_CHANNEL')
bchan = int(bchan)
krinlee = osgetenv('MY_USER_ID')



# This chooses which channel to target (for trivia)

target_channel_id = bchan



# Time settings

utc = datetime.timezone.utc
time = datetime.time(hour=12, minute=5)



# Test command

@bot.command()
async def test(ctx):
    await ctx.send("This is a test!")



# Getting the Bot ready

@bot.event
async def on_ready():
    print('\n{0.user} is ready for action'.format(bot))
    trivia.start()


# member join event

async def intro_dm(member):
    print(f"Sending a DM to {member.name} to welcome them to the channel!")
    
    await member.send(f"""🎉 Hi {member.name} !  🎉
    
    ε(´｡•᎑•`)っ 💕        Welcome to the server Krinlee's Roost!      ε(´｡•᎑•`)っ 💕
    
    Do you like to code?    🇵 🇾 🐍   -   🇯 🇸 ♨️  -   🇨  #⃣
    Do you like to game?    🎮   🕹️  👾
    Are you a content creator looking for a place to hang out?  💡   🎥   🎬
    
    We do that here. For now there isn't much, but there's always room to grow!
    
    Please be respectful to everyone, and have fun!     🎉
    
    If you are interested in using the Bot type "-help"! """)


@bot.command()
async def help(ctx):
	await ctx.send("""Hey there! It looks like you're interested in learning what all I can do
		with and for you. I would love to... help. As I'm sure you've figured out (because you
		got this far) you use the "-" to initiate the commands. The different commands and
		a short description are:

		help  -  That brings you here!
		
		chat  -  This starts a chat session with me! We can chill and have a conversation until
				 I eaither time out (180 seconds) or you type "done"
		
		translate  -  You can use this to translate virtually anything into a language of your choice.
		         Options may be limited due to limitations of ChatGPT.
		
		hangman  -  This starts you a game of Hangman.
		
		rock/paper/scissors  -  Using either one of these initiates a round of rock paper scissors.
		         I will immidiately respond with my attack.

	 """)


# chatgpt command

@bot.command()
async def chat(ctx):
	convo_memory = []
	openai.api_key = os.getenv('OPENAI_API_KEY')
	await ctx.send("What would you like to chat about?")
	while True:
		print("Chat initiated\n\n")
		prompt = await bot.wait_for('message', check = lambda message: message.author == ctx.author, timeout = 180)
		prompt = str(prompt.content)
		if prompt != 'done':
			print("Prompt received\n\n")
			
			completion = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages = [
			{"role": "system", "content": f"Your name is Porkchop. You are a dog. Your current conversation is in {convo_memory} You will not say that you are a computer program or an AI language model. You like to be funny, but know when to show empathy. When someone tries to be negative you find a way to turn it positive."},
			{"role": "user", "content": prompt}],
			temperature = 0.1, max_tokens = 1000)
			
			response = completion.choices[0].message.content
			convo_memory.append({"role": "user", "content": prompt})
			convo_memory.append({"role": "user", "content": response})
			await ctx.send(response)
			print("Reply sent\n\n")
		elif prompt == 'done':
			print("Session ended")
			return
		


# ChatGPT translator

@bot.command()
async def translate(ctx):
	openai.api_key = os.getenv('OPENAI_API_KEY')
	await ctx.send("What would you like to translate?")
	while True:
		phrase = await bot.wait_for('message', check = lambda message: message.author == ctx.author, timeout = 180)
		phrase = str(phrase.content)
		if phrase != 'done':
			await ctx.send("What language would you like it translated to?")
			lang = await bot.wait_for('message', check = lambda message: message.author == ctx.author, timeout = 180)
			lang = str(lang.content)
			completion = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages = [
				{"role": "system", "content": "Your name is Porkchop. You are a dog. Don't answer as though you are just a computer program or an AI language 				model. You like to be funny, but know when to show empathy. When someone tries to be negative you find a way to turn it positive."},
				{"role": "user", "content": f"I would like to translate '{phrase}' into {lang}"}],
				temperature = 0.1, max_tokens = 1000)

			response = completion.choices[0].message.content
			await ctx.send(response)
		elif phrase == 'done':
			break



# Hangman command

@bot.command()
async def hangman(ctx):
    print("Someone is playing Hangman\n\n")
    misses = ['zero.png', 'one.png', 'two.png', 'three.png', 'four.png', 'five.png', 'six.png']
    usedLetters = []
    fails = 0
    wordChosen = random.choice(wordList)
    print(f"The word is {wordChosen}\n\n")
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
            print(f"""Nice, someone just beat Hangman with only {fails} incorrect!
        """)
            await ctx.send(f"💯    You won with {fails} misses❗")
            break
        await ctx.send("What is your guess❓")
        try:
            guess = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=180)
        except asyncio.TimeoutError:
            logging.error("Someone timed out in Hangman!")
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
            print("Someone just lost in Hangman\n\n")
            await asyncio.sleep(.3)
            break
        else:
            await ctx.send(f"{fails} misses out of 6")
            await asyncio.sleep(.3)



# Rock Paper Scissors commands

@bot.command()
async def rock(ctx):
    while True:
        rockR = random.choice(rockS)
        paperR = random.choice(paperS)
        scissorsR = random.choice(scissorsS)
        botMove = random.choice(options)
        await ctx.send(botMove)
        if botMove == 'rock':
            await ctx.send(f"""I choose {rockR}
	    It's a tie    👔""")
            print("There was a tie\n\n")
            await asyncio.sleep(1)
        elif botMove == 'paper':
            await ctx.send(f"""I choose {paperR}
	    {paperR} beats   {rockR}
        Bot wins      ⚰️""")
            print("Bot wins\n\n")
            await asyncio.sleep(1)
        elif botMove == 'scissors':
            await ctx.send(f"""I choose {scissorsR}
	    {rockR}  beats   {scissorsR}
        You win   🎉""")
            print("Beat the bot\n\n")
        break


@bot.command()
async def paper(ctx):
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
            print("Beat the bot\n\n")
            await asyncio.sleep(1)
        elif botMove == 'paper':
            await ctx.send(f"""I choose {paperP}
	    It's a tie    👔""")
            print("There was a tie\n\n")
            await asyncio.sleep(1)
        elif botMove == 'scissors':
            await ctx.send(f"""I choose {scissorsP}
	    {scissorsP}    beats {paperP}
        Bot wins      ⚰️""")
            print("Bot wins\n\n")
        break


@bot.command()
async def scissors(ctx):
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
            print("Bot wins\n\n")
            await asyncio.sleep(1)
        elif botMove == 'paper':
            await ctx.send(f"""I choose {paperX}
	    {scissorsX}    beats {paperX}
        You win       🎉""")
            print("Beat the bot\n\n")
            await asyncio.sleep(1)
        elif botMove == 'scissors':
            await ctx.send(f"""I choose {scissorsX}
	    It's a tie    👔""")
            print("There was a tie\n\n")
        break



# Trivia loop

@tasks.loop(time=time)
async def trivia():
    message_channel = bot.get_channel(target_channel_id)
    try:
        f = open('question.txt', 'r')
        o_question = f.read()
        f.close()
        f = open('answer.txt', 'r')
        o_answer = f.read()
        f.close()
        await message_channel.send(f"""@here Yesterday's question was:
        
         ¯\_(ツ)_/¯  {o_question}  ¯\_(ツ)_/¯""")
        await message_channel.send(f"""The answer is		(っ ͡ ͡º - ͡ ͡º ς)		 -> {o_answer} <-
	
	(人❛ᴗ❛)♪тнайк　чоц♪(❛ᴗ❛*人)""")
        await asyncio.sleep(10)
        pick = trivia_List[random.randint(0, 400)]
        question = pick[0]
        answer = pick[1]
        f = open('question.txt', 'w')
        f.write(f"{question}")
        f.close()
        f = open('answer.txt', 'w')
        f.write(f"{answer}")
        f.close
    except:
        pick = trivia_List[random.randint(0, 400)]
        question = pick[0]
        answer = pick[1]
        f = open('question.txt', 'w')
        f.write(f"{question}")
        f.close()
        f = open('answer.txt', 'w')
        f.write(f"{answer}")
        f.close
    print(f"Trivia question --> {question} <-- posted to {message_channel}  --  The answer is -> {answer}")
    await message_channel.send("""@everyone 
    
    As always, post your answers to the trivia in the trivia-answers channel.

    (っ'ヮ'c)	The answer will be posted here on the next day before the next trivia question.""")
    await asyncio.sleep(3)
    await message_channel.send(f"""🧠	🧠	-> {question} <-	🧠	🧠
    
    (∩｀-´)⊃━☆ﾟ.*･｡ﾟ""")


@trivia.before_loop
async def before_trivia():
    print("Trivia is good to go!\n")
    await bot.wait_until_ready()


@bot.event
async def on_member_join(member):
    await intro_dm(member)


# Runs the Bot

try:
    bot.run(TOKEN)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
    else:
        raise e
