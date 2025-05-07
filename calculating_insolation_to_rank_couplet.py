import numpy as np
import pandas as pd
from scipy.stats import trim_mean
from scipy.signal import coherence, csd

#------------------------------
#step 1, read original insolation time series csv file
df = pd.read_csv('Input_insolation_time_series.csv', header = 0)
time_column = df.columns[0]  # time
insolation_column = df.columns[1]  # insolation values (watts/meter^2)

#------------------------------
#step 2, impose the insolation with a series of thresholds from 428 to 510 at interval 1
# NOTE: you can use an interval 0.1, which need 3-5 minutes for running codes and plotting
thresholds = pd.Series(np.arange(428, 511, 1))
new_df = pd.DataFrame()
new_df[time_column] = df[time_column]  # keep the time series
for threshold in thresholds:
    new_column_name = f'{threshold}'
    new_df[new_column_name] = df[insolation_column].apply(lambda x: threshold )
output_file = 'Output_insolation_threshold.csv'  
new_df.to_csv(output_file, index=False)  # index=False prevents writing index
print(f'{output_file} is saved')

#------------------------------
#step 3, formulate the insolation rank time series
# imposing the thresholds to insolation values
new_df = pd.DataFrame()
new_df[time_column] = df[time_column]  # keep the time series
for threshold in thresholds:
    new_column_name = f'{threshold}'
    new_df[new_column_name] = df[insolation_column].apply(lambda x: 1 if x > threshold else -1)
output_file = 'Output_insolation_rank.csv'  
new_df.to_csv(output_file, index=False)  # index=False prevents writing index
print(f'{output_file} is saved')

#------------------------------
# step 4, formulate the insolation couplet time series
def process_couplet(series):
    """Process grouping logic for a single column containing 1/-1 sequences"""
    # Create temporary DataFrame with standardized column name
    temp_df = series.rename('value').reset_index()
    # Generate continuous block identifiers using vectorized operations
    temp_df['block'] = (temp_df['value'] != temp_df['value'].shift()).cumsum()
    # Build block information DataFrame with start/end positions
    block_df = temp_df.groupby('block').agg(
        start=('index', 'first'),
        end=('index', 'last'),
        value=('value', 'first'),
        length=('index', 'count')
    ).reset_index(drop=True)
        # Apply grouping rules based on 1/-1 sequences
    groups = []
    i = 0
    while i < len(block_df):
        current = block_df.iloc[i]
                # Merge 1-blocks with subsequent -1 blocks
        if current['value'] == 1 and i+1 < len(block_df) and block_df.iloc[i+1]['value'] == -1:
            next_block = block_df.iloc[i+1]
            groups.append((current['start'], next_block['end'], current['length'] + next_block['length']))
            i += 2
        else:
        # Handle standalone blocks (leading -1 or trailing 1)
            groups.append((current['start'], current['end'], current['length']))
            i += 1
    # Create new series with group counts
    new_series = pd.Series(0, index=series.index)
    for start, end, count in groups:
        new_series.loc[start:end] = count
    return new_series

# read rank time series csv file
df = pd.read_csv('Output_insolation_rank.csv')

# process the rank series to couplet series
for col in df.columns[1:]:
    df[col] = process_couplet(df[col].astype(int))

output_file = 'Output_insolation_couplet.csv'  
df.to_csv(output_file, index=False)  # index=False prevents writing index
print(f'{output_file} is saved')

#------------------------------
# step 5, calculate the propotion, duration, coherence, phase of rank and couplet time series
def calculate_propotion_duration_coherence_phase(file1, file2, fs=1):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    results = [] # ready to save results
    
    # calculate parameters for each threshold
    for col in df1.columns[1:]:      
        x = df1[col] # rank series
        y = df2[col] # couplet series
        
        # calculate propotion of ranks 1, and average duration of couplets
        valid = x.isin([1, -1])
        count_1 = (x.loc[valid] == 1).sum()
        count_neg1 = (x.loc[valid] == -1).sum()
        propotion = count_1 / (count_1 + count_neg1)
        duration = trim_mean(y, proportiontocut=0.2) # remove 20% extreme values
                        
        # calculate coherence and phase
        freq, Cxy = coherence(x, y, fs, nperseg=4096, noverlap=2500)
        coh = Cxy
        freq, Pxy = csd(x, y, fs, nperseg=4096, noverlap=2500)
        phase = np.angle(Pxy, deg=True) 
        phase = abs(phase)
        # choose bands of frequencies
        freq_mask = (freq >= 0.0015) & (freq <= 0.0035)
        selected_coherence = np.mean(coh[freq_mask])
        selected_phase = np.mean (phase[freq_mask])
        
        #keep decimal places
        propotion = np.round(propotion, 4)  
        duration = np.round(duration, 2)  
        selected_coherence = np.round(selected_coherence, 3) 
        selected_phase = np.round(selected_phase, 2) 
        
        # Output
        results.append({
            'Threshold': col,
            'Propotion': propotion,
            'Duration' : duration,
            'Coherence': selected_coherence,
            'Phase'    : selected_phase
        })
    return pd.DataFrame(results)

# main function
if __name__ == "__main__":
    # input rank and couplet series
    file1 = "Output_insolation_rank.csv"
    file2 = "Output_insolation_couplet.csv"
    # calculate
    result_df = calculate_propotion_duration_coherence_phase(file1, file2)
    # save the ouputs
    output_file = 'Output_Propotion_Duration_Coherence_Phase.csv'  
    result_df.to_csv (output_file, index=False)  # index=False prevents writing index
    print(f'{output_file} is saved')




