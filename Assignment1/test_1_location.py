import unittest
from location import Location, manhattan_distance, deserialize_location


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

if __name__ == '__main__':
    unittest.main()
