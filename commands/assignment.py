import discord
import datetime
from discord.ext import commands, tasks


class Assignment(commands.Cog):
    """
    과제에 대한 명령어에 대한 클래스 
    """

    def __init__(self, bot):
        self.bot = bot

        self.assignments = {}

    @commands.group(name="과제")
    async def assignment_group(self, ctx):
        """사용자가 '과제' 명령어를 입력하면, 서브 커맨드가 없는 경우에 실행되는 함수입니다"""
        # 만약 서브 커맨드가 없다면, 추가 명령어를 입력하도록 안내합니다
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="추가 명령어를 입력해주세요",
                description="- 부여\n"
                            "- 확인\n"
                            "- 제출",
                color=0x3498db
            )
            await ctx.send(embed=embed)

    @assignment_group.command(name="부여")
    async def assign_assignment(self, ctx, content, deadline):
        """사용자가 '과제 부여' 명령어를 입력하면 실행되는 함수입니다. 과제를 부여하고, 부여 완료를 알립니다."""
        user = ctx.author.name  # 명령어를 입력한 사용자의 이름을 가져옵니다
        if user not in self.assignments:  # 이 사용자에게 처음으로 과제를 부여하는 경우, 새로운 과제 리스트를 생성합니다.
            self.assignments[user] = [{'과제명': content, '마감일': deadline}]
        else:  # 이 사용자에게 이미 과제가 부여된 경우, 과제 리스트에 새로운 과제를 추가합니다.
            self.assignments[user].append({'과제명': content, '마감일': deadline})
        embed = discord.Embed(
            description="과제 부여 완료",
            color=0x3498db
        )
        await ctx.send(embed=embed)

    @assignment_group.command(name="확인")ㅍ
    async def show_assignment(self, ctx):
        """사용자가 '과제 확인' 명령어를 입력하면 실행되는 함수입니다. 모든 멤버의 과제를 출력합니다"""
        members = ctx.guild.members
        data = ""
        for member in members:
            if not member.bot:
                data += f"{member.name}\n"
                if member.name in self.assignments:
                    for idx, assignment in enumerate(self.assignments[member.name]):
                        data += f"- {assignment['과제명']}: {assignment['마감일']}까지\n"
                else:
                    data += "- 과제 없음\n"
        embed = discord.Embed(
            description=data,
            color=0x3498db
        )
        await ctx.send(embed=embed)

    @tasks.loop(hours=1)
    async def check_deadline(self, ctx):
        """과제의 마감 시간을 확인하는 함수입니다"""
        now = datetime.datetime.now()
        for ass in self.assignments:  # 부여된 모든 과제를 순회합니다.
            pass  # 여기에 마감 시간을 확인하고 알림을 보내는 코드를 추가할 수 있습니다.
