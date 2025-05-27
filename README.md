# Gait Analysis Data Collection and Preprocessing Pipeline

A synchronized multi-modal data collection pipeline using the **GaitForce smart shoe**, smartphone IMU sensors, and video footage for accurate human gait analysis.

---

## Overview

This project facilitates the synchronized collection and processing of:

- **Smartphone Camera** (mounted on headband)
- **Sensor Logger Android App** (max sampling frequency)
- **GaitForce Smart Shoe** (sampling at ~138 Hz)

The collected data is preprocessed and synchronized

---

## Hardware Requirements

- **GaitForce Shoe** (with foot pressure sensors)
- **NodeMCU Communication Module** (ESP8266 or similar)
- **Smartphone** (with Sensor Logger App and Camera)
- **Headband** (to mount the phone)
- **Portable Battery Pack** (to power the NodeMCU)

---

## Data Collection Workflow

*** 1. Preparation**

a. Connect the battery to the Communication Module.
b. Ask the participant to wear the GaitForce Shoe.
c. Connect the shoe to the Communication Module.
d. Ask the person: "Can you walk freely?" If not adjust the shoe tightness.
e. Mount the smartphone on the participant's headband.
   - Ensure the x-axis in Sensor Logger App represents gravity (this axis is used in accelerometer data).
f. Start GaitForce data logging:
   ➤ python save_udp_server_Leg_only.py

g. Start Sensor Logger App recording (max sampling frequency).

h. Start video recording:
   ➤ State their ID (what you will save) aloud before walking.

i. After the trial ends do below in steps for better synchronisation:
   ➤ Stop video recording.
   ➤ Stop Sensor Logger data collection.
   ➤ Stop GaitForce script (Ctrl+C).

*** 2. Data Preprocessing & Synchronization**
1. separate_leg.py
   ➤ Splits data into separate CSVs for Left and Right legs.

2. diff_and_z_score.py
   ➤ Computes successive differences and applies z-score normalization.

3. ewm_with_plot.py
   ➤ Smooths data using Exponential Weighted Moving average.

4. plot.py (Manual step)
   ➤ Open Left Leg CSV and delete unnecessary initial rows (since most subjects start walking with left leg).

5. filter_csv.py
   ➤ Filters Right Leg data based on filtered Left Leg timestamps.
   ➤ Can be done manually as well.

6. convert_timestamp.py
   ➤ Extracts data from Sensor Logger IMU files.
   ➤ Uses:
       - `Uncalibrated Accelerometer`
       - `Calibrated Gyroscope`

   ⚙️ Kalman filter is applied later to remove gravity component.

7. filter_csv.py (again)
   ➤ Filters Acc/Gyro data based on the processed Left Leg data.

8. extract_frames.py
   ➤ Extracts frames from video and filters them using Left Leg timestamps.

*** 3. Directory Structure**
.
├── Master_Hardware/
│   └── Code for NodeMCU Communication Module
├── processed_data/
│   ├── frames/
│   ├── imu/
│   └── leg_sensor/
├── raw_data/
│   ├── raw_imu_data/
│   ├── raw_leg_sensor_data/
│   └── raw_video_data/
├── save_udp_server_Leg_only.py
├── separate_leg.py
├── diff_and_z_score.py
├── ewm_with_plot.py
├── plot.py
├── filter_csv.py
├── convert_timestamp.py|
├── extract_frames.py
└── README.md