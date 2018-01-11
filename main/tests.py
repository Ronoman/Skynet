import unittest
import math
import lsm

class GyroMath(unittest.TestCase):
    def setUp(self):
        self.gyro = lsm.Gyro()

    def test_return_last_value_of_gyro_data(self):
        self.gyro.x = [1, 2, 3]
        self.gyro.y = [4, 5, 6]
        self.gyro.z = [7, 8, 9]
        self.gyro.ts = [10, 11, 12]

        self.assertEqual(self.gyro.getx(), 3, "not returning most recent x value")
        self.assertEqual(self.gyro.gety(), 6, "not returning most recent y value")
        self.assertEqual(self.gyro.getz(), 9, "not returning most recent z value")
        self.assertEqual(self.gyro.getTs(), 12, "not returning most recent ts value")

    def test_riemann_sum_find_area_correctly(self):
        self.assertEqual(self.gyro.simpleRiemann(0, 7.0, 0.5), 3.5, "not riemanning correctly")
        self.assertEqual(self.gyro.simpleRiemann(4.0, 3.0, 1.5), 5.5, "previous value not added correctly")

    def test_tolerance_calculates_correctly(self):
        self.assertTrue(self.gyro.checkTolerance(1, 2, 3, 4), "tolerance throwing out good points")
        self.assertFalse(self.gyro.checkTolerance(5, 6, 7, 4), "tolerance allowing bad points through")
