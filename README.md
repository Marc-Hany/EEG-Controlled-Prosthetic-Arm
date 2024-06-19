# EEG-Controlled-Prosthetic-Arm


![Project Image or Logo](https://github.com/Marc-Hany/EEG-Controlled-Prosthetic-Arm/blob/main/Arm.png?raw=true)

## Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Project Files](#project-files)


## About the Project

The EEG-Controlled Prosthetic Arm project leverages EEG signals channels Pz, P3, P4, Cz, C3, and C4 to enable six distinct grasp and lift movements. A machine learning model processes these signals to predict user intentions, which are then transmitted via Bluetooth to an ESP32 microcontroller that controlls servo motors for precise control of the prosthetic arm.

## Features

- EEG Dataset Utilization:EEG signals captured from predefined channels and saved in a dataset were used to train a deep learning model.
- Machine Learning Model: Employed for real-time prediction of user actions based on EEG data, ensuring responsive and intuitive prosthetic control.
- Bluetooth Communication: Facilitates seamless transmission of processed signals from the machine learning model to the ESP32 microcontroller embedded in the prosthetic arm.
- Graphical User Interface (GUI): Provides a user-friendly interface for initiating and adjusting grasp and lift functions.
- Real Life Model Integration: Incorporates a customizable prosthetic arm model, designed for comfort and functionality.
![System Workflow](https://github.com/Marc-Hany/EEG-Controlled-Prosthetic-Arm/blob/main/System%20Workflow.png?raw=true)


## Project Files
-For more details: https://drive.google.com/drive/folders/1ki9Iui3ly2TKzNObjGp2JHiSAL6yZ45y
