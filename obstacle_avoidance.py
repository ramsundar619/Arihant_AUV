#! /usr/bin/env python

import rospy

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

pub = None

def main():
    global pub

    rospy.init_node('reading_laser')

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    sub = rospy.Subscriber('/m2wr/laser/scan1', LaserScan, clbk_laser)

    rospy.spin()




def clbk_laser(msg):
    regions = {
        'right':  min(msg.ranges[40], 10),
        'front':  min((msg.ranges[360]), 10),
        'left':   min(msg.ranges[680], 10),
    }

    take_action(regions)


def take_action(regions):
    msg = Twist()
    linear_x = 0
    angular_z = 0

    state_description = ''
    dist = 0.1
    dist1 = 0.6
    if regions['front'] > dist and regions['left'] > dist1 and regions['right'] > dist1:
        state_description = 'case 1 - nothing'
        linear_x = 0.3
        angular_z = 0
    elif regions['front'] < dist and regions['left'] > dist1 and regions['right'] > dist1:
        state_description = 'case 2 - front'
        linear_x = 0.05
        angular_z = 0
    elif regions['front'] > dist and regions['left'] > dist1 and regions['right'] < dist1:
        state_description = 'case 3 - right'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] > dist and regions['left'] < dist1 and regions['right'] > dist1:
        state_description = 'case 4 - fleft'
        linear_x = 0.1
        angular_z = 0.3
    elif regions['front'] < dist and regions['left'] > dist1 and regions['right'] < dist1:
        state_description = 'case 5 - front and fright'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] < dist and regions['left'] < dist1 and regions['right'] > dist1:
        state_description = 'case 6 - front and fleft'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] < dist and regions['left'] < dist1 and regions['right'] < dist1:
        state_description = 'case 7 - front and fleft and fright'
        linear_x = 0.05
        angular_z = 0
    elif regions['front'] > dist and regions['left'] < dist1 and regions['right'] < dist1:
        state_description = 'case 8 - fleft and fright'
        linear_x = 0.3
        angular_z = 0
    else:
        state_description = 'unknown case'
        rospy.loginfo(regions)

    rospy.loginfo(state_description)
    msg.linear.x = linear_x
    msg.angular.z = angular_z
    pub.publish(msg)

if __name__ == '__main__':
    main()
