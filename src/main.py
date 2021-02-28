"""
This is merely a quick and dirty example. It doesn't provide any support for
customisation, extending functionality, or more extensive data collection.
"""
from typing import List
import groupGenerators as gen
import random
    

def generate_groups(time: int) -> List[int]:
    """Generates the groups to be added to the line.
    """
    return [random.randint(1,7) for _ in range(random.randint(1,2))]

def step_time(line: List[int], time: int) -> List[int]:
    """Generates new groups and loads a single boat.
    """
    # People arrive
    line.extend(gen.generate_groups(time))
    # Load the boat
    remaining = 8
    while len(line) > 0 and remaining >= line[0]:
        remaining -= line.pop(0)
    return line

def perf_timesteps(n: int)->None:
    """Step forward in time n steps
    """
    line = []
    for time in range(n):
        line = step_time(line, time)
        print(line)

if __name__ == "__main__":
    perf_timesteps(100)
