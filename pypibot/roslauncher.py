import subprocess
import rospy
import rosnode

class roslauncher:
    def __init__(self, cmd=None):
        self.cmd = cmd

    def launch(self):
        self.child = subprocess.Popen(self.cmd)
        return True

    def shutdown(self):
        self.child.terminate()
        self.child.wait()
        return True