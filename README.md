# Laboratory of Cyberphysical and Robotic Intelligent Systems

This repository contains the source code and documentation for the **Autonomous Racing** and **Autonomous Drone** challenges.

---

## 1. File Scheme

The repository is organized into two main directories, corresponding to each challenge.

### **Autonomous Racing Challenge**

This folder contains the control code developed for the autonomous navigation of a racing vehicle using different control algorithms:

* **p_version.py**: Implementation of the **Proportional (P)** controller.

* **pd_version.py**: Implementation of the **Proportional-Derivative (PD)** controller.

* **pid_version.py**: Implementation of the **Proportional-Integral-Derivative (PID)** controller.

### **Autonomous Drone Challenge**

This folder contains the complete control code developed for the autonomous navigation of a drone in a rescue mission:

* **Fast approach to the rescue zone**: Implementation of the fast approach, using set cmd_vel and PID for altitude.
  
* **Precise approach to the rescue zone**: Implementation of the precise approach, using set cmd_pos.

* **Spiral and FaceDetection**: A set of functions for doing a spiral movement over the impact zone, detecting and counting faces in the process.


---

## 2. Initializing the Tests 🚀

To run and test the codes in a simulated and reproducible environment, it is recommended to use **Docker**. Follow these steps in a Linux terminal:

### **Step 1: Download the Docker Image**

Use the following command to get the latest JDERobot robotics-backend image:

```bash
docker pull jderobot/robotics-backend:latest
```

### **Step 2: Launch the Container (Choose Your Option)**

Expand the option that best suits your system's graphics configuration:

<details> <summary>Option A: No Graphics Acceleration</summary>

Ideal for environments without GPU support or where graphics acceleration is not critical:

```bash
docker run --rm -it \

-p 6080-6090:6080-6090 -p 7163:7163 jderobot/robotics-backend:latest
```
</details>

<details> <summary>Option B: With Graphics Acceleration (General)</summary>

Recommended to take advantage of your graphics card's rendering capabilities (requires the device /dev/dri):


```bash
docker run --rm -it --device /dev/dri \
-p 6080-6090:6080-6090 -p 7163:7163 jderobot/robotics-backend:latest
```

</details>

<details> <summary>Option C: With NVIDIA Card</summary>

Use this option if you have an NVIDIA card and want maximum graphics performance (requires installing the NVIDIA Container Toolkit and using the --gpus all flag):


```bash
docker run --rm -it --device /dev/dri --gpus all \

-p 6080-6090:6080-6090 -p 7163:7163 jderobot/robotics-backend:latest
```

</details>

### **Step 3: Run Simulation**
1. Go to ![Unibotics](https://unibotics.org)
2. Register
3. Go to Robotics Academy
4. Go to Free Course
5. Select the Environment (Follow Line or ...)
6. Click Connect in the bottom left corner
7. Paste one of the codes from the repo
8. Click Play

---

## 3. Photos and Results 📸

### **Autonomous Racing Challenge**

P Simulation Example

![](https://github.com/JoelRamosBeltran/Laboratory-of-Cyber-physical-and-Robotic-Intelligent-Systems/blob/main/Autonomous%20Racing%20Challenge/photos/mejor_P.png)

PD Simulation Example

![](https://github.com/JoelRamosBeltran/Laboratory-of-Cyber-physical-and-Robotic-Intelligent-Systems/blob/main/Autonomous%20Racing%20Challenge/photos/mejor_PD.png)

PID Simulation Example

![](https://github.com/JoelRamosBeltran/Laboratory-of-Cyber-physical-and-Robotic-Intelligent-Systems/blob/main/Autonomous%20Racing%20Challenge/photos/mejor_PID.png)

### **Autonomous Drone Challenge**

Six faces detected and Drone Returned to base

![](https://github.com/JoelRamosBeltran/Laboratory-of-Cyber-physical-and-Robotic-Intelligent-Systems/blob/main/Autonomous%20Drone%20Challenge/6_caras_vueltabase.png)
