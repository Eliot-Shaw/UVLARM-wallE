# Projet LARM - Logiciel et Architecture pour la Robotique Mobile - Groupe 3

This is the shared repository of group 3 (Eliot Shaw & Clarice Goulet) for the challenges and the end project of the UV LARM.
We are using the WallE machine. 


## Installation

Go to https://github.com/Eliot-Shaw/UVLARM-wallE.git and clone the repository on your machine

You need to build your ros workspace with the command : `colcon build`

For challenge n°2, you can run the program with the following command: `ros2 launch grp_wallE_ch2 tbot_launch.yaml`
The simulation program can be launched with the command : `ros2 launch grp_wallE_ch2 simulation_launch.yaml`

The data streamed in the topics are accessible with the Rviz2 tool: `rviz2`

You should have:
* The mb6-space as your ros workspace for the computer controlling the bot
* The following configurations (in your ros workspace) for both of the computers:

        export ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET
        export ROS_DOMAIN_ID=03

Please use our config file in Rviz2 accessible in [the /config file directory : grp_wallE_ch2/config/config_challenge_2.rviz](grp_wallE_ch2/config/config_challenge_2.rviz)


## Abilities
### Navigation
The robot can move smoothly in a unknown environnement safely and cover the entire surface of the room. 

### Vision
The robot is able to collect and process images to detect multiple green bottles in the frame using color thresholding and silouhette recognition.

### Mapping
The robot will ensure to map the visited place using the Simultaneous localization and mapping (SLAM) algorythm.
The robot is able to, using the image bottle detection, place bottles on the map using relative coordinates of a bottle from the robot frame.