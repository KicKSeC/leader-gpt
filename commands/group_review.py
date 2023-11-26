from discord.ext import commands


class GroupReview(commands.Cog):
    """
    팀원들의 평가에 대한 명령어에 대한 클래스
    """

    def __init__(self, bot):
        self.bot = bot

        self.evaluations = {}

    @commands.group(name="팀원평가")
    async def review_group(self, ctx):
        """'팀원평가' 그룹 커맨드를 정의합니다. 사용자가 '팀원평가' 명령어를 입력하면, 서브 커맨드가 없는 경우에 실행되는 함수입니다."""
        if ctx.invoked_subcommand is None:
            await ctx.send("익명 혹은 실명을 선택해주세요. (예: !팀원평가 익명)")

    @review_group.command(name="익명")
    async def review_anonymous(self, ctx):
        """
        사용자가 '팀원평가 익명' 명령어를 입력하면 실행되는 함수입니다. 익명으로 팀원을 평가하도록 안내합니다.
        """
        await ctx.send("익명평가를 시작합나다.")
        guild = ctx.guild
        members = guild.members
        for member in members:
            if not member.bot:
                await member.send("익명으로 팀원을 평가하세요")

    @review_group.command(name="종료")
    async def finish_review(self, ctx):
        """사용자가 '팀원평가 종료' 명령어를 입력하면 실행되는 함수입니다. 평가 결과를 출력하고 평가 데이터를 초기화합니다."""
        if not self.evaluations:  # 평가 데이터가 없는 경우, 안내 메시지를 출력하고 함수를 종료합니다.
            await ctx.send("저장된 평가가 없습니다.")
            return
        result = "평가 결과:\n"  # 평가 결과를 저장할 문자열을 초기화합니다.
        for member_id, evaluation in self.evaluations.items():  # 평가 데이터를 순회하면서, 각 멤버의 평가 결과를 문자열에 추가합니다.
            member = ctx.guild.get_member(member_id)
            result += f"{member.display_name}: {evaluation}\n"

        await ctx.send(result)
        self.evaluations = {}

    @commands.command(name="평가")
    async def evaluate(self, ctx, *, evaluation):
        """사용자가 '평가' 명령어를 입력하면 실행되는 함수입니다. 평가 내용을 저장하고, 저장되었다는 메시지를 보냅니다."""
        self.evaluations[ctx.author.id] = evaluation  # 사용자의 평가 내용을 저장합니다.
        await ctx.author.send("평가가 저장되었습니다.")
