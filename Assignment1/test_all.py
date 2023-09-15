import unittest
from container import PriorityQueue
from dispatcher import Dispatcher
from simulation import Simulation
from passenger import Passenger, WAITING, CANCELLED, SATISFIED
from driver import Driver
from location import Location, deserialize_location,manhattan_distance
from monitor import Monitor, PASSENGER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF
from event import Event,DriverRequest, PassengerRequest, Cancellation, Pickup, Dropoff, create_event_list


class TestLocation(unittest.TestCase):

    def test_init(self):
        location = Location(1, 2)
        self.assertEqual(str(location), "(1, 2)", 'str格式错误 或 初始化失败')

        location2 = Location(2, 1)
        location3 = Location(1, 2)
        self.assertEqual(location == location3, True, 'eq 判断失败')
        self.assertEqual(location == location2, False, 'eq 判断失败')

    def test_manhattan_distance(self):
        location = Location(3, 5)
        location2 = Location(5, 3)
        location3 = Location(3, 5)

        self.assertEqual(manhattan_distance(location,location2), 4, 'location之间距离计算失败')
        self.assertEqual(manhattan_distance(location,location3), 0, 'location之间距离计算失败')

    def test_deserialize_location(self):
        location = Location(3, 5)
        location2 = deserialize_location("3,5")
        self.assertEqual(location == location2, True, '通过str生成location失败')



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


class TestDriver(unittest.TestCase):

    def test_init(self):
        location = Location(1, 2)
        driver = Driver("id", location, 3)

        self.assertEqual(driver.id, "id", '初始化失败-id')
        self.assertEqual(driver._speed, 3, '初始化失败-speed')
        self.assertEqual(driver.location, location, '初始化失败-location')

        self.assertEqual(driver.is_idle , True, '初始化失败-is_idle')
        self.assertEqual(driver._destination, None, '初始化失败-destination')
        self.assertEqual(driver._passenger, None, '初始化失败-passenger')

    def test_eq(self):

        location = Location(1, 2)
        driver1 = Driver("id1", location, 3)

        location = Location(1, 2)
        driver2 = Driver("id1", location, 3)

        location = Location(1, 2)
        driver3 = Driver("id2", location, 3)

        self.assertEqual(driver1 == driver2, True, '相等判断失败---判断id属性是否相等')
        self.assertEqual(driver1 == driver3, False, '相等判断失败')

    def test_str(self):
        location = Location(1, 2)
        driver = Driver("id", location, 3)

        self.assertEqual(driver.id in str(driver), True, 'str信息不全 ---id要在str中')

    def test_get_travel_time(self):

        location = Location(1, 2)
        driver1 = Driver("id1", location, 3)

        location1 = Location(4, 6)
        location2 = Location(5, 6)

        self.assertEqual(driver1.get_travel_time(location1), 2, '驾驶时间计算错误')
        self.assertEqual(driver1.get_travel_time(location2), 3, '驾驶时间计算错误')

        # 注意,我这里并没有讨论 2.5 是2还是3，是使用的round的结果。
        # 如果需要讨论，问教授对应的处理方式

        # Case: speed = 0
        # driver2 = Driver("id2", location, 0)
        # try:
        #     # 如果不用讨论0的情况，把这里注释掉即可。
        #     driver2.get_travel_time(location1)
        # except:
        #     s = '司机速度为0时的情况。我并不清楚如何处理，是否讨论。需要问教授。\n'
        #     s+= '如果不用讨论，则把这个case注释掉'
        #     raise AssertionError(s)


    def test_start_drive(self):
        location = Location(1, 2)
        driver = Driver("id1", location, 3)

        location1 = Location(4, 6)

        time = driver.start_drive(location1)
        self.assertEqual(time, 2, 'start-drive 返回值错误')
        self.assertEqual(driver._destination == location1, True, 'start-drive 需要设置目的地')
        self.assertEqual(driver.is_idle, False, 'start-drive 需要改变司机状态')
        self.assertEqual(driver.location, location, 'start-drive 不应改变location')

    def test_end_drive(self):
        location = Location(1, 2)
        driver = Driver("id1", location, 3)

        location1 = Location(4, 6)
        driver.start_drive(location1)

        driver.end_drive()
        self.assertEqual(driver.location == location1, True, 'end-drive 没有更新location')
        self.assertEqual(driver._destination, None, 'end-drive没有取消目的地')
        self.assertEqual(driver.is_idle, True, 'end-drive没有设置司机状态')

    def test_start_trip(self):
        location = Location(1, 2)
        driver = Driver("id1", location, 3)

        origin = Location(1, 2)
        destination = Location(3, 5)
        passenger = Passenger("id", 5, origin, destination)

        time = driver.start_trip(passenger)
        self.assertEqual(time, 2, 'start-trip 返回值错误')
        self.assertEqual(driver._destination == destination, True, 'start-trip 没有设置目的地')
        self.assertEqual(driver._passenger == passenger, True, 'start-trip 没有设置乘客')
        self.assertEqual(driver.is_idle, False, 'start-trip 没有设置司机状态')
        self.assertEqual(driver.location, location, 'start-trip 不应改变location')


    def test_end_trip(self):
        location = Location(1, 2)
        driver = Driver("id1", location, 3)

        origin = Location(1, 2)
        destination = Location(3, 5)
        passenger = Passenger("id", 5, origin, destination)

        driver.start_trip(passenger)

        driver.end_trip()
        self.assertEqual(driver.location == destination, True, 'end-trip 没有更新location')
        self.assertEqual(driver._destination, None, 'end-trip 没有取消目的地')
        self.assertEqual(driver._passenger == None, True, 'end-trip 没有取消乘客')
        self.assertEqual(driver.is_idle, True, 'end-trip 没有设置司机状态')


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
        actual = (dropoff.timestamp, dropoff.driver, dropoff.passenger)
        expect = (3, driver1, passenger1)
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
        expect = (0, PICKUP, "d1", origin)
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

        event = Dropoff(5, passenger1, driver1)
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



class TestEvent(unittest.TestCase):
    def test_average_total_distance(self):
        monitor = Monitor()
        # monitor._average_total_distance()
        # self.assertEqual(monitor._average_total_distance(), 0.0, '司机人数为0')

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

        # self.assertEqual(monitor._average_trip_distance(), 0.0, '司机人数为0')

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


class TestSimulation(unittest.TestCase):

    def test_run_empty(self):
        events = create_event_list("test_empty.txt")
        sim = Simulation()
        report = sim.run(events)

        rusult = {'average_passenger_wait_time': 0.0,
                  'average_driver_total_distance': 0.0,
                  'average_driver_trip_distance': 0.0}

        self.assertEqual(report == rusult, True,
                         '空文件，不产生任何事件。数据都是0.0。[不要修改教授的ave time函数]')

    def test_run_sall(self):

        events = create_event_list("test_samll_sim.txt")
        sim = Simulation()
        report = sim.run(events)
        #print(report)
        # rusult = {'rider_wait_time': 2.0,
        #           'driver_total_distance': 5.0,
        #           'driver_ride_distance': 2.0}


        self.assertEqual(report['average_passenger_wait_time'], 2.0,
                         '平均等待时间不一致')
        self.assertEqual(report['average_driver_total_distance'], 5.0,
                         '平均驾驶距离不一致')
        self.assertEqual(report['average_driver_trip_distance'], 2.0,
                         '平均接送距离不一致')



    def test_run(self):

        events = create_event_list("test_sim.txt")
        sim = Simulation()
        report = sim.run(events)
        rusult = {'average_passenger_wait_time': 1.1666666666666667,
                  'average_driver_total_distance': 12.875,
                  'average_driver_trip_distance': 7.75}

        self.assertEqual(report, rusult,
                         '结果不一致')



if __name__ == '__main__':
    unittest.main()
