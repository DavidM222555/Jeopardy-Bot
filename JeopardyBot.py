import disnake 
from disnake.ext import commands 

import os
import asyncio
from dotenv import load_dotenv

from JeopardyFuncs import JeopardyWrapper
from SQLWrapper import SqlLiteWrapper

import nltk


load_dotenv('.env')

class JeopardyBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        intents = disnake.Intents.default() 
        intents.members = True 
        intents.message_content = True 

        self.jWrapper = JeopardyWrapper()
        self.sqlWrapper = SqlLiteWrapper()

        self.current_category = None
        self.current_question = None 
        self.current_answer = None 
        self.current_value = None

        self.question_valid = False
        self.question_currently_being_asked = False 
        self.question_answered_correctly = False

        self.users_that_have_answered = []

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

            self.users_that_have_answered = []

            await ctx.send(self.current_question)

            print(self.current_answer)
            print(self.current_value)

            await asyncio.sleep(15)

            self.question_valid = False
            self.question_currently_being_asked = False

            if(self.question_answered_correctly == True):
                return

            await ctx.send("Question no longer valid")


        @self.command(name='answer', pass_context=True)
        async def answer(ctx, answer_arg):
            message_sender = str(ctx.message.author)
            message_sender_id = ctx.message.author.id

            if(self.question_valid != True):
                await ctx.send("Question not currently valid")
            elif(message_sender in self.users_that_have_answered):
                await ctx.send("You have already tried to answer this question")
            else:
                self.current_answer = self.current_answer.lower()
                answer_arg = answer_arg.lower()

                edit_distance = nltk.edit_distance(self.current_answer, answer_arg)

                # If question was answered correctly (or close enough to correctly)
                if(edit_distance < 3):
                    response_str = "Correct answer <@" + str(message_sender_id) + ">"

                    await ctx.send(response_str)
                    self.question_answered_correctly = True

                    self.sqlWrapper.increment_questions_correct(message_sender)
                    self.sqlWrapper.increment_game_score(message_sender, self.jWrapper.convert_value_to_int(self.current_value))

                    return
                else:
                    response_str = "Incorrect answer <@" + str(message_sender_id) + ">"
                    self.users_that_have_answered.append(message_sender)

                    # Decrement game scores
                    self.sqlWrapper.increment_questions_incorrect(message_sender)
                    self.sqlWrapper.increment_game_score(message_sender, -1 * self.jWrapper.convert_value_to_int(self.current_value))

                    await ctx.send(response_str)

