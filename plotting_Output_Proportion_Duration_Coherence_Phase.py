import pandas as pd
import matplotlib.pyplot as plt

# read CSV file
df = pd.read_csv('Output_Proportion_Duration_Coherence_Phase.csv', header=0)
time_col = df.columns[0]
metrics = df.columns[1:]

fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(6, 6))
plt.subplots_adjust(hspace=0.4)
y_limits = [
    (0, 1),      
    (10, 1000),      
    (0, 1),  
    (0, 180)      
]

# plot cycle
for i, (ax, metric) in enumerate(zip(axes, metrics)):
    ax.plot(df[time_col], df[metric], linewidth=1)
    ax.set_ylim(y_limits[i])
    
    #set y axis labels
    if i == 1: 
        ax.set_yscale('log')
        ax.yaxis.set_major_formatter(plt.ScalarFormatter()) 
        ax.set_ylabel(f"{metric} (log scale)", fontsize=9, rotation=0)
    else:
        ax.set_ylim(y_limits[i])

    ax.set_ylabel(metric, fontsize=9, rotation=90)
    ax.yaxis.set_label_coords(-0.1, 0.5)


    if i == 0:  # first subplot set the threshold
        ax.xaxis.set_ticks_position('top')
        ax.xaxis.set_label_position('top')
        ax.xaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
        plt.setp(ax.get_xticklabels(), ha='left')  
        ax.set_xlabel(df.columns[0], fontsize=10)
    else:
        # other subplots do not need threshold
        ax.tick_params(
            labelbottom=False,  
            labeltop=False,     
            bottom=False,       
            top=(i==0)         
        )


#save
output_file = 'Output_proportion_Duration_Coherence_Phase.png' 
plt.savefig(output_file, dpi=300)

# show
plt.show()