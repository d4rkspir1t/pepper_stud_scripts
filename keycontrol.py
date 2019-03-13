#!/usr/bin/env python
from naoqi import ALProxy
import argparse
import tty
import termios
import sys
import select
import qi

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


def setup(session):

    motion = session.service('ALMotion')
    motion.setStiffnesses('Body', 1.0)
    motion.setStiffnesses('Head', 1.0)
    motion.moveInit()
    motion.setOrthogonalSecurityDistance(0.1)

    names = "Head"
    angleLists = [0.0, 0.0]
    motion.setAngles(names, angleLists, 0.1)

    target = 'All'
    print('Security', motion.getExternalCollisionProtectionEnabled(target))
    motion.setExternalCollisionProtectionEnabled(target, False)

    albgmovements = session.service('ALBackgroundMovement')
    albgmovements.setEnabled(False)

    awareness = session.service('ALBasicAwareness')
    awareness.pauseAwareness()
    return motion, albgmovements, awareness


def exec_motion(motion, lin_vel, side_vel, ang_vel):
    motion.move(lin_vel, side_vel, ang_vel)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.2",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--verbose", action="store_true",
                        help="Printing to console")
    parser.add_argument("--plot", action="store_true",
                        help="Plotting recorded variable lists")
    parser.add_argument("--csv", action="store_true",
                        help="Logging to a csv file")
    args = parser.parse_args()

    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) + ".\n"
                                                                                              "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    settings = termios.tcgetattr(sys.stdin)
    status = 0
    target_linear_vel  = 0.0
    target_angular_vel = 0.0
    target_side_vel = 0.0
    lin_step = 0.1
    side_step = 0.1
    ang_step = 0.1
    motion, albgmovements, awareness = setup(session)

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
                if key == 'c':
                    names = "Head"
                    angleLists = [0.0, 0.0]
                    motion.setAngles(names, angleLists, 0.1)
                if (key == '\x03'):
                    target_linear_vel = 0.0
                    target_angular_vel = 0.0
                    target_side_vel = 0.0
                    motion.stopMove()
                    print vels(target_linear_vel, target_side_vel, target_angular_vel)
                    break

            if not awareness.isAwarenessPaused():
                awareness.pauseAwareness()
            if status == 20 :
                print msg
                status = 0
            exec_motion(motion, target_linear_vel, target_side_vel, target_angular_vel)
    except:
        print e

    finally:
        sec_dist = motion.getOrthogonalSecurityDistance()
        if sec_dist < 0.4:
            motion.setOrthogonalSecurityDistance(0.4)
        target = 'All'
        motion.setExternalCollisionProtectionEnabled(target, True)
        motion.setStiffnesses('Body', 0.0)
        motion.setStiffnesses('Head', 0.0)
        albgmovements.setEnabled(True)
        awareness.resumeAwareness()

        print('Bye!')

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
