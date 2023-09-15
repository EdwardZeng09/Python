import unittest
from passenger import Passenger, WAITING
from location import Location


class TestRider(unittest.TestCase):

    def test_init(self):
        origin = Location(1, 2)
        destination = Location(3, 5)

        passenger = Passenger("id", 5, origin, destination)

        self.assertEqual(passenger.id, "id", '初始化失败-id')
        self.assertEqual(passenger.patience, 5, '初始化失败-patience')
        self.assertEqual(passenger.origin == origin, True, '初始化失败-origin')
        self.assertEqual(passenger.destination == destination, True, '初始化失败-destination')
        self.assertEqual(passenger.status, WAITING, '初始化失败-status')


if __name__ == '__main__':
    unittest.main()
