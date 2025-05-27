import pandas as pd
list1 = ["01", "02", "03", "04"]
# Load the input CSV file to get start and end timestamps
for i in list1:
    input_df = pd.read_csv(f"processed_data/leg_sensor/0021/{i}/0021_{i}_20250322_L_Leg.csv")

    # Extract the first and last timestamps
    start_time = input_df.iloc[0]["Timestamp"]
    end_time = input_df.iloc[-1]["Timestamp"]

    # Convert timestamps to datetime
    start_time = pd.to_datetime(start_time)
    end_time = pd.to_datetime(end_time)

    # Load the target CSV file where we want filter
    file_path_1 = f"0021_{i}_20250322_Acce.csv"
    file_path_2 = f"0021_{i}_20250322_Gyro.csv"
    filpath = list([file_path_1, file_path_2])
    for file_path in filpath:
        if(file_path == ""):
            continue
        target_df = pd.read_csv(file_path)

        # Convert the 'Timestamp' column to datetime
        target_df["Timestamp"] = pd.to_datetime(target_df["Timestamp"])

        # Filter the target DataFrame based on the timestamp range (inclusive)
        filtered_df = target_df[(target_df["Timestamp"] >= start_time) & (target_df["Timestamp"] <= end_time)]

        # Save the filtered data to a new CSV file
        filtered_df.to_csv(file_path, index=False)

        # Display the filtered DataFrame
        print(filtered_df)