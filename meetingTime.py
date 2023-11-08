from datetime import datetime

inputTime = {}
#날짜와 시간을 inputStr 딕셔너리에 저장.
START_MESSAGE = "일정을 구하기 위한 시간을 입력받습니다."
END_MESSAGE = "일정을 입력받았습니다."

print("가능한 날짜와 시간을 입력하세요: ex) 11/5 12:00~15:00\n")
while True:
    user_input = input()
    if user_input == 'q':
        break
    date, time = user_input.split(" ")
    if date not in inputTime:
        inputTime[date] = []
    inputTime[date].append(time)


print(inputTime)

#시간대가 2개 이상으로, 비교할 시간대가 있는 날짜와 그 날짜의 시간대들을 추출하여 filterTime 딕셔너리에 저장.
filterTime = {}

for key, value in inputTime.items():
    if len(value) != 1:
        filterTime[key] = value
   

#가능한 날짜와 시간을 meetTime에 저장.
meetTime = {}
for date, times in filterTime.items():
    overlapping_times = []
    for i in range(len(times)):
        for j in range(i + 1, len(times)):
            time1_start, time1_end = times[i].split("~")
            time2_start, time2_end = times[j].split("~")
            
            time1_start, time1_end = datetime.strptime(time1_start, "%H:%M"), datetime.strptime(time1_end, "%H:%M")
            time2_start, time2_end = datetime.strptime(time2_start, "%H:%M"), datetime.strptime(time2_end, "%H:%M")
            
            if time1_start <= time2_end and time2_start <= time1_end:
                # 시간대가 겹치는 경우
                start_time = max(time1_start, time2_start)
                end_time = min(time1_end, time2_end)
                overlapping_times.append(f"{start_time.strftime('%H:%M')}~{end_time.strftime('%H:%M')}")

    if overlapping_times:
        meetTime[date] = overlapping_times

# print(meetTime)

print("가능한 날짜와 시간 ")
for date, times in meetTime.items():
    print(date, "and".join(times))
