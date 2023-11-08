import os
import discord
from discord.ext import commands
import discord_bot
import unittest

bot_token = os.getenv('DISCORD_TOKEN')
channel_id = int(os.getenv('PLOEI_CHANNEL_ID'))

class DiscordBotTest(unittest.TestCase):
    def test_channel_ID(self):
        intents = discord.Intents.default()
        bot = commands.Bot(command_prefix='!', intents=intents)
     
        @bot.event
        async def on_ready():
            print(f'We have logged in as {bot.user}')
            channel = bot.get_channel(channel_id)
            self.assertTrue(channel)
  
        bot.run(bot_token) 
    
if __name__ == '__main__':
    unittest.main()
