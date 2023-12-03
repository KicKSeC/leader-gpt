import logging

import discord
from discord.ext import commands
from chatgpt import ChatGPT

PROMPT_CREATE_MEETING_LOG = "서기로서, 아래 나열되는 회의 대화를 요약, 정리, 나열해서 회의록을 작성해"


class MeetingLog(commands.Cog):
    """
    회의록을 작성하는 디스코드 커멘드에 관한 클래스 
    """

    def __init__(self, bot):
        self.bot = bot

        # 대화를 기록하기 위한 변수들
        self.conversation = {}  # 메세지가 기록되는 딕셔너리. {'대화명', [[이름, 내용], ...]}
        self.record_names = []  # 기록되는 대화의 이름들

    @commands.group(name="기록")
    async def record(self, ctx):
        """디스코드간에 오가는 대화를 기록합니다."""
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="명령어 목록",
                description="- 기록 시작\n"
                            "- 기록 종료\n"
                            "- 기록 보이기",
                color=0x3498db
            )
            await ctx.send(embed=embed)

    @record.command(name="시작")
    async def start_record(self, ctx):
        """기록 시작"""
        if "기록" in self.record_names:
            await ctx.send(embed=discord.Embed(description="이미 기록중입니다", color=0x3498db))
            return

        await ctx.send(embed=discord.Embed(description="기록 시작", color=0x3498db))
        self.record_names.append("기록")
        self.conversation["기록"] = []

    @record.command(name="종료")
    async def end_record(self, ctx):
        """기록 종료"""
        await ctx.send(embed=discord.Embed(description="기록 종료", color=0x3498db))
        self.record_names.remove("기록")

    @record.command(name="보이기")
    async def show_record(self, ctx):
        """기록된 내용을 보여줌"""
        result = "'기록'의 내용은\n"
        for message in self.conversation["기록"]:
            result += f"{message[0]}: {message[1]}\n"
        await ctx.send(embed=discord.Embed(title="기록", description=result, color=0x3498db))

    @commands.command(name="회의록작성")
    async def create_meeting_log(self, ctx):
        """사용자가 '회의록작성' 명령어를 입력하면 실행되는 함수입니다. 회의록 작성을 시작합니다."""
        if not self.conversation["기록"]:
            await ctx.send(embed=discord.Embed(description="기록된 회의가 없습니다. '!기록 시작'으로 회의를 기록하십시오.", color=0x3498db))
            return

        await ctx.send(embed=discord.Embed(title="회의록 작성중...", description="잠시만 기다려 주세요", color=0x3498db))
        prompt = PROMPT_CREATE_MEETING_LOG + "\n" + "\n".join(
            [f"{msg[0]}: {msg[1]}" for msg in self.conversation['기록']])

        meeting_log = ChatGPT.get_response(prompt)

        logging.info(meeting_log)
        await ctx.send(embed=discord.Embed(title="회의록", description=meeting_log, color=0x3498db))

    @commands.Cog.listener()
    async def on_message(self, ctx):
        """디스코드 상의 오가는 대화를 각각의 리스트에 저장"""
        for record_name in self.record_names:
            if ctx.author != self.bot.user:
                self.conversation[record_name].append([ctx.author.name, ctx.content])
