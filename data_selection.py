"""
Select the targeted companies from all the long form
"""
# libraries
import os
from tqdm import tqdm
import pandas as pd

if __name__ == "__main__":
    os.chdir(os.path.join('.\ECON4999X'))
    CLEANED_DATA_DIR = os.path.normpath(r'.\Cleaned_Data')
    print(os.listdir(CLEANED_DATA_DIR))
    
    # Select the targeted companies
    df_selected_comps = pd.read_csv(os.path.join(CLEANED_DATA_DIR, 'df_selected_comps.csv'), encoding='latin-1', index_col=0)
    df_selected_comps = df_selected_comps.reset_index()

    # Read long form time series
    ts_file_name = 'df_ghg_ts_long_form.csv'
    ts_file_path = os.path.join(CLEANED_DATA_DIR, ts_file_name)
    df = pd.read_csv(ts_file_path)

    df_selected = df.merge(df_selected_comps['entity_id'], on='entity_id', how='right')
    df_selected['entity_id'].nunique()
    # export
    cleaned_file_name = 'df_ghg_ts_long_form_selected.csv'
    df_selected.to_csv(os.path.join(CLEANED_DATA_DIR, cleaned_file_name), index=False)

    # Filter the selected companies from long form power time series
    ts_file_name = 'df_power_ts_long_form.csv'
    ts_file_path = os.path.join(CLEANED_DATA_DIR, ts_file_name)
    df = pd.read_csv(ts_file_path)

    df_selected = df.merge(df_selected_comps['entity_id'], on='entity_id', how='right')
    df_selected['entity_id'].nunique()
    # export
    cleaned_file_name = 'df_power_ts_long_form_selected.csv'
    df_selected.to_csv(os.path.join(CLEANED_DATA_DIR, cleaned_file_name), index=False)
