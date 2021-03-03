"""
This is merely a quick and dirty example. It doesn't provide any support for
customisation, extending functionality, or more extensive data collection.
"""
import constants as const
from typing import List, Tuple
import random


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

def generate_groups_fancy(time: int, dist: List[int], line_length: int, busyness: float, line_target: int)-> List[Tuple[int,int]]:
    """
    Generates the groups to be added to the line.
    Groups are tuples of ints in the form (size, arrival_time).
    This one is more fancy because it takes the distribution and busyness into consideration.
    line_length is the current line length, and the line_target is the length,
    before visitors start to get discouraged by line_length.
    dist is a list of weights, for each group size.
    """
    
    if line_length < line_target:
        groups = random.randint(1,4)
    else:
        if random.uniform(0,1) < busyness:
            groups = random.randint(0,1)
        else:
            groups = 0
    sizes = random.choices(list(range(1, const.MAX_GROUP_SIZE + 1)), dist, k = groups)
    return [(n, time) for n in sizes]
        
    
    # Parameters of group size distribution 
    # How busy it is in the park
    # Length of the line 

def step_time(line: List[Tuple[int, int]], time: int) -> (List[int], List[int]):
    """Generates new groups and loads a single boat. Returns line, departed_groups
    Looks forward MAX_LINE_SKIP groups to load the boat. (so skipping is possible)
    """

    # People arrive
    line.extend(generate_groups(time))
    
    #line.extend(generate_groups_fancy(time, [1,1,1,1,1,1,1], 5, 1, 8)) # example parameters
    
    # This is sufficient for first come first serve
    # Load the boat and keep track of departed groups
    # remaining = const.BOAT_CAPACITY
    # departed = []
    # while len(line) > 0 and remaining >= line[0][0]:        
    #    departed.append(line.pop(0))
    #    remaining -= departed[-1][0]
    # return line, departed
    
    remaining = const.BOAT_CAPACITY
    departed = []
    while len(line) > 0:
        options = [index for index, option in enumerate(line[0:const.MAX_LINE_SKIP]) if option[0] <= remaining]
        if len(options) > 0:
            departed.append(line.pop(options[0]))
            remaining -= departed[-1][0]
        else:
            break

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
    #print(generate_groups_fancy(28, [1,1,1,1,1,1,1], 5, 1, 8))
    #df_timesteps, df_groups = perf_timesteps(2000)
    print(step_time([(2, 28), (1, 28), (6, 28), (2, 28), (1, 28), (6, 28), (2, 28), (1, 28), (6, 28)], 0))
