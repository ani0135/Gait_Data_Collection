import cv2
import os
import pandas as pd
from datetime import datetime, timedelta

def extract_frames(video_path, output_dir):
    # Extract the initial timestamp from the video filename
    video_name = os.path.basename(video_path)
    timestamp_str = video_name.split('_')[2] + video_name.split('_')[3].split('.')[0]

    try:
        initial_timestamp = datetime.strptime(timestamp_str, "%Y%m%d%H%M%S%f")
    except ValueError:
        raise ValueError("Video filename should contain a timestamp in the format VID_YYYYMMDD_HHMMSSsss.mp4.")

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise IOError("Could not open video file.")

    # Get FPS (frames per second)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"FPS: {fps}")

    frame_count = 0
    success, frame = cap.read()
    extracted_frames = []  # Store filenames for filtering

    while success:
        # Calculate the timestamp for the current frame
        frame_time = initial_timestamp + timedelta(seconds=frame_count / fps)
        frame_time_str = frame_time.strftime("%Y-%m-%d_%H_%M_%S_%f")[:-3]  # Format to milliseconds

        # Save the frame with a timestamped filename
        frame_filename = os.path.join(output_dir, f"frame_{frame_time_str}.jpg")
        cv2.imwrite(frame_filename, frame)
        extracted_frames.append(frame_filename)

        frame_count += 1
        success, frame = cap.read()

    cap.release()
    print(f"Extracted {frame_count} frames to {output_dir}")

    return extracted_frames  # Return list of extracted frames


def filter_and_remove_extra_frames(output_dir, input_csv):
    # Load the input CSV file to get start and end timestamps
    input_df = pd.read_csv(input_csv)

    # Extract the first and last timestamps
    start_time = pd.to_datetime(input_df.iloc[0]["Timestamp"])
    end_time = pd.to_datetime(input_df.iloc[-1]["Timestamp"])

    # Function to extract timestamp from frame filename
    def extract_timestamp(filename):
        try:
            parts = filename.split("_")
            date_part = parts[1]  # YYYY-MM-DD
            time_part = parts[2:5]  # HH, MM, SS
            millisec = parts[5].split(".")[0]  # Milliseconds without extension

            timestamp_str = f"{date_part} {time_part[0]}:{time_part[1]}:{time_part[2]}.{millisec}"
            return pd.to_datetime(timestamp_str)
        except Exception:
            return None  # Return None if filename format is incorrect

    # List all frames in the directory
    all_frames = [f for f in os.listdir(output_dir) if f.startswith("frame_") and f.endswith(".jpg")]

    # Filter frames based on timestamp range
    for frame in all_frames:
        frame_path = os.path.join(output_dir, frame)
        frame_timestamp = extract_timestamp(frame)

        # If frame is outside the range, delete it
        if frame_timestamp is None or not (start_time < frame_timestamp < end_time):
            os.remove(frame_path)
            print(f"Removed: {frame}")

    print("Filtering complete. Extra frames deleted.")


# Example usage
video_path = "raw_data/raw_video_data/0021/03_VID_20250322_144142717.mp4"  # Video filename with timestamp
output_dir = "processed_data/frames/0021/03"
input_csv = "processed_data/leg_sensor/0021/03/0021_03_20250322_L_Leg.csv"  # CSV containing start and end timestamps

# Extract frames
extract_frames(video_path, output_dir)

# Filter frames and remove extra ones
filter_and_remove_extra_frames(output_dir, input_csv)
