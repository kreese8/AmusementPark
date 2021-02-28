"""
This is merely a quick and dirty example. It doesn't provide any support for
customisation, extending functionality, or more extensive data collection.
"""
from typing import List, Tuple
import random
import constants as const

# Copy paste from DAE exercises: import DAE libraries
import numpy as np  # import auxiliary library, typical idiom
import pandas as pd  # import the Pandas library, typical idiom

# next command ensures that plots appear inside the notebook
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns  # also improves the look of plots
sns.set()
plt.rcParams['figure.figsize'] = 10, 5  # default hor./vert. size of plots, in inches
plt.rcParams['lines.markeredgewidth'] = 1  # to fix issue with seaborn box plots; needed after import seaborn
    

def generate_groups(time: int) -> List[Tuple[int, int]]:
    """Generates the groups to be added to the line.
    Groups are tuples of ints in the form (size, arrival_time).
    """
    return [(random.randint(1,7), time) for _ in range(random.randint(1,2))]

def step_time(line: List[Tuple[int, int]], time: int) -> (List[int], List[int]):
    """Generates new groups and loads a single boat. Returns line, departed_groups
    """
    # People arrive
    line.extend(generate_groups(time))
    # Load the boat and keep track of departed groups
    remaining = const.BOAT_CAPACITY
    departed = []
    while len(line) > 0 and remaining >= line[0][0]:
        departed.append(line.pop(0))
        remaining -= departed[-1][0]
    return line, departed

def perf_timesteps(n: int) -> (pd.DataFrame, pd.DataFrame):
    """Simulate a day of n timesteps. 
    Returns two DataFrames, one containing info about the timesteps, 
    the other containing info about groups
    """
    # Initialize variables to keep track of data
    line = []
    df_timesteps = pd.DataFrame(columns = const.COLS_TIMESTEPS, dtype='float')
    df_timesteps.set_index('time')
    df_groups = pd.DataFrame(columns = const.COLS_GROUPS, dtype='float')
    
    for time in range(n):
        line, departed_groups = step_time(line, time) # Step forward 1 timestep
        
        # Add data to df_timesteps. The time, line length and boat occupancy are tracked
        timestep_row = {'time': time, 
                   'line length': len(line), 
                   'boat occupancy': sum(t[0] for t in departed_groups)
                   }
        df_timesteps = df_timesteps.append(timestep_row, ignore_index=True)
        
        # Add data to df_groups. One row per group, keeping track of sizes and times.
        group_rows = []
        for group in departed_groups:
            group_rows.append({'size': group[0],
                               'arrival time': group[1],
                               'departure time': time,
                               'wait time': time - group[1]
                })
        df_groups = df_groups.append(group_rows, ignore_index=True)
        
        #print(line)
    
    # TODO: Extract the plotting to a separate file
    # Make some pretty plots
    fig, ax = plt.subplots(nrows=2)
    df_timesteps['line length'].plot(ax=ax[0]) 
    sns.violinplot(data=df_groups, x='size', y='wait time', ax=ax[1])
    return df_timesteps, df_groups


if __name__ == "__main__":
    df_timesteps, df_groups = perf_timesteps(2000)
