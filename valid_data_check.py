# import pandas as pd
# from datetime import timedelta

# # Example CSV data as a string

# # Read data into a DataFrame
# df = pd.read_csv("0008_01_20250102_L_Leg_raw.csv")

# # Parse the Timestamp column to datetime
# df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# # Sort by Timestamp (in case the rows are out of order)
# df = df.sort_values('Timestamp')

# # Calculate time differences between consecutive rows
# df['TimeDiff'] = df['Timestamp'].diff().dt.total_seconds()

# # Check for gaps longer than 10 milli second (customize threshold as needed)
# missing_data = df[df['TimeDiff'] > 0.05]

# # Print results
# print("Missing Data Points:")
# print(missing_data)

# if missing_data.empty:
#     print("\nNo missing data found.")
# else:
#     print(f"\nMissing data found at the following rows (gaps > 1 second):")
#     print(missing_data[['Timestamp', 'TimeDiff']])


import pandas as pd

# Filepath of your CSV file
file_path = "0010_04_20250105_R_Leg_raw.csv"

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Convert the 'Timestamp' column to datetime format
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Extract seconds from the 'Timestamp' column
df['Second'] = df['Timestamp'].dt.floor('s')

# Group by the second and count occurrences
second_counts = df.groupby('Second').size()

# Filter seconds with less than 130 data points
seconds_with_low_counts = second_counts[second_counts < 130]

# Output the results
print(f"Number of seconds with less than 130 data points: {len(seconds_with_low_counts)}")
print("Seconds with less than 130 data points:")
print(seconds_with_low_counts)
