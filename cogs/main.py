import discord
from discord.ext import commands, tasks
import random
import pymongo
from pymongo import MongoClient
from copy import copy

class Main(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient(enterclientlink)
        self.db_quiz = self.cluster["discord"]
        self.collection_quiz = self.db_quiz["quiz_data"]
        self.collection_userdata = self.db_quiz["userdata"]
        self.correct_answ = "thisoneisnotcorrect"

    #  Events

    @commands.Cog.listener() #  Creating an event within a cog
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.do_not_disturb,
                                          activity=discord.Game('Hating women and minorities'))
        print('Bot is online')

    @commands.Cog.listener()  # Creating an event within a cog
    async def on_message(self, message):
        bruh_list = ["bruh", "Bruh", "BRUH", "Bro", "Brother", "Browski", "b r u h",
                     "B R U H", "BRO", "B r u h", "BRuH", "BrUh", "BRUh", "bRUH", "BruH", "BRuh",
                     "B r U h", "B r U H", "B R u h", "b R U H", "b r U H", "b r u H", "b R uH", "BRuh",
                     "BR UH", "br uh", "B ruh", "Bru h", "Br UH", "br UH", "BR uh", "BR Uh", "bru H", "bR uH",
                     ]
        for m in bruh_list:
            if message.content == m:
                if message.author.id != 684514752239501345:
                    channel = message.channel
                    await channel.send(message.content)

    @commands.Cog.listener()  # Creating an event within a cog
    async def on_message(self, message):
        if message.content == self.correct_answ:
            user_id = message.author.id
            username = message.author.name
            usr_data = self.collection_userdata.find_one({"_id":user_id})
            if usr_data is None:
                userdata_dict = {"_id": user_id, "username":username, "points": 1}
                self.collection_userdata.insert_one(userdata_dict)
            else:
                result_data = self.collection_userdata.find_one({"_id":user_id})
                replacement_dict = copy(result_data)
                replacement_dict["points"] = result_data["points"] + 1
                self.collection_userdata.replace_one(filter={"_id":user_id},
                                                     replacement=replacement_dict)

            await message.channel.send("True")


            self.correct_answ = "thisoneisnotcorrect"


    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     await ctx.send('Hata')


    #  Commands

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong!, {round(self.client.latency*1000)} ms')

    @commands.command()
    async def d_roll(self, ctx, input_int):
        random_num = random.randint(0, int(input_int))
        if random_num == 69:
            await ctx.send(f'{random_num}, Nice')
        else:
            await ctx.send(random_num)

    @commands.command()
    async def kahin(self, ctx, *, question):
        responses = ['Kesinlikle',
                     'Kesinlikle öyle',
                     'Kuşkusuz',
                     'Evet - elbette',
                     'Güvenebilirsin',
                     'Gördüğüm kadarıyla, evet',
                     'Çoğunlukla',
                     'Dışarıdan iyi görünüor',
                     'Evet',
                     'Belirtiler olduğu yönünde',
                     'Biraz belirsiz, tekrar dene',
                     'Daha sonra tekrar dene',
                     'Şimdi söylemesem daha iyi',
                     'Şimdi kehanette bulunamam',
                     'Konsantre ol ve tekrar sor',
                     'Kesinlikle hayır',
                     'Yanıtım hayır',
                     'Kaynaklarım hayır diyor',
                     'Pek iyi görünmüyor',
                     'Çok şüpheli']

        await ctx.send(f' Soru: {question} \n  Yanıt: {random.choice(responses)}')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount+1)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def quiz_add(self, ctx, id, boss, url, ans1, ans2, ans3, ans4, ans_correct, *,question):
        post_quiz ={"_id": int(id),"boss":boss, "url":url, "a":ans1, "b":ans2, "c":ans3, "d":ans4, "correct_ans":ans_correct,
                    "question": question}
        self.collection_quiz.insert_one(post_quiz)
        await ctx.send("Added")


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def quiz_inspect(self, ctx):
        inspection = self.collection_quiz.find({})
        for results in inspection:
           await ctx.send(results)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def quiz_remove(self, ctx, id):
        self.collection_quiz.delete_one({"_id":int(id)})
        await ctx.send("Removed")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def quiz_ask(self,ctx, id):
        quiz = self.collection_quiz.find({"_id":int(id)})
        for quiz in quiz:

            embed = discord.Embed(title="NERD QUIZ TIME", description=quiz["question"]+
                                                                      f"\n a) {quiz['a']}" +
                                                                      f"\n b) {quiz['b']} " +
                                                                      f"\n c) {quiz['c']} " +
                                                                      f"\n d) {quiz['d']} ",
                                  colour=discord.Color.red(), url='https://www.google.com.tr/')
            embed.set_author(name="Boss of the day: "+  quiz["boss"])
            embed.set_image(url=quiz["url"])

            self.correct_answ = quiz["correct_ans"]

            await ctx.send(embed=embed)






def setup(client):
    client.add_cog(Main(client))