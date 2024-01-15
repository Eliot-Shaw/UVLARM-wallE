# Projet LARM - Logiciel et Architecture pour la Robotique Mobile - Groupe 3

This is the shared repository of group 3 (Eliot Shaw & Clarice Goulet) for the challenges and the end project of the UV LARM.
We are using the WallE machine. 


## Installation

go to https://github.com/Eliot-Shaw/UVLARM-wallE.git
clone the repository on your machine

run the command in your ros workspace : `colcon build`

For challenge n°1, you can run the program with the following command: `ros2 launch grp_wallE_ch1 tbot_launch.yaml`
The data streamed in the topics are also accessible by another computer on the same domain ID by running the command: `ros2 launch grp_wallE_ch1 visualize_launch.yaml`

You should have:
* The mb6-space as your ros workspace for the computer controlling the bot
* The following configurations (in your ros workspace) for both of the computers:

        export ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET
        export ROS_DOMAIN_ID=03