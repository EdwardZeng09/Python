import unittest
from driver import Driver
from passenger import Passenger
from location import Location
from dispatcher import Dispatcher



class TestDispatcher(unittest.TestCase):

    def test_request_driver(self):
        dispatcher = Dispatcher()

        location = Location(1, 2)
        driver1 = Driver("d1", location, 1)

        location = Location(1, 2)
        driver2 = Driver("d2", location, 3)

        location = Location(3, 2)
        driver3 = Driver("d3", location, 3)

        origin = Location(3, 2)
        destination = Location(3, 5)
        passenger1 = Passenger("r1", 5, origin, destination)

        origin = Location(2, 2)
        destination = Location(3, 5)
        passenger2 = Passenger("r2", 5, origin, destination)

        origin = Location(10, 2)
        destination = Location(3, 5)
        passenger3 = Passenger("r3", 5, origin, destination)

        origin = Location(10, 2)
        destination = Location(3, 5)
        passenger4 = Passenger("r4", 5, origin, destination)

        # 没有司机
        get_driver = dispatcher.request_driver(passenger1)
        self.assertEqual(get_driver, None, '请求司机错误-无司机可用[1]')
        self.assertEqual(passenger1 in dispatcher._waiting_passengers, True,
                         '请求司机错误-未分配的乘客，应加入等待列表')

        #添加司机
        dispatcher._drivers = {"d1" : driver1, "d2" : driver2, "d3" : driver3}
        dispatcher._waiting_passengers = []

        # 距离为0
        get_driver = dispatcher.request_driver(passenger1)
        self.assertEqual(get_driver, driver3, '请求司机错误-筛选司机方式不正确[1]')
        get_driver.start_drive(passenger1.origin)

        # 抵达时间更短的司机
        get_driver = dispatcher.request_driver(passenger2)
        self.assertEqual(get_driver, driver2, '请求司机错误-筛选司机方式不正确[2]')
        get_driver.start_drive(passenger2.origin)

        # 只剩一个
        get_driver = dispatcher.request_driver(passenger3)
        self.assertEqual(get_driver, driver1, '请求司机错误-筛选司机方式不正确[3]')
        get_driver.start_drive(passenger3.origin)

        # 没有空闲的司机
        get_driver = dispatcher.request_driver(passenger4)
        self.assertEqual(get_driver, None, '请求司机错误-无可用司机[2]')
        self.assertEqual(passenger4 in dispatcher._waiting_passengers, True,
                         '请求司机错误-未分配的乘客，应加入等待列表')



    def test_request_passenger(self):
        dispatcher = Dispatcher()

        location = Location(1, 2)
        driver1 = Driver("d1", location, 1)

        location = Location(1, 2)
        driver2 = Driver("d2", location, 3)

        location = Location(3, 2)
        driver3 = Driver("d3", location, 3)

        origin = Location(0, 2)
        destination = Location(3, 5)
        passenger1 = Passenger("r1",5,origin,destination)

        origin = Location(4, 2)
        destination = Location(3, 5)
        passenger2 = Passenger("r2",5,origin,destination)

        # 没有乘客
        get_passenger = dispatcher.request_passenger(driver1)
        self.assertEqual(get_passenger, None, '请求乘客错误-没有等待的乘客[1]')
        self.assertEqual(driver1.id in dispatcher._drivers, True,
                         '请求乘客错误-新司机需要添加进车队字典')

        #添加乘客
        dispatcher._waiting_passengers = [passenger1, passenger2]

        #分配等待更久的乘车---list里更靠前的乘客
        get_passenger = dispatcher.request_passenger(driver1)
        self.assertEqual(get_passenger, passenger1, '请求乘客错误-乘客分配错误[1]')
        self.assertEqual(passenger1 in dispatcher._waiting_passengers, False,
                         '请求乘客错误-乘客被分配，应从列表移除')

        # 分配乘客 ---- 只有一个
        get_passenger = dispatcher.request_passenger(driver2)
        self.assertEqual(get_passenger, passenger2, '请求乘客错误-乘客分配错误[2]')
        self.assertEqual(driver2.id in dispatcher._drivers, True,
                         '请求乘客错误-新司机需要添加进车队字典')
        self.assertEqual(passenger2 in dispatcher._waiting_passengers, False,
                         '请求乘客错误-乘客被分配，应从列表移除')

        # 乘客列表清空
        get_passenger = dispatcher.request_passenger(driver3)
        self.assertEqual(get_passenger, None, '请求乘客错误-没有等待的乘客[2]')
        self.assertEqual(driver3.id in dispatcher._drivers, True,
                         '请求乘客错误-新司机需要添加进车队字典')

    def test_cancel_ride(self):

        dispatcher = Dispatcher()

        origin = Location(3, 2)
        destination = Location(3, 5)
        passenger1 = Passenger("r1",5,origin,destination)

        origin = Location(1, 2)
        destination = Location(3, 5)
        passenger2 = Passenger("r2",5,origin,destination)


        # 乘客2放入等待列表
        dispatcher.request_driver(passenger2)

        # 不在等待列表
        dispatcher.cancel_ride(passenger1)
        self.assertEqual([passenger2] == dispatcher._waiting_passengers,  True,
                         '乘客cancel错误-等待列表不发生变化')

        dispatcher.cancel_ride(passenger2)
        self.assertEqual(dispatcher._waiting_passengers, [],
                         '乘客cancel错误-waitlist移除指定乘客')

    def test_request_driver1(self):
        dispatcher = Dispatcher()
        pas = Passenger('1', 5, Location(1, 2), Location(3, 2))
        pas1 = Passenger('2', 5, Location(2, 2), Location(4, 2))
        pas2 = Passenger('3', 5, Location(4, 2), Location(5, 2))
        dr1 = Driver('1', Location(1, 2), 1)
        dr2 = Driver('2', Location(2, 2), 1)
        a = dispatcher.request_driver(pas1)
        assert a == None
        b = dispatcher.request_passenger(dr1)
        assert b == pas1
        dr1.start_drive(pas1.origin)
        c = dispatcher.request_passenger(dr2)
        assert c == None
        d = dispatcher.request_driver(pas)
        assert d == dr2
        dr2.start_drive(pas.origin)
        no = dispatcher.request_driver(pas2)
        assert no == None


if __name__ == '__main__':
    unittest.main()









