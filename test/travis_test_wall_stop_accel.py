#!/usr/bin/env python
import unittest, rostest
import rosnode, rospy
import time

class WallStopAccelTest(unittest.TestCase):
    def set_and_get(self, lf, ls, rs, rf):
        with open("/dev/rtlightsensor0", "w") as f:
            f.write("%d %d %d %d\n" % (rf, rs, ls, lf))

        time.sleep(0.3)

        with open("/dev/rtmotor_raw_l0", "r") as lf, \
             open("/dev/rtmotor_raw_r0", "r") as rf:
            left = int(lf.readline().rstrip())
            right = int(rf.readline().rstrip())

        return left, right

    def test_io(self):
        left, right = self.set_and_get(100,100,50,60)
        self.assertTrue(left == 0 and right == 0, "can't stop")

        left, right = self.set_and_get(50, 0, 0, 49)
        time.sleep(5.0)
        self.assertTrue(left == right, "left should same as right")
        self.assertTrue((0 < left) and (left < 1000), "can't move again")



if __name__ == "__main__":
    time.sleep(3)
    rospy.init_node("travis_test_wall_stop_accel")
    rostest.rosrun("pimouse_run_corridor", "travis_test_wall_stop_accel", WallStopAccelTest)
        
