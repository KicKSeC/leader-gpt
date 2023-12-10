import discord
import sys, os
from discord.ext import commands

from settings import Settings  # 이 클래스가 가장 먼저 임포트되어야 함
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
intents.guilds = True
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
    print(bot.user.name)  # type: ignore


@bot.event
async def on_guild_join(guild):
    """서버에 입장했을 때 실행될 코드"""
    for guild in bot.guilds:
        default_channel = guild.system_channel  # 디스코드 봇이 들어온 서버의 기본 채널을 가져옵니다.
        if default_channel is not None:
            embed = discord.Embed(
                title="안녕하세요! Leader.GPT입니다!",
                description="여러분들의 팀장이 될 Leader.GPT라고 합니다\n\n"
                            "헌신적인 팀장이 될 수 있도록 노력할게요!\n\n"
                            "!도움말을 입력해 명령어를 확인할 수 있어요!\n\n"
                            "시작하기에 앞서 기본설정을 위해 '!설정 채널'을 입력해주시겠어요?",
                color=0x3489db
            )
            await default_channel.send(embed=embed)
            break


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed=discord.Embed(description="존재하지 않는 명령어입니다 -> !도움말", color=0xFF0000))


bot.run(Settings.load('DISCORD_TOKEN', is_setting=True))
