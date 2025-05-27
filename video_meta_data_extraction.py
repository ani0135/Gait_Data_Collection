import os
import pandas as pd
from pathlib import Path

frames_root_dir = "processed_data/frames"
output_root_dir = "processed_data/video_metadata"
for frames_root, ids, files in os.walk(frames_root_dir):
    for id in ids:
        id_dir = os.path.join(frames_root,id)
        for id_root, sessions, files in os.walk(id_dir):
            for session in sessions:
                frames_dir_ = os.path.join(id_dir,session)
                base_name = frames_dir_.split("/")
                id = base_name[2]
                session = base_name[3]

                # List all frame files in the directory
                frame_files = sorted([f for f in os.listdir(frames_dir_) if f.endswith('.jpg')])

                # Generate metadata
                metadata = []
                parts = []
                for frame_number, frame_file in enumerate(frame_files):
                    # Extract timestamp from the filename
                    parts = frame_file.split('_')
                    timestamp_str = f"{parts[1]} {parts[2]}:{parts[3]}:{parts[4]}.{parts[5].split('.')[0]}"
                    
                    # Append extracted timestamp and frame number
                    metadata.append([timestamp_str, frame_number])

                # Create a DataFrame
                metadata_df = pd.DataFrame(metadata, columns=['timestamp', 'frame_number'])
                date = parts[1].replace("-","")
                # Save the metadata DataFrame to a CSV file
                output_csv_path = id+'_'+session+'_'+date+'_'+"metadata.csv"
                out_dir = os.path.join(output_root_dir,id,session)
                os.makedirs(out_dir, exist_ok=True)
                output_csv_path = os.path.join(out_dir,output_csv_path)
                metadata_df.to_csv(output_csv_path, index=False)

                print(f"Metadata saved to {output_csv_path}")
