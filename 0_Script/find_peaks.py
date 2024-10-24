
import pandas as pd
from datetime import timedelta
from scipy.signal import find_peaks

def catch_peaks(monitors_dict, co2_prominence, tvoc_prominence, pm2p5_prominence, temp_prominence, humidity_prominence):
    result = {}
    
    prominence_dict = {
        'co2': co2_prominence,
        'tvoc': tvoc_prominence,
        'pm2p5': pm2p5_prominence,
        'temp': temp_prominence,
        'humidity': humidity_prominence
    }
    
    for filename, monitor_list in monitors_dict.items():
        result[filename] = []
        if 'reference' in filename.lower():
            continue
        
        for monitor_df in monitor_list:
            monitor_column = monitor_df.columns[1]
            
            if 'reference' in monitor_column.lower():
                continue
            
            monitor_df['datetime'] = pd.to_datetime(monitor_df['datetime'])
            prominence = next((v for k, v in prominence_dict.items() if k in monitor_column.lower()), None)
            
            if prominence is None:
                print(f"Warning: No prominence specified for {monitor_column}. Skipping.")
                continue
            
            peaks, _ = find_peaks(monitor_df[monitor_column], prominence=prominence)
            peak_times = monitor_df['datetime'].iloc[peaks]
            peak_values = monitor_df[monitor_column].iloc[peaks]
            peak_dict = {time: value for time, value in zip(peak_times, peak_values)}
            
            result[filename].append({monitor_column: peak_dict})
    
    return result



def find_non_overlapping_peaks_combined(file_data, window_hours=5):
    all_peaks = {}
    for monitor_dict in file_data:
        for monitor_name, peaks in monitor_dict.items():
            all_peaks.update(peaks)
    
    sorted_peaks = sorted(all_peaks.items())
    
    non_overlapping_peaks = {}
    current_window_end = None
    
    for i, (time1, value1) in enumerate(sorted_peaks):
        if current_window_end is None or time1 > current_window_end:
            window_start = time1
            window_end = time1 + timedelta(hours=window_hours)
            highest_peak = (time1, value1)
            for j, (time2, value2) in enumerate(sorted_peaks[i:]):
                if time2 > window_end:
                    break
                if value2 > highest_peak[1]:
                    highest_peak = (time2, value2)
            non_overlapping_peaks[highest_peak[0]] = highest_peak[1]
            current_window_end = window_end
    
    return non_overlapping_peaks

def process_catch_peaks_output(catch_peaks_output, window_hours=5):
    result = {}
    for filename, file_data in catch_peaks_output.items():
        result[filename] = find_non_overlapping_peaks_combined(file_data, window_hours)
    return result