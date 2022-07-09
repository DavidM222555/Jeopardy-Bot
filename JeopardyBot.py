import disnake 
from disnake.ext import commands 

from dotenv import load_dotenv
import os
import asyncio

from dotenv import load_dotenv 
from JeopardyFuncs import JeopardyWrapper

import nltk

load_dotenv('.env')

class JeopardyBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        intents = disnake.Intents.default() 
        intents.members = True 
        intents.message_content = True 

        self.jWrapper = JeopardyWrapper()
        self.current_category = None
        self.current_question = None 
        self.current_answer = None 
        self.current_value = None

        self.question_valid = False
        self.question_currently_being_asked = False 
        self.question_answered_correctly = False

        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents, *args, **kwargs)

        self.add_commands()
        self.run(os.getenv('discord-token'))

    
    async def on_ready(self):
        print("We have logged in as {}".format(self.user))

    
    def add_commands(self):

        @self.command(name='question', pass_context=True)
        async def question(ctx):

            if(self.question_currently_being_asked == True):
                await ctx.send("There is already a question in play")
                return

            random_entry = self.jWrapper.get_random_entry()

            self.current_category = random_entry[0]
            self.current_question = random_entry[1]
            self.current_answer = random_entry[2]
            self.current_value = random_entry[3]

            self.question_valid = True
            self.question_currently_being_asked = True
            self.question_answered_correctly = False

            sent_message = await ctx.send(self.current_question)

            print(self.current_answer)
            print(self.current_value)
            print(sent_message.id)

            await asyncio.sleep(15)

            self.question_valid = False
            self.question_currently_being_asked = False

            if(self.question_answered_correctly == True):
                return

            await ctx.send("Question no longer valid")


        @self.command(name='answer', pass_context=True)
        async def answer(ctx, answer_arg):
            if(self.question_valid != True):
                await ctx.send("Question not currently valid")
                print("Answer not completed ")
            else:
                print("Answer will be considered")

                edit_distance = nltk.edit_distance(self.current_answer, answer_arg)

                if(edit_distance < 10):
                    await ctx.send("Correct answer!")
                    self.question_answered_correctly = True
                    return

                
            

