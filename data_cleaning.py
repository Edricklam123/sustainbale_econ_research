# libraries
import os
import pandas as pd

# main
if __name__ == '__main__':
    RAW_DATA_DIR = os.path.normpath(r'C:\Users\dickl\Dropbox\Uni study file\Sem 8\ECON4999X\Project\Data')
    print(os.listdir(RAW_DATA_DIR))

    # Cleaning the power excel
    for file_name in os.listdir(RAW_DATA_DIR):
        if 'power' in file_name:
            file_path = os.path.join(RAW_DATA_DIR, file_name)
            df_raw = pd.read_excel(file_path, header=2)
            # find ts starting point
            ts_index = float('nan')
            for i in df_raw.iloc[1,:].values:
                if i == i:
                    ts_index = list(df_raw.iloc[1,:].values).index(i)
                    break
            df_ts_part = df_raw.iloc[:, ts_index:]
