import os
import random
import discord
import chatgpt

BOT_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('PLOEI_CHANNEL_ID'))
DESCRIPTION = 'leader gpt can help your team!'


class LeaderClient(discord.Client):
    def __init__(self, *, intents, channel, **options):
        super().__init__(intents=intents, options=options)
        self.command_keywords = { 'hello': self.say_hello, 'dice': self.roll }
        self.channel = self.get_channel(channel)

        if self.channel is None:
            raise AttributeError(f"Channel {channel} is not found")
            
    
    async def on_ready(self):
        print(f'Logged on as {self.user}')
        await self.change_presence(status=discord.Status.online,
                                   activity=discord.Game("성실"))
        await self.channel.send('Hello World!')
        
    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('!'):
            await self.answer(message)

    async def answer(self, message):
        is_answered = False
        answer = ""
        # check message.content is command
        for keyword in list(self.command_keywords.keys):
            if message.content.lower().startswith('!'+keyword):
                # if this's command, remove command keyword and
                # get answer of the command
                answer = await self.command_keywords[keyword](
                    message.content.replace('!'+keyword+' ', '', 1))
                is_answered = True
                break
       
        if not is_answered:
            answer = chatgpt.get_response(message.content)
            await self.channel.send(answer)
           
    def say_hello(self, message):
        return f'Hello! {message.author}'
   
    async def roll(self, dice: str):
        """Rolls a dice in NdN format

        Args:
            dice (str): NdN format
        """
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.channel.send('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))

        return result


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = LeaderClient(intents=intents, channel=CHANNEL_ID, description=DESCRIPTION)
client.run(BOT_TOKEN)
