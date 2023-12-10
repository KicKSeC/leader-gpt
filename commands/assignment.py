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
        self.path_data = os.path.join("data", "data.json")  # 과제 데이터 파일 경로 설정
        self.path_setting = os.path.join("data", "settings.json")  # 채널 ID 저장되어 있는 파일 경로 설정
        self.channel_id = None
        try:
            with open(self.path_data, 'r') as f:
                content = json.load(f)
                self.assignments = content.get("assignment", {})  # 데이터 로드, 없으면 빈 딕셔너리 생성
        except FileNotFoundError:
            self.assignments = {}

    def upadate_channel(self):
        print("채널 id 업데이트")
        try:
            with open(self.path_setting, 'r') as f:
                content = json.load(f)
                print(content)
                self.channel_id = content.get("channel")
                print(self.channel_id)
        except FileNotFoundError:
            print("파일 없음")
            self.channel_id = None

    def save_assignments(self):
        """과제 데이터를 파일에 저장"""
        print("과제 갱신")
        with open(self.path_data, 'r', encoding='utf-8') as f:
            content = json.load(f)
        content['assignment'] = self.assignments
        with open(self.path_data, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=4, ensure_ascii=False)

    @commands.group(name="과제")
    async def assignment_group(self, ctx):
        """'과제' 명령어 처리 함수"""
        if ctx.invoked_subcommand is None:
            # 서브 명령어가 없을 때 안내하는 Embed 메시지 출력
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
        """'과제 부여' 명령어 처리 함수"""
        user = ctx.author.display_name

        # 입력 유효성 검사
        if not content:
            # 과제 내용이 비어있을 경우 안내 메시지 출력
            embed = discord.Embed(
                description="올바른 과제 내용을 입력해주세요",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return

        if not deadline:
            # 마감일이 비어있을 경우 안내 메시지 출력
            embed = discord.Embed(
                description="올바른 마감일을 입력해주세요",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return

        try:
            valid_date = datetime.strptime(deadline, "%Y-%m-%d").date()
        except ValueError:
            # 날짜 형식이 올바르지 않을 경우 안내 메시지 출력
            embed = discord.Embed(
                description="올바른 날짜 형식(YYYY-MM-DD)으로 입력해주세요",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
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
        self.save_assignments()
        await ctx.send(embed=embed)

    @assignment_group.command(name="확인")
    async def show_assignment(self, ctx):
        """'과제 확인' 명령어 처리 함수"""
        members = ctx.guild.members
        data = ""
        for member in members:
            if not member.bot:
                data += f"{member.display_name}\n"
                if member.display_name in self.assignments:
                    for idx, assignment in enumerate(self.assignments[member.display_name]):
                        data += f"- {assignment['과제명']}: {assignment['마감일']}까지\n"
                else:
                    data += "- 과제 없음\n"
        embed = discord.Embed(
            description=data,
            color=0x3498db
        )
        await ctx.send(embed=embed)

    @assignment_group.command(name="삭제")
    async def remove_assignment(self, ctx, user, content):
        """'과제 삭제' 명령어 처리 함수"""
        if user in self.assignments and any(assignment['과제명'] == content for assignment in self.assignments[user]):
            self.assignments[user] = [assignment for assignment in self.assignments[user] if
                                      assignment['과제명'] != content]
            print(f"{user}의 {content} 과제가 삭제되었습니다.")
        print(self.assignments)
        self.save_assignments()

    @tasks.loop(minutes=1)
    async def check_deadlines(self):
        """과제 마감일 확인 및 처리하는 함수"""
        self.upadate_channel()
        print(self.channel_id)
        if self.channel_id is not None:
            print("과제 검사를 시작합니다")
            reserve_remove = []
            today = datetime.now().date()

            channel = self.bot.get_channel(self.channel_id)

            for user, assignments in self.assignments.items():
                for assignment in assignments:
                    deadline = datetime.strptime(assignment['마감일'], "%Y-%m-%d").date()
                    if deadline == today + timedelta(days=1):
                        embed = discord.Embed(
                            title="과제 마감 임박",
                            description=f"{user}님의 {assignment['과제명']}의 마감기한이 1일 남았습니다",
                            color=0xFFA500
                        )
                        await channel.send(embed=embed)
                    elif deadline < today:
                        reserve_remove.append((user, assignment))
            for user, assignment in reserve_remove:
                self.assignments[user].remove(assignment)
            self.save_assignments()
