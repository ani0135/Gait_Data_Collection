import pandas as pd
from datetime import timedelta

# Load the CSV file
file_path = '0001_01_L_Leg.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Define the column for timestamps and target frequency
timestamp_column = 'Timestamp'
frequency = 140  # 140 Hz = 140 samples per second

# Function to handle duplicates and resample for periodic data
def resample_pressure_data(df, time_col, freq):
    # Convert timestamps to datetime
    df[time_col] = pd.to_datetime(df[time_col])
    
    # Handle duplicates by averaging
    df = df.groupby(time_col).mean().reset_index()
    
    # Set the time column as the index and sort
    df = df.sort_values(by=time_col).set_index(time_col)
    
    # Generate a new time index at the desired frequency
    start_time = df.index.min()
    end_time = df.index.max()
    resampled_index = pd.date_range(start=start_time, end=end_time, freq=f'{int(1_000 / freq)}L')

    # Reindex and interpolate using cubic spline
    df = df.reindex(resampled_index)  # Align to the new time index
    df = df.interpolate(method='spline', order=3)  # Smooth cubic spline interpolation
    df = df.fillna(method='bfill').fillna(method='ffill')  # Ensure no NaNs remain
    df.reset_index(inplace=True)
    df.rename(columns={'index': time_col}, inplace=True)
    
    return df

# Apply the function to resample the data
resampled_data = resample_pressure_data(data, timestamp_column, frequency)

# Save the resampled data to a new CSV file
output_csv_path = 'resampled_pressure_data_140Hz.csv'
resampled_data.to_csv(output_csv_path, index=False)

print(f"Resampled pressure data saved to: {output_csv_path}")
