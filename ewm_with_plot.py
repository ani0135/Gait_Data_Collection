import matplotlib.pyplot as plt

from matplotlib.dates import DateFormatter
import pandas as pd
import glob
import os

# Load the sample data into a DataFrame
csv_files = glob.glob('0021*_z_score.csv', recursive=True)
for csv_data in csv_files:
    # csv_data = '0002_04_20241217_R_Leg_z_score.csv'
    df = pd.read_csv(csv_data)
    base_name = csv_data.split("_")
    id = base_name[0]
    session = base_name[1]
    date = base_name[2]
    leg = base_name[3]
    # Create the DataFrame
    df = pd.read_csv(csv_data)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    print(df)


    # Calculate successive differences

    alpha = 0.3  # Smoothing factor, between 0 and 1
    df['T'] = df['T'].ewm(alpha=alpha).mean()
    df['H1'] = df['H1'].ewm(alpha=alpha).mean()
    df['H2'] = df['H2'].ewm(alpha=alpha).mean()

    # df['x'] = df['x'].ewm(alpha=alpha).mean()
    # df['y'] = df['y'].ewm(alpha=alpha).mean()
    # df['z'] = df['z'].ewm(alpha=alpha).mean()

    print(df)
    path = id+'_'+session+'_'+date+'_'+leg+'_Leg.csv'
    df.to_csv(path, index=False)
    # Create zoomable interactive plots

    fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    fig.suptitle("Successive Differences of Sensor Data (Zoomable)")



    # Define a date formatter for the x-axis

    date_format = DateFormatter("%H:%M:%S.%f")

    for ax in axs:

        ax.xaxis.set_major_formatter(date_format)



    # Plot each column difference

    axs[0].plot(df['Timestamp'], df['T'], label='X', color='blue')

    axs[0].set_ylabel('T_diff')

    axs[0].legend(loc='upper right')



    axs[1].plot(df['Timestamp'], df['H1'], label='Y', color='orange')

    axs[1].set_ylabel('H1_diff')

    axs[1].legend(loc='upper right')



    axs[2].plot(df['Timestamp'], df['H2'], label='Z', color='green')

    axs[2].set_ylabel('H2_diff')

    axs[2].legend(loc='upper right')



    # Formatting

    axs[2].set_xlabel('Timestamp')

    plt.xticks(rotation=45)

    plt.tight_layout(rect=[0, 0, 1, 0.95])



    # Enable zoom and pan interaction

    plt.subplots_adjust(hspace=0.3)

    # plt.show()
    os.remove(csv_data)

