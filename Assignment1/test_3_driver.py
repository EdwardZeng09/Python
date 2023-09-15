import unittest
from driver import Driver
from passenger import Passenger
from location import Location


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


if __name__ == '__main__':
    unittest.main()

