import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import pandas as pd

def plot_df(param, df, peak_dict, min_co2, max_co2, max_pm2p5, max_tvoc, min_temp, max_temp, min_hum, max_hum):
    
    '''
    Plot the DataFrame
    
    Inputs:
    - param
    - df
    - customized range for parameters
    '''
    
    sns.set_style("whitegrid", {"grid.color": ".4", "grid.linestyle": ":", "grid.alpha":'.2'})
    
    fig_dict = {
        'tvoc': {
            'title': 'TVOC',
            'xlabel': '',
            'ylabel': 'TVOC Concentration [ppb]'
    },
        'pm2p5': {
            'title': r'$PM_{2.5}$',
            'xlabel': '',
            'ylabel': r'$PM_{2.5}$' + ' Concentration [\u03BCg/m\u00b3]'
    },
        'pm10': {
            'title': r'$PM_{10}$',
            'xlabel': '',
            'ylabel': r'$PM_{10}$' + ' Concentration [\u03BCg/m\u00b3]'
        },
        'temp': {
            'title': 'Temperature',
            'xlabel': '',
            'ylabel': 'Temperature [°C]'
        },
        'co2': {
            'title': r'$CO_{2}$',
            'xlabel': '',
            'ylabel': r'$CO_{2}$ Concentration [ppm]'
        },
        'humidity': {
            'title': 'Relative Humidity',
            'xlabel': '',
            'ylabel': 'Relative Humidity [%RH]'
        }
     }
    fig, ax = plt.subplots(figsize=(12,6))
    
    # Convert datetime column to datetime type if it's not already
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.drop(f'reference_{param}', axis = 1)
    
    for i in df.columns:
        if i != 'datetime':
            if "reference" in i:
                ax.plot(df['datetime'], df[i], linewidth=2, color='black', alpha=0.4)
            else:
                ax.plot(df['datetime'], df[i], alpha=0.8)
                
    # [Optional] temporarily set max for pm2p5 to 60
    if param == 'co2':
        ax.set_ylim([min_co2, max_co2])
    
    if param == 'pm2p5':
        ax.set_ylim([0, max_pm2p5])
    
    # [Optional] temporarily set max for tvoc to 2000
    if param == 'tvoc':
        ax.set_ylim([0, max_tvoc])
        
    # [Optional] temporarily set temp to 15 - 30
    if param == 'temp':
        ax.set_ylim([min_temp, max_temp])
        
    # [Optional] temporarily set temp to 30 - 90
    if param == 'humidity':
        ax.set_ylim([min_hum, max_hum])
    
    peak_times = list(peak_dict[param].keys())
    peak_values = list(peak_dict[param].values())
    ax.scatter(peak_times, peak_values, color='red', s=60, marker='^', label='Peaks')
    
    ax.set_xlim(df['datetime'].min(), df['datetime'].max())
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    ax.tick_params(axis="x", labelrotation=90)   
    
    ax.spines[:].set_color('black')
    ax.legend(df.columns[1:], bbox_to_anchor=(0.5, 1.17), ncol=3, loc='upper center')
    ax.set_ylabel(fig_dict[param]['ylabel'], fontsize=12, labelpad=6)
    
    plt.tight_layout()
    return fig