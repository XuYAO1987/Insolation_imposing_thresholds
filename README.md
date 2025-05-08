# Insolation_imposing_thresholds

We provide Python code for generating dynamic visualizations of insolation series (using the 65°N Laskar 2004 solution for the past 10 million years) across threshold continua, along with simulated rank and couplet time series and their cross-spectral coherence and phase at 405-kyr periodicities.

We use the "Input_insolation_time_series.csv" as the only input data source for generating the rank and couplet time series.

We employ the "calculating_insolation_to_rank_couplet" Python package to simulate rank and couplet time series for each threshold model. This package calculates key model parameters including: the proportion of rank 1 states in the rank time series, the average couplet duration, the cross-spectral coherence and phase relationships between rank and couplet series at 405-kyr periodicities. The results are saved in the four output CSV files.

We utilize the "plotting_insolation_rank_couplet_coherence_phase" Python package to visualize the rank and couplet time series across threshold continua within the insolation series, and the cross-spectral coherence and phase relationships between rank and couplet series at 405-kyr periodicities. The results are displayed as an animation in a GIF file.

We use the "plotting_Output_Propotion_Duration_Coherence_Phase" Python package to exhibit the proportion of rank 1, average duration of couplets, cross-spectral coherence and phase between rank and couplet series at 405-kyr periodicities in each threshold model. The results are displayed in a PNG file.
