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
            embed = discord.Embed(
                title="사용법",
                description="예: !역할분담 시작 역할1 역할2 역할3\n"
                            "역할이 입력되지 않는다면 역할이 숫자로 분배됩니다",
                color=0x3498db
            )
            await ctx.send(embed=embed)

    @role_dividing.command(name="시작")
    async def role_random(self, ctx, *roles):
        """사용자가 '역할분담 자동분배' 명령어를 입력하면 실행되는 함수입니다. 입력된 역할을 무작위로 분배합니다."""
        member_count = 0
        members = ctx.guild.members
        embed = None
        for member in members:
            if not member.bot:
                member_count += 1

        if roles:
            roles = list(roles)
            # 입력받은 역할의 개수와 팀원 수가 일치하지 않는 경우, 안내 메시지를 출력하고 함수를 종료합니다.
            if len(roles) != member_count:
                embed = discord.Embed(
                    description="입력받은 역할의 개수와 팀 구성원의 명수가 일치하지 않습니다",
                    color=0xFF0000
                )
                await ctx.send(embed=embed)
                return
        else:
            roles = [n + 1 for n in range(member_count)]
        random.shuffle(roles)
        n = 0
        for member in members:
            if not member.bot:
                self.role[member.display_name] = roles[n]
                n += 1
                embed = discord.Embed(
                    description="역할분담이 완료되었습니다\n"
                                "'!역할분담 결과'를 통해 결과를 확인하세요",
                    color=0x3498db
                )
        await ctx.send(embed=embed)

    @role_dividing.command(name="결과")
    async def role_result(self, ctx):
        """사용자가 '역할분담 결과' 명령어를 입력하면 실행되는 함수입니다. 역할 분배 결과를 출력합니다."""
        result = ""
        for member, role in self.role.items():
            result += f"- {member}: {role}\n"
        await ctx.send(embed=discord.Embed(title="역할분담 결과", description=result, color=0x3498db))
