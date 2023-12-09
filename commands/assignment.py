import discord
from datetime import datetime, timedelta
from discord.ext import commands, tasks
import os
import json


class Assignment(commands.Cog):
    """
    과제에 대한 명령어에 대한 클래스 
    """

    def __init__(self, bot):
        self.bot = bot
        self.path = os.path.join("data", "events.json")
        print(self.path)
        try:
            with open(self.path, 'r') as f:
                content = json.load(f)
                self.assignments = content.get("assignment", {})
        except FileNotFoundError:
            self.assignments = {}

    def save_assignments(self):
        print("과제 갱신")
        with open(self.path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        content['assignment'] = self.assignments
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=4, ensure_ascii=False)

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
        user = ctx.author.name

        # 입력 유효성 검사 - 과제 내용이 비어 있는지 확인
        if not content:
            await ctx.send("올바른 과제 내용을 입력해주세요.")
            return

        # 입력 유효성 검사 - 날짜 형식이 올바른지 확인
        try:
            valid_date = datetime.strptime(deadline, "%Y-%m-%d").date()
        except ValueError:
            await ctx.send("올바른 날짜 형식(YYYY-MM-DD)으로 입력해주세요.")
            return

        # 유효성 검사 통과시 과제 부여
        if user not in self.assignments:
            self.assignments[user] = [{'과제명': content, '마감일': deadline}]
        else:
            self.assignments[user].append({'과제명': content, '마감일': deadline})
        embed = discord.Embed(
            description="과제 부여 완료",
            color=0x3498db
        )
        await ctx.send(embed=embed)
        await self.save_assignments()

    @assignment_group.command(name="확인")
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

    @tasks.loop(minutes=1)  # 1분 주기로 반복
    async def check_deadlines(self):
        print("과제 검사를 시작합니다")
        print(self.assignments)
        now = datetime.now().date()
        for user, assignments in self.assignments.items():
            for assignment in assignments:
                deadline = datetime.strptime(assignment['마감일'], "%Y-%m-%d").date()
                if deadline == now + timedelta(days=1):
                    print(f"{assignment} 의 마감일이 하루 남았습니다")
