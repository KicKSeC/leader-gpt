﻿import os
import random
import discord
import chatgpt

BOT_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('PLOEI_CHANNEL_ID'))
DESCRIPTION = 'leader gpt can help your team!'
GPT_ANSWER_CHECK = '✔'


class LeaderClient(discord.Client):
    async def on_ready(self):
        #
        self.command_keywords = { 'hello': self.say_hello, 'dice': self.roll, '!': self.gpt4_answer,
                                 'token': self.get_token_usage}
        self.channel = self.get_channel(CHANNEL_ID)
        self.is_answering = False

        if self.channel is None:
            raise AttributeError(f"Channel {CHANNEL_ID} is not found")
        
        await self.change_presence(status=discord.Status.online,
                                   activity=discord.Game("성실"))
        print(f'Logged on as {self.user}') 
        await self.channel.send('Commands: ' + ', '.join(self.command_keywords.keys()) +
                                '. 예시: !hello')
        
    async def on_message(self, message):
        if message.author == self.user: # ignore message of itself
            return
    
        if message.content.startswith('!'): # if it's command symbol
            await self.answer(message)            # answer to command

    async def answer(self, message): 
        # check message.content is command
        for keyword in list(self.command_keywords.keys()):
            if message.content.lower().startswith('!'+keyword):
                # if this's command, remove command keyword and
                # get answer of the command 
                await self.command_keywords[keyword](message)   
                return
        # if it's not command, then get response from chatgpt on chatgpt.py 
        if self.is_answering:
            await self.channel.send('이전 답변이 완료될 때까지 기다려주세요')
            return
            
        await message.add_reaction(GPT_ANSWER_CHECK)
        self.is_answering = True
        answer = chatgpt.get_response(message.content)
        await self.channel.send(answer)     # send answer 
        self.is_answering = False
    
    def trim_message_content(self, message) -> str:
        """trim command in message content"""
        content = message.content[1:]   # trim command symbol

        # trim keyword
        for keyword in list(self.command_keywords.keys()):
            if content.lower().startswith(keyword):
                content = content.replace(keyword, '', 1)

        # trim white space
        while content.startswith(' '):
            content = content[1:]

        return content
           
    async def say_hello(self, message):
        """send hello"""
        await self.channel.send(f'Hello! {message.author}')
   
    async def roll(self, message):
        """roll dices and send numbers of dices"""
        try:
            dice = self.trim_message_content(message)
            rolls, limit = map(int, dice.split('d'))
        except ValueError:
            await self.channel.send('NdN 형식이 아니예요! 예시: !dice 2d20')
            return

        await self.channel.send(', '.join(str(random.randint(1, limit)) for r in range(rolls))) 
        
    async def gpt4_answer(self, message):
        content = self.trim_message_content(message)
        if self.is_answering:
            self.channel.send('이전 답변이 완료될 때까지 기다려주세요')
            return
        
        await message.add_reaction(GPT_ANSWER_CHECK)
        answer = chatgpt.get_response(content, model=chatgpt.gpt_model['gpt4'])
        await self.channel.send(answer)
        
    async def get_token_usage(self, message):
        await self.channel.send(f'지금까지 사용된 토큰의 양은 {chatgpt.get_token_usage()}이에요.')


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = LeaderClient(intents=intents, channel=CHANNEL_ID, description=DESCRIPTION)
client.run(BOT_TOKEN)
