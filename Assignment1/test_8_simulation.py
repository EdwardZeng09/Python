
import unittest
from container import PriorityQueue
from dispatcher import Dispatcher
from event import Event, create_event_list
from monitor import Monitor
from simulation import Simulation

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
