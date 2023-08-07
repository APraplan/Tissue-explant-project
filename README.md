# Tissue explant project

## Objectives
In the context of tumor research, personalized medical treatments are very expensive and not widely accessible. One aspect of the research involves isolating samples from a biopsy to test several treatments on the same tumor. This project aims to develop a robotic platform capable of selecting, moving, and culturing these different samples to streamline the resulting research and make the technique more affordable.

<p align="center">
  <img src=https://github.com/APraplan/Tissue-explant-project/assets/102581647/a2fc5a77-ee43-46f8-9007-71de811df887 width="600">
</p>

## Hardware


The project use the frame from a 3D printer, an anycubic mega zero with it's controller. A webcam is used in order to detect and track the samples and three dynamixel xl430 are used to actuate two micro-pipette in order to act like a pneumatic gripper and to automate the manipulation of liquids..
The next illustrations represent the frame of the robot, the end effextor with the camera and the two pipette tips and the actuation of the pipette.

<p align="center">
  <img src=https://github.com/APraplan/Tissue-explant-project/assets/102581647/9572526d-2aea-4ac9-890c-88496cf5c024 width=400>
  <img src=https://github.com/APraplan/Tissue-explant-project/assets/102581647/9491d089-d363-485e-b1a6-77915be80771 width=400>
  <br />
  <img src=https://github.com/APraplan/Tissue-explant-project/assets/102581647/5af37c6f-3fae-4b4e-ba93-a12e1c62b9a3 width=800>
  <br />
  <img src=https://github.com/APraplan/Tissue-explant-project/assets/102581647/2d33303c-686a-4d1b-bafa-7784a51ddd15 width=800>
<!--   <img src=https://github.com/APraplan/Tissue-explant-project/assets/102581647/0e87f826-67db-4a24-9667-6fe99478dcc2 width=400> -->
</p>


## Computer vision
One of the main constraint of this project was to be able to detect and select the tissue samples. The webcam placed at the end effector of the robot makes it possible. The camera gives the position of the particles and it is also used to check if the samples are correctly picked up by the tip of the pipette. 

The first challenge was to guarantie a high precision, under the milimeter scale for the evaluation of the position of the particles. The results on the tests patterns are very demonstratives and show a high repetability, the pattern here is used with a needle on the end effector to perforate the sheet.

<p align=center>
  <img src=https://github.com/APraplan/Tissue-explant-project/assets/102581647/72a405a1-bf46-4a53-aa01-3a52034d86cd width=600>
</p>

The second aspect is to detect and select the different samples taking into account their size and shape to ensure more representative results.

<p align=center>
  <img src=  width=400>
  <img src=  width=400>
</p>

In order to increase the reliability of the platform a second camera is used to validate the catch. A macro camera is used on the side to evaluate the tip. 

<p align="center">
  <img src=https://github.com/APraplan/Tissue-explant-project/assets/102581647/6038e902-d1f7-42bd-8073-8eb91fe38501 width=400>
  <img src=https://github.com/APraplan/Tissue-explant-project/assets/102581647/933e7158-f30c-4ca2-8dc3-d1c17217bc4a width=400>
</p>

To assess the images, a convolutional neural netword as been trained. The role of the network is to classify the images while been very robust to the differents shapes of samples and lighting conditions. The tests shows a very high reliability, over 98% and a rate of false positives close to zero.

<p align="center">
  <img src=https://github.com/APraplan/Tissue-explant-project/assets/102581647/3bda8a96-e742-4747-898d-87a8af75925e width=400>
</p>

## Results

The platform as been tested on three diffrents types of samples. The differents results as been collected on mouse samples, spleen, kidney and colon tissues. This samples gives a good ideas of the capabilities of the robot.

<p align="center">
  
</p>

## Paper 
comming soon...
