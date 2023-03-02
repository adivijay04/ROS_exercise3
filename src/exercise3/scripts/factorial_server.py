#! /usr/bin/env python

import rospy

import actionlib

import exercise3.msg


class FactorialAction(object):
    # create messages that are used to publish feedback/result
    _feedback = exercise3.msg.FactorialFeedback()
    _result = exercise3.msg.FactorialResult()

    def __init__(self, name):
        self._action_name = name
        self._as = actionlib.SimpleActionServer(
            self._action_name, exercise3.msg.FactorialAction, execute_cb=self.execute_cb, auto_start=False)
        self._as.start()

    def execute_cb(self, goal):
        # helper variables
        r = rospy.Rate(1)
        success = True

        # append the seeds for the fibonacci sequence
        self._feedback.sequence = []
        self._feedback.sequence.append(1)
        self._feedback.sequence.append(2)

        # publish info to the console for the user
        rospy.loginfo('%s: Executing, creating factorial of order %i' % (
            self._action_name, goal.order))

        # start executing the action
        while(self._feedback.sequence[1] <= goal.order):
            # check that preempt has not been requested by the client
            if self._as.is_preempt_requested():
                rospy.loginfo('%s: Preempted' % self._action_name)
                self._as.set_preempted()
                success = False
                break

            self._feedback.sequence[0] = self._feedback.sequence[0] * \
                self._feedback.sequence[1]
            self._feedback.sequence[1] += 1
            # publish the feedback
            self._as.publish_feedback(self._feedback)
            # this step is not necessary, the sequence is computed at 1 Hz for demonstration purposes
            r.sleep()

        if success:
            self._result.sequence = self._feedback.sequence
            rospy.loginfo('%s: Succeeded' % self._action_name)
            self._as.set_succeeded(self._result)


if __name__ == '__main__':
    rospy.init_node('factorial')
    server = FactorialAction(rospy.get_name())
    rospy.spin()
