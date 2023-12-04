import logging
import discord
from datetime import datetime  
from discord.ext import commands, tasks
from events import Event, Events
from settings import Settings

class Schedule(commands.Cog):
    """
    팀원의 일정을 관리하는 커맨드에 대한 클래스
    """

    def __init__(self, bot):
        self.bot = bot   
        self.next_meeting = ""
        self.events = Events() 
        
        self.check_schedule_launcher.start()        # 에러가 뜨지만 잘 작동함
        
    @commands.group(name="일정")
    async def schedule(self, ctx):
        '''사용자가 '일정' 명령어를 서브 커맨드 없이 입력하는 경우의 함수'''
        
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="명령어 목록",
                description='- 일정 추가 "0000-00-00 00" "일정 이름" "내용"\n'
                            '- 일정 삭제 "0000-00-00 00"\n'
                            "- 일정 확인\n"
                            "- 일정 저장",
                color=0x3498db
            )
            await ctx.send(embed=embed)
    
    @schedule.command(name="추가")
    async def add_schedule(self, ctx):
        '''새 일정을 추가함'''
        def parse_schedule_input(input_string:str):
            try:
                input_list = input_string.split('"') 
                # input_list 는 ['!일정 추가 ', '2023-10-23', ' ', '회의', ' ', '좋아', ''] 형식
                # assigned를 설정할 경우 [..., '좋아', ' ', 'selbri']
                
                _date = input_list[1].strip()
                _name = input_list[3].strip()
                _content = input_list[5].strip()
                if len(input_list) > 7:
                    _assigned = input_list[7].strip()
                else:
                    _assigned = ""
                    
                return _date, _name, _content, _assigned
            except ValueError:
                return None, None, None, None
        
        input_string = ctx.message.content
        date, name, content, assigned = parse_schedule_input(input_string) 
        logging.info('%s, %s, %s, %s', date, name, content, assigned)
            
        if (not date or not name or not content) or not Event.check_date(date):
            embed = discord.Embed(
                title="입력을 확인하여주십시오",
                description='예시) !일정 추가 "2023-10-20 20" "일정 이름" "내용" (선택)"과제 해당자"\n',
                color=0x3498db
            )
            await ctx.send(embed=embed)
            return
        description = f"date: {date}\n" + f"name: {name}\n" + f"content: {content}\n" 
        description += f"assigned: {assigned if (assigned != '') else '없음'}"
        embed = discord.Embed(
            title="일정이 등록되었습니다",
            description=description,
            color=0x3498db
        )
        
        if assigned is None:
            raise ValueError()
        self.events.push(date, name, content, assigned)
        await ctx.send(embed=embed)
        
    @schedule.command(name="삭제")
    async def delete_schedule(self, ctx):
        '''입력된 이름의 일정을 삭제함'''
        def parse_schedule_input(input_string:str):
            try:
                input_list = input_string.split('"') 
                # input_list 는 ['!일정 삭제 ', '회의'] 형식
                _name = input_list[1].strip() 
                return _name
            except ValueError:
                return None
            
        input_string = ctx.message.content
        name = parse_schedule_input(input_string) 
        
        if not name:
            embed = discord.Embed(
                title="입력을 확인하여주십시오",
                description='예시) !일정 삭제 "2023-10-20 20"\n',
                color=0x3498db
            )
            await ctx.send(embed=embed)
            return
        
        is_deleted = self.events.delete(name)

        if is_deleted:
            embed = discord.Embed(
                title=f"{name} 일정이 삭제되었습니다",
                color=0x3498db
            )
        else:
            embed = discord.Embed(
                title=f"{name} 일정이 삭제되지 못하였습니다",
                description="정확히 입력하였는지 확인하십시오",
                color=0x3498db
            ) 
        await ctx.send(embed=embed) 
        
    @schedule.command(name="저장")
    async def save_schedule(self, ctx):
        self.events.save()
        await ctx.send("저장되었습니다!")
        
    @schedule.command(name="확인")
    async def show_schedule(self, ctx):
        '''일정을 나열하는 커팬드'''        # TODO 출력 디자인 개선 
        events = self.events.get_events()
        description = "날짜:이름:내용:할당\n"
        for event in events:
            description += f'{event.date.strftime("%Y-%m-%d %H")}:{event.name}:{event.content}:{event.assigned}\n'
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
    
    @tasks.loop(minutes=1)
    async def check_schedule_launcher(self):
        """하루의 매 시간, 즉 분침이 0일 때 일정을 확인하기 위해 분침이 0일 때 실행하고 종료"""
        now = datetime.now()  
        if now.minute == 0:
            self.check_schedule.start() 
            self.check_schedule_launcher.stop()
    
    @tasks.loop(minutes=60)
    # @tasks.loop(minutes=1)
    async def check_schedule(self):
        '''일정이 지났는지 확인하여 지난 일정을 채널에 표시'''
        now = datetime.now()
        
        # 현재 시간을 기준으로 일정이 지난 리스트들을 확인하고 삭제
        while True:
            event = self.events.get_head()
            if not event is None and now > event.date:    # 일정이 지남
                description = f"{event.content}"
                if not event.is_assignment():     # 과제 할당 여부 
                    description += f"\n{event.assigned}에게 할당됨"
                embed = discord.Embed(
                    title=f"일정: {event.name}",
                    description=description,
                    color=0x3498db
                )
                
                channel = self.bot.get_channel(Settings.load('channel'))
                if not channel is None:        # TODO 채널이 할당되지 않았다면 출력하지 못함...
                    await channel.send(embed=embed)

                event = self.events.pop() # 지난 일정 삭제 
            else: 
                break 
        
    