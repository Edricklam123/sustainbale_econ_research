# libraries
import os
from tqdm import tqdm
import pandas as pd

# main
if __name__ == '__main__':
    os.chdir(os.path.join('.\ECON4999X'))
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

    # Turn the time series into long form
    # Load the dataframe
    CLEANED_DATA_DIR = os.path.join(r'.\Cleaned_data')
    ts_file_name = 'df_power_ts_master.csv'
    ts_file_path = os.path.join(CLEANED_DATA_DIR, ts_file_name)
    df = pd.read_csv(ts_file_path)

    # melt the df
    df_long_form = df.melt(id_vars='entity_id')
    pattern_year = r'_cy(\d{4})'
    pattern_var = r'TC_COMPANY_POWER_GEN_(.+)_cy.*'.lower()
    df_long_form['year'] = df_long_form['variable'].str.extract(pattern_year)
    df_long_form['power'] = df_long_form['variable'].str.extract(pattern_var)
    df_long_form.head()

    df_long_form = df_long_form[['entity_id', 'power', 'year', 'value']]
    df_long_form = df_long_form.pivot_table(columns='power', index=['entity_id', 'year'], values='value')
    
    cleaned_file_name = 'df_power_ts_long_form.csv'
    df_long_form.to_csv(os.path.join('.', 'Cleaned_Data', cleaned_file_name))
    """
    Note: many eu companies have number, that is good
    """

    # Turn the ghg time series into long form
    # Load the dataframe
    CLEANED_DATA_DIR = os.path.join(r'.\Cleaned_data')
    ts_file_name = 'df_ghg_ts_master.csv'
    ts_file_path = os.path.join(CLEANED_DATA_DIR, ts_file_name)
    df = pd.read_csv(ts_file_path)

    # melt the df
    df_long_form = df.melt(id_vars='entity_id')
    pattern_year = r'_cy(\d{4})'
    pattern_var = r'tc_(.+)_cy.*'.lower()
    df_long_form['year'] = df_long_form['variable'].str.extract(pattern_year)
    df_long_form['ghg_scope'] = df_long_form['variable'].str.extract(pattern_var)
    df_long_form.head()
    df_long_form = df_long_form[['entity_id', 'ghg_scope', 'year', 'value']]
    df_long_form = df_long_form.pivot_table(columns='ghg_scope', index=['entity_id', 'year'], values='value')
    
    cleaned_file_name = 'df_ghg_ts_long_form.csv'
    df_long_form.to_csv(os.path.join('.', 'Cleaned_Data', cleaned_file_name))

    # Clean the column names for all master df
    CLEANED_DATA_DIR = os.path.join(r'.\Cleaned_data')
    file_name_list = ['df_info_master.csv', 'df_ghg_ts_master.csv', 'df_power_ts_long_form.csv', 'df_power_ts_master.csv']
    for file_name in file_name_list:
        file_path = os.path.join(CLEANED_DATA_DIR, file_name)
        df = pd.read_csv(file_path)
        df.columns = [x.lower().replace(' ', '_').replace(':', '') for x in df.columns]
        if 'unnamed_0' in df.columns:
            df = df.drop('unnamed_0', axis=1)
        df.to_csv(file_path)


    # Select the companies
    CLEANED_DATA_DIR = os.path.join(r'.\Cleaned_data')
    file_name = 'df_info_master.csv'
    file_path = os.path.join(CLEANED_DATA_DIR, file_name)

    df_info_master = pd.read_csv(file_path)
    df_info_master = df_info_master.drop('Unnamed: 0', axis=1)
    df_selected_comps = df_info_master.query(r'industry_classification.isin(@selected_industry)')
    """
    I found tht there may be duplicated companies, all fields are same except the industry, we need to drop them as well
    """
    df_selected_comps = df_selected_comps.drop_duplicates('entity_id', keep='first')

    # Filter the exchange country
    CLEANED_DATA_DIR = os.path.join(r'.\Cleaned_data')
    file_name = 'df_exchange_mapping.csv'
    file_path = os.path.join(CLEANED_DATA_DIR, file_name)

    df_ex_map = pd.read_csv(file_path, encoding='latin-1')
    df_selected_comps = df_selected_comps.merge(df_ex_map, on='exchange', how='left')
    df_selected_comps = df_selected_comps.query(r'is_eu == "Y"')
    df_selected_comps = df_selected_comps.drop_duplicates()

    # exporting
    cleaned_file_name = 'df_selected_comps.csv'
    df_selected_comps.to_csv(os.path.join('.', 'Cleaned_Data', cleaned_file_name), index=False)
    df_selected_comps

if __name__ == '__utils__':
    CLEANED_DATA_DIR = os.path.join(r'.\Cleaned_data')
    file_name = 'df_info_master.csv'
    file_path = os.path.join(CLEANED_DATA_DIR, file_name)
    df_company_info_master = pd.read_csv(file_path)
    df_company_info_master.columns
    # Print industry list
    industry_list = df_company_info_master['industry_classification'].unique().tolist()
    _ = [print(x) for x in industry_list]
    selected_industry = [x for x in industry_list if 'electric' in x.lower()]

    # Print primary industry list
    pri_industry_list = df_company_info_master['Primary Industry'].unique().tolist()
    _ = [print(x) for x in pri_industry_list]

    # Print secondary industry list
    sec_industry_list = df_company_info_master['2nd Level Primary Industry'].unique().tolist()
    _ = [print(x) for x in sec_industry_list]

    # Next step: making the data ts into long form so that we can run regression
    # Also plot some initial graphs
    # also adding the company geographical location