import discord
import logging
from datetime import datetime 
from os import name
from discord.ext import commands
from events import Event, Events

logging.basicConfig(filename='bot_command.log', level=logging.INFO,  # 로그 파일 설정
                    format='%(asctime)s:%(levelname)s:%(message)s')

class Schedule(commands.Cog):
    """
    팀원의 일정을 관리하는 커맨드에 대한 클래스
    """

    def __init__(self, bot):
        self.bot = bot
        self.next_meeting = ""
        self.event = Events()
        
    @commands.group(name="일정")
    async def schedule(self, ctx):
        '''사용자가 '일정' 명령어를 서브 커맨드 없이 입력하는 경우의 함수'''
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="명령어 목록",
                description='- 일정 추가 "0000-00-00" "일정 이름" "내용"\n'
                            '- 일정 삭제 "0000-00-00"\n'
                            "- 일정 보이기\n"
                            "- 일정 저장",
                color=0x3498db
            )
            await ctx.send(embed=embed)
    
    @schedule.command(name="추가")
    async def add_schedule(self, ctx):
        def parse_schedule_input(input_string:str):
            try:
                input_list = input_string.split('"') 
                # input_list 는 ['!일정 추가 ', '2023-10-23', ' ', '회의', ' ', '좋아', ''] 형식
                
                _date = input_list[1].strip()
                _name = input_list[3].strip()
                _content = input_list[5].strip()
                return _date, _name, _content
            except ValueError:
                return None, None, None
        
        input_string = ctx.message.content
        date, name, content = parse_schedule_input(input_string) 
            
        if (not date or not name or not content) or not Event.check_date(date):
            embed = discord.Embed(
                title="입력을 확인하여주십시오",
                description='예시) !일정 추가 "2023-10-20" "일정 이름" "내용"\n',
                color=0x3498db
            )
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="일정이 등록되었습니다",
            description=f"date: {date}\n"
                        f"name: {name}\n"
                        f"content: {content}\n",
            color=0x3498db
        )
        
        self.event.push(date, name, content)
        await ctx.send(embed=embed)
        
    @schedule.command(name="삭제")
    async def schedule_delete(self, ctx):
        def parse_schedule_input(input_string:str):
            try:
                input_list = input_string.split('"') 
                # input_list 는 ['!일정 삭제 ', '2023-10-23'] 형식
                _date = input_list[1].strip()
                return _date
            except ValueError:
                return None
            
        input_string = ctx.message.content
        date = parse_schedule_input(input_string) 
        
        if not date or not Event.check_date(date):
            embed = discord.Embed(
                title="입력을 확인하여주십시오",
                description='예시) !일정 삭제 "2023-10-20"\n',
                color=0x3498db
            )
            await ctx.send(embed=embed)
            return
        
        is_deleted = self.event.delete(date)

        if is_deleted:
            embed = discord.Embed(
                title=f"{date} 일정이 삭제되었습니다",
                color=0x3498db
            )
        else:
            embed = discord.Embed(
                title=f"{date} 일정이 삭제되지 못하였습니다",
                description="정확히 입력하였는지 확인하십시오",
                color=0x3498db
            )
        
        await ctx.send(embed=embed)
        
        
    @schedule.command(name="저장")
    async def schedule_save(self, ctx):
        self.event.save()
        await ctx.send("저장되었습니다!")
        
    @schedule.command(name="보이기")
    async def schedule_show(self, ctx):
        events = self.event.get_events()
        description = ""
        for event in events:
             description += f'{event.date.strftime("%Y-%m-%d")}:{event.name}:{event.content}\n'
        embed = discord.Embed(
            title="일정 목록",
            description=description,
            color=0x3498db
        )
        await ctx.send(embed=embed)

    @commands.group(name="회의시간")
    async def meeting(self, ctx):
        """사용자가 '회의시간' 명령어를 입력하면, 서브 커맨드가 없는 경우에 실행되는 함수입니다"""
        # 만약 서브 커맨드가 없다면, 다음 회의 시간을 출력하거나, 예정된 회의가 없다는 메시지를 출력합니다.
        if ctx.invoked_subcommand is None:
            if self.next_meeting:
                embed = discord.Embed(
                    title="다음 회의 시간",
                    description=f"다음 회의는 {self.next_meeting}에 예정되어 있습니다.",
                    color=0x3498db
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send(embed=discord.Embed(description="예정된 회의가 없습니다.", color=0x3498db))

    @meeting.command(name="정하기")
    async def arrange_meeting(self, ctx):
        """사용자가 '회의시간 정하기' 명령어를 입력하면 실행되는 함수입니다. 회의 참석 가능 시간을 입력하도록 안내합니다."""
        await ctx.send(embed=discord.Embed(description="본인의 참석가능한 시간을 입력해주세요", color=0x3498db))