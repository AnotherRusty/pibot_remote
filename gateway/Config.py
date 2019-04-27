# tcp server
HOST = '0.0.0.0'
PORT = 8998

# protocol
BOF = 0x5a
EOF = 0x0a

# robot status update
ABSOLUTE = 0    # absolute pose in a map
RELATIVE = 1    # pose relative to initial place (odom)
ROBOT_POSE_TYPE = ABSOLUTE
ROBOT_STATUS_UPDATE_FREQUENCY = 10  # Hz

# automatic robot status feedback
ROBOT_STATUS_AUTOFEED = True
ROBOT_STATUS_AUTOFEED_FREQUENCY = 20    # Hz

# enable/disable debug
DEBUG = False
ROBOT_STATUS_DEBUG = False

LAUNCH_NAVIGATION = True
#NAVIGATION_LAUNCH_CMD = ["roslaunch", "pibot_simulator", "nav.launch"]
NAVIGATION_LAUNCH_CMD = ["roslaunch", "pibot_navigation", "nav.launch"]
