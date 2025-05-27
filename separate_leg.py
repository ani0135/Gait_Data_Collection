import pandas as pd
import os
import glob

# Get all CSV files in the directory and subdirectories
csv_files = glob.glob('raw_data/raw_leg_sensor_data/0021/0021_*_raw.csv', recursive=True)

for file_path in csv_files:
    # Load the data into a DataFrame
    df = pd.read_csv(file_path)
    
    # Get file naming components
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    new_name = base_name.split("_")
    id = new_name[0]
    session = new_name[1]
    date = new_name[2]
    
    # Extract L_Leg and R_Leg data into separate DataFrames
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['L_Leg'] = df['RawData'].str.extract(r'"L_Leg": ?"(\d+ \d+ \d+)"')
    df['R_Leg'] = df['RawData'].str.extract(r'"R_Leg": ?"(\d+ \d+ \d+)"')
    
    # Process left leg data
    df_l_leg = df.dropna(subset=['L_Leg'])
    df_l_leg = df_l_leg.copy()
    df_l_leg[['T', 'H1', 'H2']] = df_l_leg['L_Leg'].str.split(' ', expand=True)
    df_l_leg = df_l_leg[['Timestamp', 'T', 'H1', 'H2']]
    
    # Process right leg data
    df_r_leg = df.dropna(subset=['R_Leg'])
    df_r_leg = df_r_leg.copy()
    df_r_leg[['T', 'H1', 'H2']] = df_r_leg['R_Leg'].str.split(' ', expand=True)
    df_r_leg = df_r_leg[['Timestamp', 'T', 'H1', 'H2']]
    
    # Generate output file paths
    l_leg_path = id + '_' + session + '_' + date + '_' + 'L_Leg_raw.csv'
    r_leg_path = id + '_' + session + '_' + date + '_' + 'R_Leg_raw.csv'
    
    # Save to CSV files
    df_l_leg.to_csv(l_leg_path, index=False)
    df_r_leg.to_csv(r_leg_path, index=False)
    
    print(f"Processed {file_path} -> {l_leg_path}, {r_leg_path}")