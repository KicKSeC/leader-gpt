import discord
from discord.ext import commands, tasks


class Schedule(commands.Cog):
    """
    팀원의 일정을 관리하는 커맨드에 대한 클래스
    """

    def __init__(self, bot):
        self.bot = bot
        self.next_meeting = ""

    @commands.group(name="회의시간")
    async def meeting(self, ctx):
        """사용자가 '회의시간' 명령어를 입력하면, 서브 커맨드가 없는 경우에 실행되는 함수입니다"""
        # 만약 서브 커맨드가 없다면, 다음 회의 시간을 출력하거나, 예정된 회의가 없다는 메시지를 출력합니다.
        if ctx.invoked_subcommand is None:
            if self.next_meeting:
                embed = discord.Embed(
                    title="다음 회의 시간",
                    description=f"다음 회의는 {self.next_meeting}에 예정되어 있습니다.",
                    color=0x3498db
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send(embed=discord.Embed(description="예정된 회의가 없습니다.", color=0x3498db))

    @meeting.command(name="정하기")
    async def arrange_meeting(self, ctx):
        """사용자가 '회의시간 정하기' 명령어를 입력하면 실행되는 함수입니다. 회의 참석 가능 시간을 입력하도록 안내합니다."""
        await ctx.send(embed=discord.Embed(description="본인의 참석가능한 시간을 입력해주세요", color=0x3498db))
