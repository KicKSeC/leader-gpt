import discord
from discord import NotFound
from discord.ext import commands
from settings import Settings


class UserSettings(commands.Cog):
    """사용자가 설정을 입력하도록 돕는 명령어 클래스"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="설정")
    async def settings(self, ctx):
        """채널과 관련된 명령어 그룹"""
        # 만약 서브 커맨드가 없다면, 사용 가능한 명령어 목록을 출력합니다.
        if ctx.invoked_subcommand is None:
            available_commands = ["현재채널"]
            embed = discord.Embed(
                title="명령어 목록",
                description='\n- !설정 '.join(available_commands),
                color=0x3498db  # 임베드 색상 설정
            )
            await ctx.send(embed=embed)

    @settings.command(name="채널")
    async def set_channel(self, ctx):
        """현재 채널로 채널 설정 저장"""
        try:
            channel = ctx.channel.id

            Settings.save('channel', channel)

            embed = discord.Embed(
                title="채널 변경 완료",
                description="현재 채널로 대상 채널을 설정하였습니다!",
                color=0x3498db  # 임베드 색상 설정
            )
            await ctx.send(embed=embed)

        except NotFound:
            embed = discord.Embed(
                title="채널 변경 실패",
                description="채널을 찾을 수 없습니다.",
                color=0xFF0000  # 실패했을 때의 색상
            )
            await ctx.send(embed=embed)
