import discord
import os
from discord.ext import commands
from bot_command import LGPTCommand

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(bot.user.name)
    await bot.add_cog(LGPTCommand(bot))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("존재하지 않는 명령어입니다.")


bot.run(os.getenv('DISCORD_TOKEN'))
