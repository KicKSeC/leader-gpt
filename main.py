import discord
import sys, os
from discord.ext import commands

from settings import Settings   # 이 클래스가 가장 먼저 임포트되어야 함
from bot_command import LGPTCommand
from commands.user_settings import UserSettings
from commands.meeting_log import MeetingLog
from commands.role_distribution import RoleDistribution
from commands.schedule import Schedule
from commands.team_rule import TeamRule
from commands.group_review import GroupReview
from commands.assignment import Assignment
from commands.meetingTime import MeetingTime
sys.path.append(os.path.dirname(__file__))
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready(): 
    await bot.add_cog(LGPTCommand(bot))
    await bot.add_cog(UserSettings(bot))
    await bot.add_cog(MeetingLog(bot))
    await bot.add_cog(Schedule(bot))
    await bot.add_cog(RoleDistribution(bot))
    await bot.add_cog(TeamRule(bot))
    await bot.add_cog(GroupReview(bot))
    await bot.add_cog(MeetingTime(bot))
    assignment_cog = Assignment(bot)
    await bot.add_cog(assignment_cog)
    assignment_cog.check_deadlines.start()  # check_deadlines 시작 - 시연이후 삭제될 코드
    print(bot.user.name)        # type: ignore


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed=discord.Embed(description="존재하지 않는 명령어입니다 -> !도움말", color=0xFF0000))


bot.run(Settings.load('DISCORD_TOKEN', is_setting=True))
