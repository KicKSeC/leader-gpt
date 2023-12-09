import logging
import asyncio
from discord.ext import commands
from datetime import datetime
logging.basicConfig(filename='bot_command.log', level=logging.DEBUG,  # 로그 파일 설정
                    format='%(asctime)s:%(levelname)s:%(message)s')


class MeetingTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        #팀원이름, 날짜, 시간을 묶어서 저장하는 딕셔너리. (팀원이름: [{날짜: 시간}])
        self.memberDict = {}
         
        #최종 회의시간을 저장할 딕셔너리
        self.meetingTime = {}

     

    #memberDict 현황 확인용 - 추후 삭제(일반 사용자가 이용 X 개발자 확인용)
    @commands.command("멤버딕트")
    async def print_memberDict(self, ctx):
        await ctx.send(self.memberDict)
    #meetingTime 확인용 - 추후 삭제(일반 사용자가 이용 X 개발자 확인용)
    @commands.command("미팅타임")
    async def print_meetingTime(self, ctx):
        await ctx.send(self.meetingTime)

    #시간입력 날짜 시간 - 사용자의 별명(key)에 입력한 날짜, 시간을 저장.
    @commands.command("시간입력")
    async def add_schedule1(self, ctx, date, time):
        #입력하는 사용자의 디스코드 별명(채널 내의 별명)을 display_name에 저장
        display_name = ctx.author.display_name
        if display_name not in self.memberDict:
            self.memberDict[display_name] = {}
            #기존에 없는 팀원 추가 시, 메시지 출력
            await ctx.send(f"새로운 팀원 {display_name} 추가")

        if date not in self.memberDict[display_name]:
            self.memberDict[display_name][date] = []

        self.memberDict[display_name][date].append(time)
        await ctx.send(f"새로운 시간 {date} {time}이 입력되었습니다.")

    #시간입력 팀원이름 날짜 시간 - 팀원이름을 함께 입력하여 입력한 팀원이름(key)에 입력한 날짜, 시간을 저장
    @commands.command("팀원시간입력")
    async def add_schedule2(self, ctx, member_name, date, time):
        
        if member_name not in self.memberDict:
            self.memberDict[member_name] = {}
            #기존에 없는 팀원 추가 시, 메시지 출력
            await ctx.send(f"새로운 팀원 {member_name} 추가")

        if date not in self.memberDict[member_name]:
            self.memberDict[member_name][date] = []

        self.memberDict[member_name][date].append(time)
        await ctx.send(f"새로운 시간 {date} {time}이 입력되었습니다.")
        
    
    #전체 목록을 보여줌. 
    @commands.command(name='전체목록')
    async def print_dict(self, ctx):
        # 팀원 목록 출력
        member_names = ', '.join(self.memberDict.keys())
        await ctx.send(f"현재 팀원 목록: {member_names}")

        # 팀원별 시간 출력
        result_message = "팀원별 시간:\n"
        for member, schedules in self.memberDict.items():
            formatted_schedules = [f"{date}: {', '.join(times)}" for date, times in schedules.items()]
            result_message += f"{member}: {', '.join(formatted_schedules)}\n"

        await ctx.send(result_message)
    #현재 저장된 팀원의 목록을 확인
    @commands.command(name="팀원목록")
    async def member_list(self, ctx):
        member_names = list(self.memberDict.keys())
        await ctx.send(f"현재 팀원 목록: {', '.join(member_names)}") 
        
   
    #자신이 입력한 회의 가능 시간을 확인
    @commands.command(name="시간확인")
    async def check_member_time1(self, ctx):
        #입력하는 사용자의 디스코드 별명(채널 내의 별명)을 Name에 저장
        Name = ctx.author.display_name

        if Name not in self.memberDict:
            await ctx.send(f"{Name} 팀원은 등록되지 않았습니다.")
            return

        member_schedule = self.memberDict[Name]
        formatted_schedule = []

        for date, times in sorted(member_schedule.items()):
            times.sort()  # 시간이 빠른 순서대로 정렬
            formatted_times = ', '.join(times)
            formatted_schedule.append(f"{date}: {formatted_times}")

        result_message = f"{Name} 팀원의 저장된 시간:\n" + '\n'.join(formatted_schedule)
        await ctx.send(result_message)

    #팀원의 이름을 입력하여, 그 팀원의 회의 가능 시간을 확인
    @commands.command(name="팀원시간확인")
    async def check_member_schedule(self, ctx, Name):
        if Name not in self.memberDict:
            await ctx.send(f"{Name} 팀원은 등록되지 않았습니다.")
            return

        member_schedule = self.memberDict[Name]
        formatted_schedule = []

        for date, times in sorted(member_schedule.items()):
            times.sort()  # 시간이 빠른 순서대로 정렬
            formatted_times = ', '.join(times)
            formatted_schedule.append(f"{date}: {formatted_times}")

        result_message = f"{Name} 팀원의 저장된 시간:\n" + '\n'.join(formatted_schedule)
        await ctx.send(result_message)
        
    #입력된 시간들을 전부 삭제 - 회의시간을 결정 후 필요없는 정보들을 삭제 (memberDict를 빈 딕셔너리로 초기화)
    @commands.command(name="전체삭제")
    async def delete_memberDict(self, ctx):
        self.memberDict = {}
        self.meetingTime = {} #빈 딕셔너리로 초기화
        await ctx.send("입력된 시간 정보가 전부 삭제되었습니다.")

    #저장된 팀원의 정보를 삭제
    @commands.command(name="팀원삭제")
    async def delete_member(self, ctx, Name):
        if Name not in self.memberDict:
            await ctx.send(f"팀원 {Name}은(는) 존재하지 않습니다.")
            return

        del self.memberDict[Name]
        await ctx.send(f"팀원 {Name}이(가) 삭제되었습니다.")
        

    #입력한 시간 중, 삭제하고자 하는 시간을 삭제(날짜 시간 입력)
    @commands.command(name="시간삭제")
    async def delete_member_time1(self, ctx, inputDate, inputTime):
        Name = ctx.author.display_name
        if Name not in self.memberDict:
            await ctx.send(f"팀원 {Name}은(는) 존재하지 않습니다.")
            return

        if inputDate in self.memberDict[Name]:
            if inputTime in self.memberDict[Name][inputDate]:
                self.memberDict[Name][inputDate].remove(inputTime)
                if not self.memberDict[Name][inputDate]:  # Check if the list is empty
                    del self.memberDict[Name][inputDate]  # Remove the date if no times are left
                await ctx.send(f"{inputDate} {inputTime} 삭제 완료.")
            elif inputTime == None:
                del self.memberDict[Name][inputDate]
            else:
                await ctx.send(f"{inputDate} 날짜에 {inputTime}은(는) 존재하지 않습니다.")
        else:
            await ctx.send(f"{inputDate} 날짜는 존재하지 않습니다.")    
     
    #팀원을 지정하여, 그 팀원의 시간 중 삭제하고자 하는 부분을 삭제(팀원이름 날짜 시간 입력)
    @commands.command(name="팀원시간삭제")
    async def delete_member_time2(self, ctx, Name: str, inputDate, inputTime):
        if Name not in self.memberDict:
            await ctx.send(f"팀원 {Name}은(는) 존재하지 않습니다.")
            return

        if inputDate in self.memberDict[Name]:
            if inputTime in self.memberDict[Name][inputDate]:
                self.memberDict[Name][inputDate].remove(inputTime)
                if not self.memberDict[Name][inputDate]:  # Check if the list is empty
                    del self.memberDict[Name][inputDate]  # Remove the date if no times are left
                await ctx.send(f"{inputDate} {inputTime} 삭제 완료.")
            elif inputTime == None:
                del self.memberDict[Name][inputDate]
            else:
                await ctx.send(f"{inputDate} 날짜에 {inputTime}은(는) 존재하지 않습니다.")
        else:
            await ctx.send(f"{inputDate} 날짜는 존재하지 않습니다.")


    #!회의시간결정 -현재 저장된 팀원들의 시간을 비교하여 회의시간을 결정
    @commands.command(name="회의시간결정")
    async def decide_meeting_time(self, ctx):
        if len(self.memberDict) < 2:
            await ctx.send("팀원이 부족하여 회의 시간을 결정할 수 없습니다.")
            return

        # 빈 딕셔너리를 모두 제거한 새로운 딕셔너리 리스트
        new_dict_list = [d for d in self.memberDict.values() if d]
        overlap_dict = {}  # 초기화 필요

        async def find_overlap_times(dict1, dict2):
            overlap_dict = {}

            for date, times1 in dict1.items():
                if date in dict2:
                    overlap_dict[date] = overlap_dict.get(date, [])

                    for time1 in times1:
                        for time2 in dict2[date]:
                            start_time1, end_time1 = map(lambda x: x.strip(), time1.split('~'))
                            start_time2, end_time2 = map(lambda x: x.strip(), time2.split('~'))

                            end_time1 = '00:00' if end_time1 == '24:00' else end_time1
                            end_time2 = '00:00' if end_time2 == '24:00' else end_time2

                            start1 = datetime.strptime(start_time1, "%H:%M")
                            end1 = datetime.strptime(end_time1, "%H:%M")
                            start2 = datetime.strptime(start_time2, "%H:%M")
                            end2 = datetime.strptime(end_time2, "%H:%M")

                            if start1 <= end2 and start2 <= end1:
                                overlapping_start = max(start1, start2)
                                overlapping_end = min(end1, end2)
                                overlap_dict[date].append(f"{overlapping_start.strftime('%H:%M')}~{overlapping_end.strftime('%H:%M')}")

            return overlap_dict

        for i in range(len(new_dict_list) - 1):
            dict1 = new_dict_list[i]
            dict2 = new_dict_list[i + 1]

            overlap_dict = await find_overlap_times(dict1, dict2)
            new_dict_list[i + 1] = overlap_dict

        self.meetingTime = overlap_dict
        
       # 사용자에게 보내는 메시지 형식 변경
        result_message = "회의가능한 시간:\n"
        for date, times in self.meetingTime.items():
            formatted_times = ', '.join(times)
            result_message += f"{date}: {formatted_times}\n"
        if result_message == "회의가능한 시간:\n":
            result_message = "회의가능한 시간이 없습니다."
        
        await ctx.send(result_message)

    #정해진 회의시간들 중, 하나를 선택하여 최종 회의 시간을 결정한다. 최종 회의 시간이 정해지면, 남아있던 회의 가능 시간들은 삭제된다.
    @commands.command(name='회의시간선택')
    async def final_decision_meeting_time(self, ctx):
        if not self.meetingTime:
            await ctx.send("현재 정해진 회의 시간이 없습니다.")
            return

        # 정해진 회의 시간 목록 출력
        meeting_time_list = [f"({i + 1}). {date} {time}" for i, (date, times) in enumerate(self.meetingTime.items()) for time in times]
        meeting_time_message = '\n'.join(meeting_time_list)
        await ctx.send("정해진 회의 시간 목록:\n" + meeting_time_message)

        # 사용자에게 번호 입력 받기
        await ctx.send("원하는 회의 시간의 번호를 입력하세요:")
        try:
            # 사용자 입력 대기 (타임아웃은 60초)
            user_response = await self.bot.wait_for("message", timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
            choice = int(user_response.content)

            # 선택한 회의 시간 가져오기
            selected_meeting_time = list(self.meetingTime.keys())[choice - 1]
            selected_time_range = self.meetingTime[selected_meeting_time]

            # 공지 메시지 생성
            announcement_message = f"회의 시간이 최종 확정되었습니다!\n선택한 회의 시간: {selected_meeting_time} {', '.join(selected_time_range)}"

            # 공지 메시지 전송
            await ctx.send(announcement_message)

            # meetingTime 초기화
            self.meetingTime = {}

        except ValueError:
            await ctx.send("올바른 숫자를 입력하세요.")
        except IndexError:
            await ctx.send("유효한 범위의 번호를 입력하세요.")
        except asyncio.TimeoutError:
            await ctx.send("시간이 초과되었습니다. 명령어를 다시 입력하세요.")

   