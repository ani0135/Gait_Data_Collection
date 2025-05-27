import matplotlib.pyplot as plt

from matplotlib.dates import DateFormatter


import pandas as pd
# Load the sample data into a DataFrame
csv_data = '/media/ani/TOSHIBA_E/Projects/PGP/Sensor_Reading/processed_data/leg_sensor/0021/03/0021_03_20250322_L_Leg.csv'
df = pd.read_csv(csv_data)
base_name = csv_data.split("_")
id = base_name[0]
session = base_name[1]
date = base_name[2]
leg = base_name[3]
# Create the DataFrame
df = pd.read_csv(csv_data)
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
 
fig.suptitle("Successive Differences of Sensor Data")



# Define a date formatter for the x-axis

date_format = DateFormatter("%H:%M:%S.%f")

for ax in axs:

    ax.xaxis.set_major_formatter(date_format)



# Plot each column difference

# axs[0].plot(df['Timestamp'], df['x'], label='X', color='blue')
# axs[1].plot(df['Timestamp'], df['y'], label='Y', color='orange')
# axs[2].plot(df['Timestamp'], df['z'], label='Z', color='green')


axs[0].plot(df['Timestamp'], df['T'], label='X', color='blue')
axs[1].plot(df['Timestamp'], df['H1'], label='Y', color='orange')
axs[2].plot(df['Timestamp'], df['H2'], label='Z', color='green')

# axs[0].set_ylabel('T_diff')
# axs[0].legend(loc='upper right')
# axs[1].set_ylabel('H1_diff')
# axs[1].legend(loc='upper right')
# axs[2].set_ylabel('H2_diff')
# axs[2].legend(loc='upper right')

axs[0].set_ylabel('X')
axs[0].legend(loc='upper right')
axs[1].set_ylabel('Y')
axs[1].legend(loc='upper right')
axs[2].set_ylabel('Z')
axs[2].legend(loc='upper right')

axs[2].set_xlabel('Timestamp')

plt.xticks(rotation=45)

plt.tight_layout(rect=[0, 0, 1, 0.95])



# Enable zoom and pan interaction

plt.subplots_adjust(hspace=0.3)

plt.show()

