import discord
from discord.ext import commands, tasks 
from chatgpt import ChatGPT

# TODO 더 나은 팀 규칙 생성 프롬프트 작성
PROMPT_CREATE_RULE = "팀을 위한 규칙을 숫자 없이 나열해. 조원이 불참했을 때, 분쟁이 있을 때 등등"

class TeamRule(commands.Cog):
    """
    팀의 규칙을 정하는 커맨드에 대한 클래스
    """ 
    def __init__(self, bot):
        self.bot = bot
        
        self.rules = []
        
    @commands.group(name="규칙")
    async def rule(self, ctx):
        """사용자가 '규칙' 명령어를 입력하면, 서브 커맨드가 없는 경우에 실행되는 함수입니다"""
        if ctx.invoked_subcommand is None:
            await ctx.send("규칙 생성, 추가 혹은 확인을 선택해주세요 (예: !규칙 생성)")

    @rule.command(name="생성")
    async def create_rule(self, ctx):
        """사용자가 '규칙 생성' 명령어를 입력하면 실행되는 함수입니다. 규칙을 생성합니다."""
        if not ChatGPT.is_answering:    # 챗지피티가 이미 사용되고 있지는 않은지 확인 
            await ctx.send("ChatGPT를 통해 규칙생성")
            rules = ChatGPT.get_response(message=PROMPT_CREATE_RULE)
            await ctx.send(rules)
            
            # 나열된 규칙을 개별적으로 나누어 (빈 거 제외하고) 각각 저장
            for rule in [x for x in rules.split('\n') if x != ""]:
                self.rules.append(rule)
        else:
            await ctx.send("이미 답변 중에 있습니다. 답변 이후에 요청해 주십시오.")

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