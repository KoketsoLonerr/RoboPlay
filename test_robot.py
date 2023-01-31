import unittest
from io import StringIO
import sys
from test_base import run_unittests
from test_base import captured_io
import maze.obstacles as obstacles
import robot

class MyTests(unittest.TestCase):
    def test_step3_default_maze(self):

        with captured_io(StringIO('BEN\noff\n')) as (out, err):
            obstacles.random.randint = lambda a, b: 1
            robot.robot_start()

        output = out.getvalue().strip()

        self.assertEqual("""What do you want to name your robot? BEN: Hello kiddo!
BEN: Loaded obstacles.
There are some obstacles:
- At position 1,1 (to 5,5)""", output[:130])



if __name__ == '__main__':
    unittest.main()
