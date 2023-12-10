import heapq 
import logging 
from datetime import datetime 
from settings import Settings

class Event:
    '''이벤트의 정보를 저장하는 클래스'''
    def __init__(self, date:datetime, name:str, content:str, assigned=""):
        self.date = date
        self.name = name
        self.content = content
        
        # assigned가 ""가 아니라면 이 이벤트는 과제이고 is_assignment를 통해 여부를 반환받는다. 
        self.assigned = assigned    
        
    def is_assignment(self):
        return self.assigned == ""
            
    @staticmethod
    def check_date(date): 
        '''입력된 날짜가 유효한지 확인'''
        try:
            datetime.strptime(date, "%Y-%m-%d %H")
        except ValueError: 
            return False
        return True 

        
class Events:
    """이벤트들을 딕셔너리와 힙을 사용해 관리하는 클래스"""
    
    def __init__(self, key, load=True):  # load: events.csv에서 스케줄을 읽어들일 것인지 여부
        self.heap = []
        self.dict = {}
        
        if load:    # 저장된 파일이 이미 있다면 로드
            self.load(key)
    
    def push(self, date:str, name:str, content="", assigned=""):
        '''입력된 이벤트 날짜, 이름, 내용, 할당으로 새 이벤트를 삽입'''
        event = Event(
            date=datetime.strptime(date, "%Y-%m-%d %H"),   # str를 datetime 객체로 변환
            name=name,
            content=content, 
            assigned=assigned
        )
        key = event.date.timestamp()
        self.dict[key] = event
        heapq.heappush(self.heap, key)

    def pop(self) -> Event:
        '''Head를 반환 및 삭제'''
        head_key = heapq.heappop(self.heap) 
        head = self.dict[head_key]
        del self.dict[head_key]
        return head
    
    def get_head(self):
        '''가장 이른 이벤트를 반환합니다'''
        if len(self.heap) > 0:
            return self.dict[self.heap[0]]
        return None
    
    def delete(self, name:str) -> bool:
        '''매개된 이름과 같은 이벤트를 삭제. 성공시 True 실패시 False''' 
        is_deleted = False
        for index, key in enumerate(self.heap):
            if self.dict[key].name == name:
                del self.heap[index]
                del self.dict[key]
                is_deleted = True

        if is_deleted:
            heapq.heapify(self.heap) 

        logging.info(self.heap)
        return is_deleted
    
    def get_events(self)  -> list[Event]:
        '''이벤트들을 정렬된 상태로 반환'''
        sorted_events = []
        _heap = self.heap.copy()
        
        while _heap:
            tmp = heapq.heappop(_heap)
            sorted_events.append(self.dict[tmp])
        
        return sorted_events
    
    def save(self, key):
        '''이벤트들을 정렬하여 csv 파일로 저장'''
        events = []
        for timestamp in self.heap:
            events.append(self.dict[timestamp])
            
        Settings.save(key, events) 
    
    def load(self, key):
        '''파일에서 정렬된 이벤트들을 읽어들여 heapify하고 저장'''
        # 기존 데이터 비우기
        self.dict = {}
        self.heap = []
        
        schedules: list = Settings.load(key)
        if schedules is None:
            return 
        
        for e in schedules:
            date = datetime.strptime(e[0], "%Y-%m-%d %H")
            timestamp = date.timestamp()        # key

            self.dict[timestamp] = Event(
                datetime.strptime(e[0], '%Y-%m-%d %H'), 
                e[1],
                e[2],
                e[3]
            )
            self.heap.append(timestamp)
            
        heapq.heapify(self.heap)