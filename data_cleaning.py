# libraries
import os
from tqdm import tqdm
import pandas as pd

# main
if __name__ == '__main__':
    RAW_DATA_DIR = os.path.normpath(r'.\Data')
    print(os.listdir(RAW_DATA_DIR))

    # Getting the company info master
    df_company_info_master = pd.DataFrame()
    for file_name in tqdm(os.listdir(RAW_DATA_DIR)):
        if 'power' in file_name or 'ghg' in file_name:
            file_path = os.path.join(RAW_DATA_DIR, file_name)
            df_raw = pd.read_excel(file_path, header=2) 
            df_raw = df_raw.set_index('Entity ID')

            ts_index = float('nan')
            for i in df_raw.iloc[1,:].values:
                if i == i:
                    ts_index = list(df_raw.iloc[1,:].values).index(i)
                    break
            df_info_part = df_raw.iloc[:, :ts_index]
            
            # Use the first and second row as column name - SP id + CY
            df_company_info_master = pd.concat([df_company_info_master, df_info_part])
            df_company_info_master = df_company_info_master.drop_duplicates()
    df_company_info_master = df_company_info_master.drop(float('nan'))
    # Export the cleaned data
    cleaned_file_name = 'df_info_master.csv'
    df_company_info_master.to_csv(os.path.join('.', 'Cleaned_Data', cleaned_file_name), index=True)
    

    # Cleaning the power excel
    df_power_ts_master = pd.DataFrame()
    for file_name in tqdm(os.listdir(RAW_DATA_DIR)):
        # Debug line
        # file_name = os.listdir(RAW_DATA_DIR)[4]
        if 'power' in file_name:
            file_path = os.path.join(RAW_DATA_DIR, file_name)
            df_raw = pd.read_excel(file_path, header=2) # All are (8949, 43/25)

            # Set the index to be the Entity ID
            df_raw = df_raw.set_index('Entity ID')

            # find ts starting point
            ts_index = float('nan')
            for i in df_raw.iloc[1,:].values:
                if i == i:
                    ts_index = list(df_raw.iloc[1,:].values).index(i)
                    break
            df_ts_part = df_raw.iloc[:, ts_index:]

            # Use the first and second row as column name - SP id + CY
            df_ts_part.columns = df_ts_part.iloc[0].values + '_' + df_ts_part.iloc[1].values
            df_ts_part = df_ts_part.iloc[3:,:]

            df_power_ts_master = pd.concat([df_power_ts_master, df_ts_part], axis=1)
    
    cleaned_file_name = 'df_power_ts_master.csv'
    df_power_ts_master.to_csv(os.path.join('.', 'Cleaned_Data', cleaned_file_name), index=True)
    
    

    # Cleaning the ghg excel
    df_ghg_ts_master = pd.DataFrame()
    for file_name in tqdm(os.listdir(RAW_DATA_DIR)):
        # Debug line
        # file_name = os.listdir(RAW_DATA_DIR)[4]
        if 'ghg' in file_name:
            file_path = os.path.join(RAW_DATA_DIR, file_name)
            df_raw = pd.read_excel(file_path, header=2) # All are (8949, 43/25)

            # Set the index to be the Entity ID
            df_raw = df_raw.set_index('Entity ID')

            # find ts starting point
            ts_index = float('nan')
            for i in df_raw.iloc[1,:].values:
                if i == i:
                    ts_index = list(df_raw.iloc[1,:].values).index(i)
                    break
            df_ts_part = df_raw.iloc[:, ts_index:]

            # Use the first and second row as column name - SP id + CY
            df_ts_part.columns = df_ts_part.iloc[0].values + '_' + df_ts_part.iloc[1].values
            df_ts_part = df_ts_part.iloc[3:,:]

            df_ghg_ts_master = pd.concat([df_ghg_ts_master, df_ts_part], axis=1)
    
    cleaned_file_name = 'df_ghg_ts_master.csv'
    df_ghg_ts_master.to_csv(os.path.join('.', 'Cleaned_Data', cleaned_file_name), index=True)

