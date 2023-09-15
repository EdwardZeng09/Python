import unittest
from passenger import Passenger, WAITING, CANCELLED, SATISFIED
from dispatcher import Dispatcher
from driver import Driver
from location import Location, deserialize_location
from monitor import Monitor, PASSENGER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF
from event import DriverRequest, PassengerRequest, Cancellation, Pickup, Dropoff, create_event_list


class TestEvent(unittest.TestCase):
    def test_DriverRequest_no_passenger(self):
        location = Location(1, 2)
        driver1 = Driver("d1", location, 1)

        # 无乘客
        dispatcher = Dispatcher()
        monitor = Monitor()

        event = DriverRequest(0, driver1)
        next_events = event.do(dispatcher, monitor)
        actual = (driver1.is_idle, driver1._destination)
        expect = (True, None)
        self.assertEqual(actual, expect, 'DriverRequest-do错误-无乘客时，不改变')
        self.assertEqual(next_events, [],
                         'DriverRequest-do错误-无乘客时，不产生后续事件')

        # 信息记录
        activity = monitor._activities[DRIVER]["d1"][0]
        actual = (activity.time, activity.description,
                  activity.id, activity.location)
        expect = (0, REQUEST, "d1", location)
        self.assertEqual(actual, expect, 'DriverRequest-do错误-信息记录错误')

        d = monitor._activities[PASSENGER]
        self.assertEqual(d, {}, 'DriverRequest-do错误-DriverRequest不记录乘客')


    def test_DriverRequest_has_passenger(self):

        location = Location(1, 2)
        driver1 = Driver("d1", location, 1)

        origin = Location(3, 2)
        destination = Location(3, 5)
        passenger1 = Passenger("r1", 5, origin, destination)


        #添加乘客
        dispatcher = Dispatcher()
        monitor = Monitor()
        dispatcher.request_driver(passenger1)

        event = DriverRequest(0, driver1)
        next_events = event.do(dispatcher, monitor)

        actual = (driver1.is_idle, driver1._destination)
        expect = (False, passenger1.origin)
        self.assertEqual(actual, expect, 'DriverRequest-do错误-有乘客时，改变状态')

        self.assertEqual(isinstance(next_events,list), True,
                         'DriverRequest-do错误-必须返回list of Event')
        self.assertEqual(len(next_events), 1,
                         'DriverRequest-do错误-有乘客时，只产生后续pickup事件[1]')
        self.assertEqual(isinstance(next_events[0], Pickup), True,
                         'DriverRequest-do错误-有乘客时，只产生后续pickup事件[2]')

        actual = (next_events[0].timestamp, next_events[0].driver,
                  next_events[0].passenger)
        expect = (2, driver1, passenger1)
        self.assertEqual(actual, expect, 'DriverRequest-do错误-生成事件错误')

        # 信息记录
        activity = monitor._activities[DRIVER]["d1"][0]
        actual = (activity.time, activity.description,
                  activity.id, activity.location)
        expect = (0, REQUEST, "d1", location)
        self.assertEqual(actual, expect, 'DriverRequest-do错误-信息记录错误')

        d = monitor._activities[PASSENGER]
        self.assertEqual(d, {}, 'DriverRequest-do错误-DriverRequest不记录乘客')


    def test_Cancellation_success(self):
        dispatcher = Dispatcher()
        monitor = Monitor()

        origin = Location(3, 2)
        destination = Location(3, 5)
        passenger1 = Passenger("r1", 5, origin, destination)

        dispatcher._waiting_passengers = [passenger1]

        event = Cancellation(0, passenger1)
        next_events = event.do(dispatcher, monitor)

        self.assertEqual(passenger1.status, CANCELLED,
                         'Cancellation-do错误：cancel成功，乘客状态需要改变')
        self.assertEqual(dispatcher._waiting_passengers, [],
                         'Cancellation-do错误：cancel成功，乘客从等待列表移除')

        self.assertEqual(next_events, [], 'Cancellation-do错误: 不产生后续事件')

        # 信息记录
        activity = monitor._activities[PASSENGER]["r1"][0]
        actual = (activity.time, activity.description,
                  activity.id, activity.location)
        expect = (0, CANCEL, "r1", origin)
        self.assertEqual(actual, expect, 'Cancellation-do错误-信息记录错误')

        d = monitor._activities[DRIVER]
        self.assertEqual(d, {}, 'Cancellation-do错误-Cancel不记录司机')


    def test_Cancellation_fail(self):
        dispatcher = Dispatcher()
        monitor = Monitor()

        origin = Location(3, 2)
        destination = Location(3, 5)
        passenger1 = Passenger("r1", 5, origin, destination)
        passenger1.status = SATISFIED

        event = Cancellation(0,passenger1)
        next_events = event.do(dispatcher, monitor)
        self.assertEqual(passenger1.status, SATISFIED,
                         'Cancellation-do错误:cancel失败，乘客状态不改变')
        self.assertEqual(next_events, [], 'Cancellation-do错误: 不产生后续事件')

        # 信息记录 ---- 没有记录
        d = monitor._activities[PASSENGER]
        self.assertEqual(d, {}, 'Cancellation-do错误-Cancel失败不用记录乘客')

        d = monitor._activities[DRIVER]
        self.assertEqual(d, {}, 'Cancellation-do错误-Cancel不记录司机')


    def test_Pickup_success(self):
        dispatcher = Dispatcher()
        monitor = Monitor()

        location = Location(1, 2)
        driver1 = Driver("d1", location, 1)

        origin = Location(3, 2)
        destination = Location(3, 5)
        passenger1 = Passenger("r1", 5, origin, destination)

        driver1.start_drive(passenger1.origin)

        event = Pickup(0, passenger1, driver1)

        next_events = event.do(dispatcher, monitor)

        actual = (driver1.is_idle, driver1._destination, driver1.location)
        expect = (False, passenger1.destination, passenger1.origin)
        self.assertEqual(actual, expect,
                         'Pickup-do错误-puckup执行后，必须刷新driver的信息')

        self.assertEqual(passenger1.status, SATISFIED,
                         'Pickup-do错误-成功时，改变乘客的状态')

        self.assertEqual(isinstance(next_events,list), True,
                         'Pickup-do错误-必须返回list of Event')
        self.assertEqual(len(next_events), 1,
                         'Pickup-do错误-成功时，只产生一个后续事件')
        self.assertEqual(isinstance(next_events[0], Dropoff), True,
                         'Pickup-do错误-成功时，只产生后续drop off事件')

        dropoff = next_events[0]
        actual = (dropoff.timestamp, dropoff.driver)
        expect = (3, driver1)
        self.assertEqual(actual, expect, 'Pickup-do错误-生成事件的信息错误')

        # 信息记录
        activity = monitor._activities[PASSENGER]["r1"][0]
        actual = (activity.time, activity.description,
                  activity.id, activity.location)
        expect = (0, PICKUP, "r1", origin)
        self.assertEqual(actual, expect, 'Pickup-do错误-信息记录错误[乘客]')


        activity = monitor._activities[DRIVER]["d1"][0]
        actual = (activity.time, activity.description,
                  activity.id, activity.location)
        expect = (0, PICKUP, "d1", origin)
        self.assertEqual(actual, expect, 'Pickup-do错误-信息记录错误[司机]')




    def test_Pickup_fail(self):
        dispatcher = Dispatcher()
        monitor = Monitor()

        location = Location(1, 2)
        driver1 = Driver("d1", location, 1)

        origin = Location(3, 2)
        destination = Location(3, 5)
        passenger1 = Passenger("r1",5,origin,destination)

        driver1.start_drive(passenger1.origin)
        passenger1.status = CANCELLED

        event = Pickup(0, passenger1, driver1)
        next_events = event.do(dispatcher, monitor)

        actual = (driver1.is_idle, driver1._destination, driver1.location)
        expect = (True, None, passenger1.origin)
        self.assertEqual(actual, expect,
                         'Pickup-do错误-puckup执行后，必须刷新driver的信息')

        self.assertEqual(passenger1.status, CANCELLED,
                         'Pickup-do错误-失败时，不改变乘客的状态')

        self.assertEqual(isinstance(next_events,list), True,
                         'Pickup-do错误-必须返回list of Event')
        self.assertEqual(len(next_events), 1,
                         'Pickup-do错误-失败时，只产生一个后续事件')
        self.assertEqual(isinstance(next_events[0], DriverRequest), True,
                         'Pickup-do错误-失败时，只产生后续DriverRequest事件')

        request = next_events[0]
        actual = (request.timestamp, request.driver)
        expect = (0, driver1)
        self.assertEqual(actual, expect, 'Pickup-do错误-生成事件的信息错误')


        # 信息记录 ---- 乘客没有记录， 司机依然记录
        d = monitor._activities[PASSENGER]
        self.assertEqual(d, {}, 'Pickup-do错误-Pickup失败不用记录乘客')

        activity = monitor._activities[DRIVER]["d1"][0]
        actual = (activity.time, activity.description,
                  activity.id, activity.location)
        expect = (0, REQUEST, "d1", origin)
        self.assertEqual(actual, expect, 'Pickup-do错误-信息记录错误[司机]')



    def test_Dropoff(self):
        dispatcher = Dispatcher()
        monitor = Monitor()

        location = Location(1, 2)
        driver1 = Driver("d1", location, 1)

        origin = Location(3, 2)
        destination = Location(3, 5)
        passenger1 = Passenger("r1",5,origin,destination)

        driver1.start_drive(origin)
        driver1.end_drive()
        driver1.start_trip(passenger1)
        passenger1.status = SATISFIED

        event = Dropoff(5, driver1)
        next_events = event.do(dispatcher, monitor)

        actual = (driver1.is_idle, driver1._destination, driver1._passenger, driver1.location)
        expect = (True, None, None, passenger1.destination)
        self.assertEqual(actual, expect,
                         'Dropoff-do错误: 必须刷新driver的信息')
        self.assertEqual(passenger1.status, SATISFIED,
                         'Dropoff-do错误: 不改变乘客的状态')

        self.assertEqual(isinstance(next_events, list), True,
                         'Dropoff-do错误-必须返回list of Event')
        self.assertEqual(len(next_events), 1,
                         'Dropoff-do错误-产生一个后续事件')
        self.assertEqual(isinstance(next_events[0], DriverRequest), True,
                         'Dropoff-do错误-只产生后续DriverRequest事件')

        request = next_events[0]
        actual = (request.timestamp, request.driver)
        expect = (5, driver1)
        self.assertEqual(actual, expect, 'Dropoff-do错误-生成事件的信息错误')


        # 信息记录
        activity = monitor._activities[DRIVER]["d1"][0]
        actual = (activity.time, activity.description,
                  activity.id, activity.location)
        expect = (5, DROPOFF, "d1", destination)
        self.assertEqual(actual, expect, 'Dropoff-do错误-信息记录错误[司机]')

        # 乘客没有记录
        d = monitor._activities[PASSENGER]
        self.assertEqual(d, {}, 'Dropoff-do错误-Dropoff不用记录乘客')



    def test_create_event_list(self):
        events = create_event_list("test_events.txt")
        events.sort()


        self.assertEqual(isinstance(events[0],DriverRequest), True, '数据读取错误-没有生成 DriverRequest1')
        self.assertEqual(isinstance(events[1],DriverRequest), True, '数据读取错误-没有生成 DriverRequest2')
        self.assertEqual(isinstance(events[2],PassengerRequest), True, '数据读取错误-没有生成 RiderRequest1')
        self.assertEqual(isinstance(events[3],PassengerRequest), True, '数据读取错误-没有生成 RiderRequest2')

        self.assertEqual(events[2].timestamp, 20, '数据读取错误-时间读取错误')

        driver1 = events[0].driver
        driver2 = events[1].driver

        passenger1 = events[2].passenger
        passenger2 = events[3].passenger

        b = isinstance(driver1, Driver) and isinstance(driver2, Driver) and \
            isinstance(passenger1, Passenger) and isinstance(passenger2, Passenger)
        self.assertEqual(b, True, '数据读取错误-未生成对象 或对象类型不正确')

        self.assertEqual(driver1.id, "d1", '数据读取错误-生成Driver 信息错误-id')
        self.assertEqual(driver2.location, Location(3,4), '数据读取错误-生成Driver 信息错误-location')
        self.assertEqual(passenger1.id, "r1", '数据读取错误-生成Rider 信息错误-id')
        self.assertEqual(passenger1.origin, Location(3,4), '数据读取错误-生成Rider 信息错误-origin')
        self.assertEqual(passenger2.destination, Location(2,5), '数据读取错误-生成Rider 信息错误-destination')
        self.assertEqual(passenger2.patience, 10, '数据读取错误-生成Rider 信息错误-patience')





if __name__ == '__main__':
    unittest.main()
