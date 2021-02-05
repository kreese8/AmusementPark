"""
This is merely a quick and dirty example. It doesn't provide any support for
customisation, extending functionality, or more extensive data collection.
"""

from typing import List, Tuple
import random

def load_boat(line: List[int], solo_groups: int) -> Tuple[List[int], int]:
    """
    Tries to load a single boat with the groups in the line and the solo_groups.
    Returns the new line, and the new amount of groups.
    """
    remaining = 8
    while len(line) > 0 and remaining >= line[0]:
        remaining -= line.pop(0)
    return line, 0

def generate_groups(time: int) -> List[int]:
    """
    Generates the groups to be added to the line.
    """
    return [random.randint(1,7) for _ in range(random.randint(1,2))]

def step_time(line, solo_groups, time) -> Tuple[List[int], int]:
    """
    Generates new groups and loads a single boat.
    """
    line.extend(generate_groups(time))
    line, solo_groups = load_boat(line, solo_groups)
    return line, solo_groups

def perf_timesteps(n: int)->None:
    line = []
    solo_groups = 0
    for time in range(n):
        line, solo_groups = step_time(line, solo_groups, time)
        print(line)

if __name__ == "__main__":
    perf_timesteps(100)
