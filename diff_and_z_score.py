import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter
import glob
import os

csv_files = glob.glob('0021*_raw.csv', recursive=True)
for file_path in csv_files:
    # file_path = '0002_04_20241217_R_Leg_raw.csv'
    df = pd.read_csv(file_path)
    base_name = file_path.split("_")
    id = base_name[0]
    session = base_name[1]
    date = base_name[2]
    leg = base_name[3]
    df_time = df['Timestamp']
    df = df.iloc[:,1:].diff()
    df.iloc[0] = 0
    print(df)

    def zscore(s, window, thresh=1, return_all=False):
        roll = s.rolling(window=window, min_periods=1, center=True)
        avg = roll.mean()
        std = roll.std(ddof=0)
        z = s.sub(avg).div(std)   
        m = z.between(-thresh, thresh)

        if return_all:
            return z, avg, std, m
        return s.where(m, avg)

    for col in df.columns:
        df[col] = zscore(df[col], window=25)
    df = pd.concat([df_time, df], axis=1)

    path = id+'_'+session+'_'+date+'_'+leg+'_Leg_z_score.csv'
    df.to_csv(path, index=False)

    print(f"Post-processed data saved to {str(path)}")
    os.remove(file_path)


