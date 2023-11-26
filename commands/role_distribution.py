import discord
import random
from discord.ext import commands, tasks


class RoleDistribution(commands.Cog):
    """
    팀원 간의 역할 분배에 관한 커맨트에 대한 클래스
    """

    def __init__(self, bot):
        self.bot = bot

        self.role = {}

    @commands.group(name="역할분담")
    async def role_dividing(self, ctx):
        """사용자가 '역할분담' 명령어를 입력하면, 서브 커맨드가 없는 경우에 실행되는 함수입니다."""
        # 만약 서브 커맨드가 없다면, 역할분담 방식과 역할을 입력하도록 안내합니다.
        if ctx.invoked_subcommand is None:
            await ctx.send("역할분담 방식과 역할을 입력해주세요\n"
                           "- 자동분배\n"
                           "- 사다리타기\n"
                           "- 제비뽑기\n"
                           "예: !역할분담 자동분배 역할1 역할2 역할3"
                           "역할이 입력되지 않는다면 역할이 숫자로 분배됩니다")

    @role_dividing.command(name="자동분배")
    async def role_random(self, ctx, *roles):
        """사용자가 '역할분담 자동분배' 명령어를 입력하면 실행되는 함수입니다. 입력된 역할을 무작위로 분배합니다."""
        roles = list(roles)
        members_count = len(ctx.guild.members) - 1
        members = ctx.guild.members
        n = 0
        # 입력받은 역할의 개수와 팀원 수가 일치하지 않는 경우, 안내 메시지를 출력하고 함수를 종료합니다.
        if len(roles) != members_count and len(roles) > 0:
            await ctx.send("입력받은 역할의 개수와 팀 구성원의 명수가 일치하지 않습니다")
            return

        if len(roles) == 0:
            roles = [n for n in range(1, members_count + 1)]

        random.shuffle(roles)
        for member in members:
            if not member.bot:
                self.role[member.name] = roles[n]
                n += 1

        self.role = dict(sorted(self.role.items(), key=lambda x: x[1]))
        result = ""
        for r in self.role:
            result += f"{r}: {self.role[r]}\n"
        await ctx.send(result)

    @role_dividing.command(name="결과")
    async def role_result(self, ctx):
        """사용자가 '역할분담 결과' 명령어를 입력하면 실행되는 함수입니다. 역할 분배 결과를 출력합니다."""
        result = ""
        for r in self.role:
            result += f"- {r}: {self.role[r]}\n"
        await ctx.send("역할분담 결과\n"
                       f"{result}")
