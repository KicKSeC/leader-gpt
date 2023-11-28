import discord
import sys, os
from data import KeyData
from discord.ext import commands

from bot_command import LGPTCommand
from commands.meeting_log import MeetingLog
from commands.role_distribution import RoleDistribution
from commands.schedule import Schedule
from commands.team_rule import TeamRule
from commands.group_review import GroupReview
from commands.assignment import Assignment

sys.path.append(os.path.dirname(__file__))
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(bot.user.name)
    await bot.add_cog(LGPTCommand(bot))
    await bot.add_cog(MeetingLog(bot))
    await bot.add_cog(Schedule(bot))
    await bot.add_cog(RoleDistribution(bot))
    await bot.add_cog(TeamRule(bot))
    await bot.add_cog(GroupReview(bot))
    await bot.add_cog(Assignment(bot))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("존재하지 않는 명령어입니다.")


bot.run(KeyData.DISCORD_TOKEN)
