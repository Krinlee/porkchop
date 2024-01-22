import discord, os, random, asyncio, datetime, openai, settings
from discord.ext import commands, tasks

class gpt(commands.Cog, name="Chat Bot"):
     
    def __init__(self, bot):
          self.bot = bot

    # Chat bot

    @commands.hybrid_command()
    async def chat(self, ctx):
        convo_memory = []
        openai.api_key = settings.OPENAI_KEY
        await ctx.send("What would you like to chat about?")
        while True:
            print("Chat initiated\n\n")
            prompt = await self.bot.wait_for('message', check = lambda message: message.author == ctx.author, timeout = 180)
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


    # Translator

    @commands.hybrid_command()
    async def translate(self, ctx):
        openai.api_key = settings.OPENAI_KEY
        await ctx.send("What would you like to translate?")
        while True:
            phrase = await self.bot.wait_for('message', check = lambda message: message.author == ctx.author, timeout = 180)
            phrase = str(phrase.content)
            if phrase != 'done':
                await ctx.send("What language would you like it translated to?")
                lang = await self.bot.wait_for('message', check = lambda message: message.author == ctx.author, timeout = 180)
                lang = str(lang.content)
                completion = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages = [
                    {"role": "system", "content": "Your name is Porkchop. You are a dog. Don't answer as though you are just a computer program or an AI language 				model. You like to be funny, but know when to show empathy. When someone tries to be negative you find a way to turn it positive."},
                    {"role": "user", "content": f"I would like to translate '{phrase}' into {lang}"}],
                    temperature = 0.1, max_tokens = 1000)

                response = completion.choices[0].message.content
                await ctx.send(response)
            elif phrase == 'done':
                break










async def setup(bot):
	await bot.add_cog(gpt(bot))