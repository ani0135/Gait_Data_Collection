import pandas as pd
from datetime import datetime, timezone, timedelta
import os

# Load the CSV file
file_path = "raw_data/raw_imu_data/0021/0021_04_20250322_144233_raw_IMU"
file_path_1 = file_path+'/AccelerometerUncalibrated.csv'  # Replace with your actual file path
file_path_2 = file_path+'/Gyroscope.csv'
file_paths = list([file_path_1, file_path_2])
for file_path in file_paths:
    data = pd.read_csv(file_path)
    # base_name = os.path.splitext(os.path.basename(file_path))[2]
    # print(base_name)
    base_name = (file_path.split("/"))[3].split("_")
    print(base_name)
    id = base_name[0]
    session = base_name[1]
    date = base_name[2]

    base_name1 = (file_path.split("/"))[4]
    sensor_name = base_name1[0:4]
    # print(sensor_name)
    # Define Kolkata timezone offset
    kolkata_offset = timedelta(hours=5, minutes=30)

    # Replace the `time` column with formatted timestamps in Kolkata timezone
    data['time'] = data['time'].apply(
        lambda ns: (datetime.fromtimestamp(ns / 1_000_000_000, tz=timezone.utc) + kolkata_offset).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    )
    data.rename(columns={'time':'Timestamp'}, inplace=True)
    data = data.drop("seconds_elapsed", axis = 1)

    # Save the updated data to a new CSV file
    output_csv_path = id+'_'+session+'_'+date+'_'+sensor_name+'.csv'
    data.to_csv(output_csv_path, index=False)

    print(f"Converted timestamps saved to: {output_csv_path}")
