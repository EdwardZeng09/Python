import unittest
from container import PriorityQueue
from event import create_event_list, PassengerRequest, DriverRequest, Pickup, Dropoff, Cancellation
from passenger import Passenger, WAITING, CANCELLED, SATISFIED
from location import Location, deserialize_location


class TestPriorityQueue(unittest.TestCase):

    def test_add(self):
        q = PriorityQueue()
        q.add(3)
        q.add(1)
        q.add(4)
        q.add(2)

        self.assertEqual(q.remove(), 1, 'add错误')
        self.assertEqual(q.remove(), 2, 'add错误')
        self.assertEqual(q.remove(), 3, 'add错误')
        self.assertEqual(q.remove(), 4, 'add错误')

    def test_same(self):
        q = PriorityQueue()
        o1 = Location(1,1)
        d1 = Location(2,2)
        p1 = Passenger('1', 2, o1, d1)
        o2 = Location(1,1)
        d2 = Location(2,2)
        p2 = Passenger('2', 2, o2, d2)
        e1 = PassengerRequest(0, p1)
        e2 = PassengerRequest(0, p1)
        q.add(e2)
        q.add(e1)
        print(e2)
        print(e1)
        print(q._items)
        self.assertEqual(q.remove(), e2, 'add错误')
        self.assertEqual(q.remove(), e1, 'add错误')


if __name__ == '__main__':
    unittest.main()
