#! /usr/bin/env python
from __future__ import print_function
import sys
import rospy

# Brings in the SimpleActionClient
import actionlib

# Brings in the messages used by the factorial action, including the
# goal message and the result message.
import exercise3.msg


def factorial_client():
    # Creates the SimpleActionClient, passing the type of the action
    # (FactorialAction) to the constructor.
    client = actionlib.SimpleActionClient(
        'factorial', exercise3.msg.FactorialAction)

    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()

    # Creates a goal to send to the action server.
    goal = exercise3.msg.FactorialGoal(order=10)

    # Sends the goal to the action server.
    client.send_goal(goal)

    # Waits for the server to finish performing the action.
    client.wait_for_result()

    # Prints out the result of executing the action
    return client.get_result()  # A FactorialResult


if __name__ == '__main__':
    try:
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
        rospy.init_node('factorial_client')
        result = factorial_client()
        print("Resultant factorial is ", ', '.join(
            [str(n) for n in result.sequence]))
    except rospy.ROSInterruptException:
        print("program interrupted before completion", file=sys.stderr)
