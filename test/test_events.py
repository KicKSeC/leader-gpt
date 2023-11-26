from unittest import TestCase, main
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from events import Events


class EventsTest(TestCase):
    def test_event(self):
        events = Events() 

        events.push("회의 1", "2023-11-03", "프로젝트 일정 관리1")
        events.push("회의 3", "2023-11-06", "프로젝트 일정 관리3")
        events.push("회의 2", "2023-11-05", "프로젝트 일정 관리2")
        events.push("회의 5", "2023-12-01", "프로젝트 일정 관리5")
        events.push("회의 4", "2023-11-09", "프로젝트 일정 관리4")

        print([x.name for x in events.get_events()])
        self.assertEqual(events.pop().name, "회의 1")
        self.assertEqual(events.pop().name, "회의 2")
        self.assertEqual(events.pop().name, "회의 3")
        self.assertEqual(events.pop().name, "회의 4")
        self.assertEqual(events.pop().name, "회의 5")
        self.assertEqual(events.heap, [])

if __name__ == '__main__':
    main()