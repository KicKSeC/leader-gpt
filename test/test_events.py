import os
import sys
from unittest import TestCase, main
from events import Events
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


def append():
    events = Events(load=False)

    events.push("2023-11-03 15", "회의 1", "프로젝트 일정 관리1")
    events.push("2023-11-06 22", "회의 3", "프로젝트 일정 관리3")
    events.push("2023-11-06 20", "회의 2", "프로젝트 일정 관리2")
    events.push("2023-12-01 12", "회의 5", "프로젝트 일정 관리5")
    events.push("2023-11-09 00", "회의 4", "프로젝트 일정 관리4")

    return events


class EventsTest(TestCase):
    def test_event(self):
        events = append()

        print([x.name for x in events.get_events()])
        self.assertEqual(events.pop().name, "회의 1")
        self.assertEqual(events.pop().name, "회의 2")
        self.assertEqual(events.pop().name, "회의 3")
        self.assertEqual(events.pop().name, "회의 4")
        self.assertEqual(events.pop().name, "회의 5")
        self.assertEqual(events.heap, [])

    def test_event_delete(self):
        events = append()
        events.push("2023-11-06 21", "회의 2", "중간 프로젝트")
        events.delete("회의 2")

        self.assertEqual(events.pop().name, "회의 1")
        self.assertEqual(events.pop().name, "회의 3")
        self.assertEqual(events.pop().name, "회의 4")
        self.assertEqual(events.pop().name, "회의 5")
        self.assertEqual(events.heap, [])


if __name__ == '__main__':
    main()
