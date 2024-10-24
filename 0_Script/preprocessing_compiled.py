import os
import pandas as pd

def read_compiled_files(folder_path):
    csv_dict = {}
    
    for filename in os.listdir(folder_path):
        
        if filename.endswith('.csv'):
            
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            filename = os.path.splitext(filename)[0].replace('_compiled', '')
            csv_dict[filename] = df
    
    return csv_dict



def create_monitors_dict(dfs_dict):
    monitors = {}
    for df_name, df in dfs_dict.items():
        monitors[df_name] = []
        for column in df.columns[1:]:
            monitor_df = df[["datetime", column]].copy()
            monitors[df_name].append(monitor_df)
    return monitors