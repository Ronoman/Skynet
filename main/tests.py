import unittest
import lsm

class GyroMath(unittest.TestCase):
    def setUp(self):
        self.gyro = Gyro()

    def test_return_last_value_of_gyro_data(self):
        self.gyro.x = [1, 2, 3]
        self.gyro.y = [4, 5, 6]
        self.gyro.z = [7, 8, 9]
        self.gyro.ts = [10, 11, 12]

        self.assertEqual(gyro.getx(), 3, "not returning most recent x value")
        self.assertEqual(gyro.gety(), 6, "not returning most recent y value")
        self.assertEqual(gyro.getz(), 9, "not returning most recent z value")
        self.assertEqual(gyro.getz(), 12, "not returning most recent ts value")

    def test_riemann_sum_find_area_correctly(self):
        self.assertEqual(gyro.simpleRiemann(0, 7, 0.5), 3.5, "not riemanning correctly")
        self.assertEqual(gyro.simpleRiemann(4, 3, 1.5), 5.5, "previous value not added correctly")

    def test_tolerance_calculates_correctly(self):
        self.assertTrue(gyro.checkTolerance(1, 2, 3, 4), "tolerance throwing out good points")
        self.assertFalse(gyro.checkTolerance(5, 6, 7, 4), "tolerance allowing bad points through")
