import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import coherence, csd
from matplotlib.gridspec import GridSpec
import matplotlib.animation as animation


# read all data
df_ins = pd.read_csv('Input_insolation_time_series.csv')  # original data
df_thr = pd.read_csv('Output_insolation_threshold.csv')
df_rank = pd.read_csv('Output_insolation_rank.csv')
df_coup = pd.read_csv('Output_insolation_couplet.csv')

# parameters
time = df_ins.iloc[:,0].values
num_frames = df_thr.shape[1]-1  # total frames（based on numbers of thresholds）
fs = 1/(time[1]-time[0])       # sampling rate
colors = plt.cm.winter(np.linspace(0,1,num_frames))  # using a uniform color changing from blue to green
N = df_thr.iloc[2, 2] - df_thr.iloc[1, 1]
N = round(N, 1) #this is used to adjust the speed of animation


# set figure
fig = plt.figure(figsize=(10.95, 10))  
gs = GridSpec(4, 2, 
             height_ratios=[0.9, 0.9,0.9, 0.9],  
             width_ratios=[1, 1],           
             hspace=0.4,                   
             top=0.95,
             bottom=0.05
             )                     

# creat subplots
ax1 = fig.add_subplot(gs[0, :])  
ax2 = fig.add_subplot(gs[1, :])  
ax3 = fig.add_subplot(gs[2, :])  
ax4 = fig.add_subplot(gs[3, 0])  
ax5 = fig.add_subplot(gs[3, 1])  

# initiate figure and subplots
def init():
    # creat subplots
    ax1.plot(time, df_ins.iloc[:,1], 'gray', lw=0.5)
    ax1.set(xlim=(-10000,0), ylim=(410,530), xlabel='Age (ka)')
    ax1.set(ylabel='Insolation (W/m²)')
    ax2.set(xlim=(-10000,0), ylim=(-2,2), xlabel='Age (ka)')
    ax2.set(ylabel='Rank (1 and -1)')
    ax3.set(xlim=(-10000,0), yscale='log', ylim=(10,2000), xlabel='Age (ka)')
    ax3.set(ylabel='Couplet (duration/kyr)')
    ax4.set(xlim=(0,0.005), ylim=(0,1.0), xlabel='Frequency (cycle/kyr)')
    ax4.set(ylabel='Coherence of 405-kyr')
    ax5.set(xlim=(0,0.005), ylim=(0,200), xlabel='Frequency (cycle/kyr)')
    ax5.set(ylabel='Phase (°) of 405-kyr')
    # creat dynamic lines
    line1, = ax1.plot([], [], '--', lw=3)
    line2, = ax2.plot([], [], lw=1)
    line3, = ax3.plot([], [], lw=1.5)
    line4, = ax4.plot([], [], lw=3)
    line5, = ax5.plot([], [], lw=3)
    return line1, line2, line3, line4, line5

# initiate the lines
lines = init()

# update animation
def animate(frame):
    
    # update lines of threshold, rank and couplet
    current_thr = df_thr.iloc[:, frame + 1]
    current_rank = df_rank.iloc[:, frame + 1]
    current_coup = df_coup.iloc[:, frame + 1]
    lines[0].set_data(time, current_thr)  # threshold
    lines[1].set_data(time, current_rank)  # Rank
    lines[2].set_data(time, current_coup)  # Couplet
    
    # calculate the cross-spectrum analysis
    x = df_rank.iloc[:, frame + 1].values
    y = df_coup.iloc[:, frame + 1].values
    
    # calculate the cross-spectrum
    freq, Cxy = coherence(x, y, fs, nperseg=4096, noverlap=2500)
    coh = Cxy
    freq, Pxy = csd(x, y, fs, nperseg=4096, noverlap=2500)
    phase = np.angle(Pxy, deg=True) 
    phase = abs(phase)
    
    # choose bands of frequencies
    mask = (freq >= 0) & (freq <= 0.005)
    
    # update coherence and phase
    lines[3].set_data(freq[mask], coh[mask])    
    lines[4].set_data(freq[mask], phase[mask])  
    
    # update lines color
    lines[0].set_color(colors[frame])
    lines[1].set_color(colors[frame])
    lines[2].set_color(colors[frame])
    lines[3].set_color(colors[frame])
    lines[4].set_color(colors[frame])

    # update title
    ax1.set_title(f'Insolation series with hreshold: {428 + (frame) * N } W/m²', fontsize=16)
    return lines

# generate animation
ani = animation.FuncAnimation(
    fig, animate,
    init_func=init,
    frames=num_frames,
    interval= 200 * N,
    blit=True
)

output_file = 'Output_insolation_rank_couplet_coherence_phase.gif' 
ani.save(output_file, writer='pillow', dpi=150)
print(f'{output_file} is saved')
#plt.tight_layout()
plt.show()