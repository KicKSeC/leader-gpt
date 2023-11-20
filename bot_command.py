import datetime
import random
import discord
from discord.ext import commands, tasks
import matplotlib.pyplot as plt
from chatgpt import ChatGPT
import logging

# 로그 파일 설정
logging.basicConfig(filename='bot_command.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# TODO 더 나은 팀 규칙 생성 프롬프트 작성
PROMPT_CREATE_RULE = "팀을 위한 규칙을 나열해"

class LGPTCommand(commands.Cog):
    def __init__(self, bot):
        """
        클래스를 초기화하는 메서드입니다.
        봇, 다음 회의 시간, 평가, 역할, 규칙, 과제 등 여러 속성을 초기화합니다.
        """
        self.bot = bot
        self.next_meeting = ""
        self.commands = ["도움말", "팀원평가", "평가", "회의시간", "역할분담", 
                         "회의록 작성", "규칙", "과제", "그래프"]
        self.evaluations = {}
        self.role = {}
        self.rules = []
        self.assignments = {}
        
        self.chatgpt = ChatGPT()    
        
        # 대화를 기록하기 위한 변수들
        self.conversation = {}     # 메세지가 기록되는 딕셔너리. {'대화명', [[이름, 내용], ...]}
        self.record_names = []     # 기록되는 대화의 이름들
    
    @commands.group(name="도움말")
    async def help(self, ctx: discord.ext.commands.Context):
        """사용자가 '도움말' 명령어를 입력하면, 서브 커맨드가 없는 경우에 실행되는 함수입니다."""
        # 만약 서브 커맨드가 없다면, 사용 가능한 명령어 목록을 출력합니다.
        if ctx.invoked_subcommand is None:
            await ctx.send("\n- ".join(["명령어 목록"] + self.commands))

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
        if not self.evaluations:   # 평가 데이터가 없는 경우, 안내 메시지를 출력하고 함수를 종료합니다.
            await ctx.send("저장된 평가가 없습니다.")
            return
        result = "평가 결과:\n"     # 평가 결과를 저장할 문자열을 초기화합니다.
        for member_id, evaluation in self.evaluations.items():  # 평가 데이터를 순회하면서, 각 멤버의 평가 결과를 문자열에 추가합니다.
            member = ctx.guild.get_member(member_id)
            result += f"{member.display_name}: {evaluation}\n"

        await ctx.send(result)
        self.evaluations = {}

    @commands.command(name="평가")
    async def evaluate(self, ctx, *, evaluation):
        """사용자가 '평가' 명령어를 입력하면 실행되는 함수입니다. 평가 내용을 저장하고, 저장되었다는 메시지를 보냅니다."""
        self.evaluations[ctx.author.id] = evaluation    # 사용자의 평가 내용을 저장합니다.
        await ctx.author.send("평가가 저장되었습니다.")

    @commands.group(name="회의시간")
    async def meeting(self, ctx):
        """사용자가 '회의시간' 명령어를 입력하면, 서브 커맨드가 없는 경우에 실행되는 함수입니다"""
        # 만약 서브 커맨드가 없다면, 다음 회의 시간을 출력하거나, 예정된 회의가 없다는 메시지를 출력합니다.
        if ctx.invoked_subcommand is None:
            if self.next_meeting:
                await ctx.send(f"다음 회의는 {self.next_meeting}에 예정되어 있습니다.")
            else:
                await ctx.send("예정된 회의가 없습니다.")

    @meeting.command(name="정하기")
    async def arrange_meeting(self, ctx):
        """사용자가 '회의시간 정하기' 명령어를 입력하면 실행되는 함수입니다. 회의 참석 가능 시간을 입력하도록 안내합니다."""
        await ctx.send("본인의 참석가능한 시간을 입력해주세요")

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

    @commands.command(name="회의록작성")
    async def create_MOM(self, ctx):
        """사용자가 '회의록작성' 명령어를 입력하면 실행되는 함수입니다. 회의록 작성을 시작합니다."""
        await ctx.send("회의록 작성")

    @commands.group(name="규칙")
    async def rule(self, ctx):
        """사용자가 '규칙' 명령어를 입력하면, 서브 커맨드가 없는 경우에 실행되는 함수입니다"""
        if ctx.invoked_subcommand is None:
            await ctx.send("규칙 생성, 추가 혹은 확인을 선택해주세요 (예: !규칙 생성)")

    @rule.command(name="생성")
    async def create_rule(self, ctx):
        """사용자가 '규칙 생성' 명령어를 입력하면 실행되는 함수입니다. 규칙을 생성합니다."""
        await ctx.send("chatGPT를 통해 규칙생성")
        if not ChatGPT.is_answering:    # 챗지피티가 이미 사용되고 있지는 않은지 확인
            rule = ChatGPT.get_response(message=PROMPT_CREATE_RULE)
            await ctx.send(rule)
            self.rules.append(rule)

    @rule.command(name="추가")
    async def append_rule(self, ctx, new_rule):
        """사용자가 '규칙 추가' 명령어를 입력하면 실행되는 함수입니다. 새로운 규칙을 추가하고, 추가된 규칙을 출력합니다"""
        self.rules.append(new_rule)
        rules = ""
        for idx, rule in enumerate(self.rules):
            rules += f"{idx + 1}. {rule}\n"
        await ctx.send("규칙이 추가되었습니다\n"
                       f"현재 규칙\n"
                       f"{rules}")

    @rule.command(name="확인")
    async def check_rule(self, ctx):
        """사용자가 '규칙 확인' 명령어를 입력하면 실행되는 함수입니다. 현재 규칙을 출력합니다"""
        rules = ""
        for idx, rule in enumerate(self.rules):
            rules += f"{idx + 1}. {rule}\n"
        await ctx.send("현재 규칙\n"
                       f"{rules}")

    @commands.group(name="과제")
    async def assignment_group(self, ctx):
        """사용자가 '과제' 명령어를 입력하면, 서브 커맨드가 없는 경우에 실행되는 함수입니다"""
        # 만약 서브 커맨드가 없다면, 추가 명령어를 입력하도록 안내합니다
        if ctx.invoked_subcommand is None:
            await ctx.send("추가 명령어를 입력해주세요\n"
                            "- 부여\n"
                            "- 확인\n"
                            "- 제출")

    @assignment_group.command(name="부여")
    async def assign_assignment(self, ctx, content, deadline):
        """사용자가 '과제 부여' 명령어를 입력하면 실행되는 함수입니다. 과제를 부여하고, 부여 완료를 알립니다."""
        user = ctx.author.name  # 명령어를 입력한 사용자의 이름을 가져옵니다
        if user not in self.assignments:    # 이 사용자에게 처음으로 과제를 부여하는 경우, 새로운 과제 리스트를 생성합니다.
            self.assignments[user] = [{'과제명': content, '마감일': deadline}]
        else:                   # 이 사용자에게 이미 과제가 부여된 경우, 과제 리스트에 새로운 과제를 추가합니다.
            self.assignments[user].append({'과제명': content, '마감일': deadline})
        await ctx.send('과제 부여 완료')

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
        await ctx.send(data)

    @tasks.loop(hours=1)
    async def check_deadline(self, ctx):
        """과제의 마감 시간을 확인하는 함수입니다"""
        now = datetime.datetime.now()
        for ass in self.assignments: # 부여된 모든 과제를 순회합니다.
            pass                    # 여기에 마감 시간을 확인하고 알림을 보내는 코드를 추가할 수 있습니다.

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
        
    @commands.group(name="기록")
    async def record(self, ctx):
        '''디스코드간에 오가는 대화를 기록합니다.'''
        if ctx.invoked_subcommand is None:
            await ctx.send("기록 시작, 기록 종료, 기록 보이기")
        
    @record.command(name="시작")
    async def start_record(self, ctx):
        """기록 시작"""
        if "기록" in self.record_names:
            await ctx.send("이미 기록중입니다.")
            return
    
        await ctx.send("기록 시작")
        self.record_names.append("기록")
        self.conversation["기록"] = []
        
    @record.command(name="종료")
    async def end_record(self, ctx):
        """기록 종료"""
        await ctx.send("기록 종료")
        self.record_names.remove("기록")

    @record.command(name="보이기")
    async def show_record(self, ctx):
        """기록된 내용을 보여줌""" 
        result = "'기록'의 내용은\n"
        for message in self.conversation["기록"]:
            result += f"{message[0]}: {message[1]}\n"
        await ctx.send(result)
     
    @commands.Cog.listener()
    async def on_message(self, ctx):
        '''디스코드 상의 오가는 대화를 기록되는 리스트에 저장''' 
        for record_name in self.record_names:
            if ctx.author != self.bot.user:
                self.conversation[record_name].append([ctx.author.name, ctx.content])

    # TODO 이모지 투표 기능 추가
    # 이모지 API https://discordpy-ko.github.io/api.html#discord.Emoji
