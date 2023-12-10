import discord
from discord.ext import commands
import statistics as stt


class GroupReview(commands.Cog):
    """
    팀원들의 평가에 대한 명령어에 대한 클래스
    """

    def __init__(self, bot):
        self.bot = bot
        self.evaluations = {}
        self.evaluate = False

    @commands.group(name="팀원평가")
    async def review_group(self, ctx):
        """'팀원평가' 그룹 커맨드를 정의합니다. 사용자가 '팀원평가' 명령어를 입력하면, 서브 커맨드가 없는 경우에 실행되는 함수입니다."""
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                description="\'!팀원평가 시작\'을 입력해 익명 팀원평가를 시작 할 수 있습니다.",
                color=0x3498db
            )
            await ctx.send(embed=embed)

    @review_group.command(name="시작")
    async def review_anonymous(self, ctx):
        """
        사용자가 '팀원평가 시작' 명령어를 입력하면 실행되는 함수입니다. 익명으로 팀원을 평가하도록 안내합니다.
        """
        await ctx.send(embed=discord.Embed(description="평가를 시작합니다", color=0x3498db))
        guild = ctx.guild
        members = guild.members
        for member in members:
            if not member.bot:
                embed = discord.Embed(
                    title='팀원을 평가하세요',
                    description='DM으로 \'!평가 팀원명 점수\'를 입력해 팀원을 평가 할 수 있습니다\n예) \'!평가 홍길동 1\'\n'
                                '또한 \'!평가 홍길동 1 지난번 회의때 참석하지 않음\'과 같이 한줄평을 덧붙일 수 있습니다.',
                    color=0x3498db
                )
                await member.send(embed=embed)
        self.evaluate = True

    @review_group.command(name="종료")
    async def finish_review(self, ctx):
        """사용자가 '팀원평가 종료' 명령어를 입력하면 실행되는 함수입니다. 평가 결과를 출력하고 평가 데이터를 초기화합니다."""
        embed = discord.Embed()
        if not self.evaluations:  # 평가 데이터가 없는 경우, 안내 메시지를 출력하고 함수를 종료합니다.
            embed = discord.Embed(
                description="저장된 평가가 없습니다",
                color=0xFF0000
            )
        else:
            result = ""
            for member, evaluation in self.evaluations.items():  # 평가 데이터를 순회하면서, 각 멤버의 평가 결과를 문자열에 추가합니다.
                avg = stt.mean(evaluation['score'])
                result += f"{member}: {avg}\n"
                if evaluation['comments']:
                    for comment in evaluation['comments']:
                        result += f"- {comment}\n"
                else:
                    result += "- 한줄평 없음\n"
            embed = discord.Embed(
                title="---------- 평가 결과 ----------",
                description=result,
                color=0x3498db
            )
        await ctx.send(embed=embed)
        self.evaluations = {}
        self.evaluate = False

    @commands.command(name="평가")
    async def evaluate(self, ctx, member=None, score=None, *, comment=None):
        """사용자가 '평가' 명령어를 입력하면 실행되는 함수입니다. 평가 내용을 저장하고, 저장되었다는 메시지를 보냅니다"""
        # 평가가 시작되었는지 확인합니다
        if self.evaluate:
            if member is None or score is None:
                await ctx.send(embed=discord.Embed(title="잘못된 입력입니다", description="팀원명 혹은 점수가 올바르게 입력되지 않았습니다",
                                                   color=0xFF0000))
            score = int(score)
            if member not in self.evaluations:
                self.evaluations[member] = {"score": [score], "comments": [comment]}  # 사용자의 평가 내용을 저장합니다
            else:
                self.evaluations[member]['score'].append(score)
                self.evaluations[member]['comments'].append(comment)
            print(self.evaluations)
            await ctx.author.send(embed=discord.Embed(description="평가가 저장되었습니다", color=0x3498db))
        else:
            await ctx.send(embed=discord.Embed(title="진행되고 있는 평가가 없습니다",
                                               description="서버에서 !팀원평가 시작을 입력해 평가를 입력해주세요", color=0xFF0000))
