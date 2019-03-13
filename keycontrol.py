#!/usr/bin/env python
from naoqi import ALProxy
import tty
import termios
import sys
import select

msg = """
Control Your Pepper!
---------------------------
Moving around:
        w
   a    s    d
   v         n
        
w/s : increase/decrease linear velocity
a/d : increase/decrease angular velocity
v/n : increase/decrease side velocity
q : lin_vel -> 0
e : ang_vel -> 0
b : sid_vel -> 0
space : force stop
CTRL-C to quit
"""

e = """
Communications Failed
"""

def getKey(settings):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def vels(target_linear_vel, target_side_vel, target_angular_vel):
    return "currently:\tlinear vel %s\t angular vel %s\t side vel %s" % (target_linear_vel,target_angular_vel, target_side_vel)


def setup():
    motion = ALProxy('ALMotion', '192.168.1.7', 9559)
    motion.setStiffnesses('Body', 1.0)
    motion.moveInit()
    return motion


def exec_motion(motion, lin_vel, side_vel, ang_vel):
    motion.move(lin_vel, side_vel, ang_vel)


if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    status = 0
    target_linear_vel  = 0.0
    target_angular_vel = 0.0
    target_side_vel = 0.0
    lin_step = 0.1
    side_step = 0.1
    ang_step = 0.1
    motion = setup()

    try:
        print msg
        while(1):
            key = getKey(settings)
            if key == 'w':
                target_linear_vel += lin_step

                status = status + 1
                print vels(target_linear_vel, target_side_vel, target_angular_vel)
            elif key == 's':
                target_linear_vel -= lin_step

                status = status + 1
                print vels(target_linear_vel, target_side_vel, target_angular_vel)
            elif key == 'a':
                target_angular_vel += ang_step

                status = status + 1
                print vels(target_linear_vel, target_side_vel, target_angular_vel)
            elif key == 'd':
                target_angular_vel -= ang_step

                status = status + 1
                print vels(target_linear_vel, target_side_vel, target_angular_vel)
            elif key == 'q':
                target_linear_vel = 0

                status = status + 1
                print vels(target_linear_vel, target_side_vel, target_angular_vel)
            elif key == 'e':
                target_angular_vel = 0

                status = status + 1
                print vels(target_linear_vel, target_side_vel, target_angular_vel)
            elif key == 'e':
                target_angular_vel = 0

                status = status + 1
                print vels(target_linear_vel, target_side_vel, target_angular_vel)
            elif key == 'v':
                target_side_vel += side_step

                status = status + 1
                print vels(target_linear_vel, target_side_vel, target_angular_vel)
            elif key == 'n':
                target_side_vel -= side_step

                status = status + 1
                print vels(target_linear_vel, target_side_vel, target_angular_vel)
            elif key == 'b':
                target_side_vel = 0

                status = status + 1
                print vels(target_linear_vel, target_side_vel, target_angular_vel)
            elif key == ' ':
                target_linear_vel = 0.0
                target_angular_vel = 0.0
                target_side_vel = 0.0
                motion.stopMove()

                status = status + 1
                print vels(target_linear_vel, target_side_vel, target_angular_vel)
            else:
                if (key == '\x03'):
                    break

            if status == 20 :
                print msg
                status = 0
            exec_motion(motion, target_linear_vel, target_side_vel, target_angular_vel)
    except:
        print e

    finally:
        print('Bye!')

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
