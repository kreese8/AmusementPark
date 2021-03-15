"""
This is merely a quick and dirty example. It doesn't provide any support for
customisation, extending functionality, or more extensive data collection.
"""
import constants as const
from classes import *
import plots as plt
from typing import List, Tuple
import random

def generate_groups(time: int) -> List[Group]:
    """Generates the groups to be added to the line.
    Groups are tuples of ints in the form (size, arrival_time).
    """
    return [Group(random.randint(1,7), time) for _ in range(random.randint(1,2))]

def generate_groups_fancy(time: int, dist: List[int], line_length: int, busyness: float, line_target: int)-> List[Group]:
    """
    Generates the groups to be added to the line.
    Groups are tuples of ints in the form (size, arrival_time).
    This one is more fancy because it takes the distribution and busyness into consideration.
    line_length is the current line length, and the line_target is the length,
    before visitors start to get discouraged by line_length.
    dist is a list of weights, for each group size. For example: [7,6,5,4,3,2,1]
    """
    
    if line_length < line_target:
        groups = random.randint(1,4)
    else:
        if random.uniform(0,1) < busyness:
            groups = random.randint(0,1)
        else:
            groups = 0
    sizes = random.choices(list(range(1, const.MAX_GROUP_SIZE + 1)), dist, k = groups)
    return [Group(n, time) for n in sizes]
        
    
    # Parameters of group size distribution 
    # How busy it is in the park
    # Length of the line 

def step_time(line: List[Group], time: int) -> (List[Group], List[Group]):
    """Generates new groups and loads a single boat. Returns line, departed_groups
    Looks forward MAX_LINE_SKIP groups to load the boat. (so skipping is possible)
    """

    # People arrive
    # line.extend(generate_groups(time))
    
    line.extend(generate_groups_fancy(time, [1,1,1,1,1,1,1], 5, 1, 8)) # example parameters
    
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
        line[0:const.MAX_LINE_SKIP]
        options = [index for index, option in enumerate(line[0:const.MAX_LINE_SKIP]) if option.size <= remaining]
        if len(options) > 0:
            departed.append(line.pop(options[0]))
            remaining -= departed[-1].size
        else:
            break

    return line, departed

def perf_timesteps(n: int) -> RunResult:
    """Simulate a day of n timesteps. 
    Returns two DataFrames, one containing info about the timesteps, 
    the other containing info about groups
    """
    # Initialize variables to keep track of data
    line = []
    results = RunResult()
    
    for time in range(n):
        line, departed_groups = step_time(line, time) # Step forward 1 timestep
        
        # Add data to df_timesteps. The time, line length and boat occupancy are tracked
        results.add_timestep(time, line, departed_groups)
        
        # Add data to df_groups. One row per group, keeping track of sizes and times.
        results.add_groups(time, departed_groups)
        
        print(line)

    return results


if __name__ == "__main__":
    #print(generate_groups_fancy(28, [1,1,1,1,1,1,1], 5, 1, 8))
    result = perf_timesteps(200)
    plt.create_plots_single(result)
    # print(step_time([(2, 28), (1, 28), (6, 28), (6, 28), (6, 28), (6, 28), (2, 28), (1, 28), (6, 28)], 28))

# %%
