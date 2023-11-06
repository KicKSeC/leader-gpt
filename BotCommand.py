import datetime
import random
import discord
from discord.ext import commands, tasks
import matplotlib.pyplot as plt


class LGPTCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.next_meeting = ""
        self.evaluations = {}
        self.role = {}
        self.rules = []
        self.assignments = {}

    @commands.group(name="도움말")
    async def help(self, ctx: discord.ext.commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("명령어 목록\n"
                           "- 팀원평가\n"
                           "- 평가\n"
                           "- 회의시간\n"
                           "- 역할분담\n"
                           "- 프로젝트일정\n"
                           "- 제촉하기\n"
                           "- 규칙")

    @commands.group(name="팀원평가")
    async def review_group(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("익명 혹은 실명을 선택해주세요. (예: !팀원평가 익명)")

    @review_group.command(name="익명")
    async def review_anonymous(self, ctx):
        await ctx.send("익명평가를 시작합나다.")
        guild = ctx.guild
        members = guild.members
        for member in members:
            if not member.bot:
                await member.send("익명으로 팀원을 평가하세요")

    @review_group.command(name="종료")
    async def finish_review(self, ctx):
        if not self.evaluations:
            await ctx.send("저장된 평가가 없습니다.")
            return
        result = "평가 결과:\n"
        for member_id, evaluation in self.evaluations.items():
            member = ctx.guild.get_member(member_id)
            result += f"{member.display_name}: {evaluation}\n"

        await ctx.send(result)
        self.evaluations = {}

    @commands.command(name="평가")
    async def evaluate(self, ctx, *, evaluation):
        self.evaluations[ctx.author.id] = evaluation
        await ctx.author.send("평가가 저장되었습니다.")

    @commands.group(name="회의시간")
    async def meeting(self, ctx):
        if ctx.invoked_subcommand is None:
            if self.next_meeting:
                await ctx.send(f"다음 회의는 {self.next_meeting}에 예정되어 있습니다.")
            else:
                await ctx.send("예정된 회의가 없습니다.")

    @meeting.command(name="정하기")
    async def arrange_meeting(self, ctx):
        await ctx.send("본인의 참석가능한 시간을 입력해주세요")

    @commands.group(name="역할분담")
    async def role_dividing(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("역할분담 방식과 역할을 입력해주세요\n"
                           "- 자동분배\n"
                           "- 사다리타기\n"
                           "- 제비뽑기\n"
                           "예: !역할분담 자동분배 역할1 역할2 역할3"
                           "역할이 입력되지 않는다면 역할이 숫자로 분배됩니다")

    @role_dividing.command(name="자동분배")
    async def role_random(self, ctx, *roles):
        roles = list(roles)
        members_count = len(ctx.guild.members) - 1
        members = ctx.guild.members
        n = 0
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
        result = ""
        for r in self.role:
            result += f"- {r}: {self.role[r]}\n"
        await ctx.send("역할분담 결과\n"
                       f"{result}")

    @commands.command(name="회의록작성")
    async def create_MOM(self, ctx):
        await ctx.send("회의록 작성")

    @commands.group(name="규칙")
    async def rule(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("규칙 생성, 추가 혹은 확인을 선택해주세요 (예: !규칙 생성)")

    @rule.command(name="생성")
    async def create_rule(self, ctx):
        await ctx.send("chatGPT를 통해 규칙생성")

    @rule.command(name="추가")
    async def append_rule(self, ctx, new_rule):
        self.rules.append(new_rule)
        rules = ""
        for idx, rule in enumerate(self.rules):
            rules += f"{idx + 1}. {rule}\n"
        await ctx.send("규칙이 추가되었습니다\n"
                       f"현재 규칙\n"
                       f"{rules}")

    @rule.command(name="확인")
    async def check_rule(self, ctx):
        rules = ""
        for idx, rule in enumerate(self.rules):
            rules += f"{idx + 1}. {rule}\n"
        await ctx.send("현재 규칙\n"
                       f"{rules}")

    @commands.group(name="과제")
    async def assignment_group(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("추가 명령어를 입력해주세요\n"
                           "- 부여\n"
                           "- 확인\n"
                           "- 제출")

    @assignment_group.command(name="부여")
    async def assign_assignment(self, ctx, content, deadline):
        user = ctx.author.name
        if user not in self.assignments:
            self.assignments[user] = [{'과제명': content, '마감일': deadline}]
        else:
            self.assignments[user].append({'과제명': content, '마감일': deadline})
        await ctx.send('과제 부여 완료')

    @assignment_group.command(name="확인")
    async def show_assignment(self, ctx):
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
        await ctx.send(data)

    @tasks.loop(hours=1)
    async def check_deadline(self, ctx):
        now = datetime.datetime.now()
        for ass in self.assignments:
            pass

    @commands.command(name="그래프")
    async def show_graph(self, ctx):
        x = [1, 2, 3, 4]
        y = [2, 4, 6, 8]
        plt.rcParams['font.family'] = 'Arial'
        plt.plot(x, y)
        plt.xlabel('X Axis')
        plt.ylabel('Y Axis')
        plt.title('Simple Graph')

        # 이미지 파일로 저장
        plt.savefig('graph.png')
        file = discord.File("graph.png", filename="graph.png")
        await ctx.send(file=file)
