import unittest
from monitor import Monitor, PASSENGER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF
from location import Location


class TestEvent(unittest.TestCase):
    def test_average_total_distance(self):
        monitor = Monitor()
        monitor._average_total_distance()
        self.assertEqual(monitor._average_total_distance(), 0.0, '司机人数为0')

        monitor.notify(0, DRIVER, REQUEST,
                       "id1", Location(1,1))

        self.assertEqual(monitor._average_total_distance(), 0.0,
                         '司机人数为1,行驶距离为0')

        monitor.notify(0, DRIVER, REQUEST,
                       "id2", Location(2,2))

        monitor.notify(0, DRIVER, REQUEST,
                       "id3", Location(3,3))

        monitor.notify(0, DRIVER, REQUEST,
                       "id4", Location(4,4))

        self.assertEqual(monitor._average_total_distance(), 0.0,
                         '司机人数为4,行驶距离为0')

        monitor.notify(0, DRIVER, PICKUP,
                       "id1", Location(1,1))

        monitor.notify(0, DRIVER, REQUEST,
                       "id1", Location(1,1))

        monitor.notify(0, DRIVER, PICKUP,
                       "id2", Location(3,2))

        monitor.notify(0, DRIVER, REQUEST,
                       "id2", Location(3,2))

        monitor.notify(0, DRIVER, PICKUP,
                       "id3", Location(3,2))

        monitor.notify(0, DRIVER, DROPOFF,
                       "id3", Location(3,6))

        monitor.notify(0, DRIVER, REQUEST,
                       "id3", Location(3,6))


        self.assertEqual(monitor._average_total_distance(), 1.5,
                         '司机人数为4,行驶距离为6')


    def test_average_ride_distance(self):
        monitor = Monitor()

        self.assertEqual(monitor._average_trip_distance(), 0.0, '司机人数为0')

        monitor.notify(0, DRIVER, REQUEST,
                       "id1", Location(1,1))

        self.assertEqual(monitor._average_trip_distance(), 0.0,
                         '司机人数为1,行驶距离为0')

        monitor.notify(0, DRIVER, REQUEST,
                       "id2", Location(2,2))

        monitor.notify(0, DRIVER, REQUEST,
                       "id3", Location(3,3))

        monitor.notify(0, DRIVER, REQUEST,
                       "id4", Location(4,4))

        self.assertEqual(monitor._average_trip_distance(), 0.0,
                         '司机人数为4,行驶距离为0')

        monitor.notify(0, DRIVER, PICKUP,
                       "id1", Location(1,1))

        monitor.notify(0, DRIVER, REQUEST,
                       "id1", Location(1,1))


        monitor.notify(0, DRIVER, PICKUP,
                       "id2", Location(3,2))

        monitor.notify(0, DRIVER, REQUEST,
                       "id2", Location(3,2))

        self.assertEqual(monitor._average_trip_distance(), 0.0,
                         '司机人数为4,行驶距离为1,接送距离为0')

        monitor.notify(0, DRIVER, PICKUP,
                       "id3", Location(3,2))

        monitor.notify(0, DRIVER, DROPOFF,
                       "id3", Location(3,6))

        monitor.notify(0, DRIVER, REQUEST,
                       "id3", Location(3,6))


        self.assertEqual(monitor._average_trip_distance(), 1.0,
                         '司机人数为4,行驶距离为6,接送距离为4')




if __name__ == '__main__':
    unittest.main()
