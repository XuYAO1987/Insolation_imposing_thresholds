# Insolation_imposing_thresholds
We provide Python code for generating dynamic visualizations of the insolation series (65 North Laskar 2004 solution for the past 10 million years) across threshold continua, alongside simulated rank and couplet time series as well as their cross-spectrum coherence and phase at 405-kyr periodicities.

We use the "Input_insolation_time_series.cvs" as the only input data to generate the rank and couplet time series.

We use the "calculating_insolation_to_rank_couplet" python package to simulate the rank and couplet time series in each threshold model, and calculate the parameters of each threshold model including the propotion of rank 1 in the rank time series, the average duration of couplet, the cross-spectrum coherence and phase of rank and couplet at 405-kyr periodicities. 

We use the "plotting_insolation_rank_couplet_coherence_phase" python package to visualize the rank and couplet time series across threshold continua in the insolation time series, as well as the  cross-spectrum coherence and phase of rank and couplet at 405-kyr periodicities. 
