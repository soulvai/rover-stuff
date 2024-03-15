# joystick_node
Currently designed for Havit controller with XBox 360 controller layout.

## Requirements

 - [`joy`](http://wiki.ros.org/joy) (ROS package)

## Controller configuration (initial setup)

 - Connect the controller to the GSC
 - Check the controller name by running: `ls /dev/input`
 - The controller should be in the format `jsX` (default: `js0`)
 -  (optional) Check controller responses: `sudo jstest /dev/input/js0`
 - Set the permission for controller port to read+write: `sudo chmod a+rw /dev/input/jsX`
 - Make the controller port default for `joy` package: `rosparam set joy_node/dev "/dev/input/js0"`
 - (optional) Run `rosrun joy joy_node` to initiate joystick in ROS. Run `rostopic echo /joy` to check input.

## joystick_node configuration
- Create a package in a ROS workspace
- in the `src` directory, copy and paste this folder
- Build the package
- Run `roslaunch joystick_node joystick.launch`
