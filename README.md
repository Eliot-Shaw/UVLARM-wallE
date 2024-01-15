# Projet LARM - Logiciel et Architecture pour la Robotique Mobile - Groupe 3

This is the shared repository of group 3 (Eliot Shaw & Clarice Goulet) for the challenges and the end project of the UV LARM.
We are using the WallE machine. 


## Installation

Go to https://github.com/Eliot-Shaw/UVLARM-wallE.git and clone the repository on your machine

You need to build your ros workspace with the command : `colcon build`

For challenge n°1, you can run the program with the following command: `ros2 launch grp_wallE_ch1 tbot_launch.yaml`
The data streamed in the topics are also accessible by another computer on the same domain ID by running the command: `ros2 launch grp_wallE_ch1 visualize_launch.yaml`

You should have:
* The mb6-space as your ros workspace for the computer controlling the bot
* The following configurations (in your ros workspace) for both of the computers:

        export ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET
        export ROS_DOMAIN_ID=03

The rivz2 config file is available in the /config directory


todo :
- affiner detection bouteille :
        - hsv
        - forme

- Map en node
- Img depth en node (recupere centre zone verte et retourne la distance de ce pixel)

- Orientation robot par rapport à map en node
- Placage bouteille par rapport à bot (recupere distance bouteille, angle par rapp map et map et retourne coordonéesrdonées bouteilles carte)

