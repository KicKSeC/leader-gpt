import discord 
import matplotlib.pyplot as plt
from chatgpt import ChatGPT
from discord.ext import commands
                

class LGPTCommand(commands.Cog):
    def __init__(self, bot):
        """
        클래스를 초기화하는 메서드입니다.
        봇, 다음 회의 시간, 평가, 역할, 규칙, 과제 등 여러 속성을 초기화합니다.
        """
        self.bot = bot
        self.commands = ["도움말", "설정", "답변", "팀원평가", "평가", "회의시간", "역할분담",
                         "회의록작성", "규칙", "과제", "그래프", "일정"]

    @commands.group(name="도움말")
    async def help(self, ctx: discord.ext.commands.Context):
        """사용자가 '도움말' 명령어를 입력하면, 서브 커맨드가 없는 경우에 실행되는 함수입니다."""
        # 만약 서브 커맨드가 없다면, 사용 가능한 명령어 목록을 출력합니다.
        if ctx.invoked_subcommand is None:
            description = '\n- '.join(self.commands)
            description += "첫 실행이시라면 !채널 관련 명령어를 통해 초기 설정을 완료하여 주십시오"
            embed = discord.Embed(
                title="명령어 목록",
                description=description,
                color=0x3498db  # 임베드 색상 설정
            )
            await ctx.send(embed=embed)
    
    @commands.command(name="답변")
    async def answer(self, ctx, *, message):
        '''챗지피티 답변 생성'''
        msg = await ctx.send("답변중...")
        ans_txt = ""
        stream = ChatGPT.get_response_by_stream(message)
        
        while True:
            try: 
                ans_txt = next(stream)
            except StopIteration:       # 답변이 끝났는지 확인
                break
            
            await msg.edit(content=ans_txt+"-")
        await msg.edit(content=ans_txt)


    # 최종 구현여부가 정해지지 않은 기능
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

    # TODO 이모지 투표 기능 추가
    # 이모지 API https://discordpy-ko.github.io/api.html#discord.Emoji
