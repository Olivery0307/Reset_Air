def extract_monitors_value_at_peak(params_dict, final_dict):
    value_dict = {}
    for param, df in params_dict.items():
        
        peak_df = df[df['datetime'].isin(final_dict[param].keys())].copy()
        columns_for_mean = [col for col in peak_df.columns if col not in ['datetime', f'reference_{param}']]
        peak_df[f'mean_{param}'] = peak_df[columns_for_mean].mean(axis=1)
        
        value_dict[param] = peak_df
    return value_dict