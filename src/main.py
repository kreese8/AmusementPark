"""
This is merely a quick and dirty example. It doesn't provide any support for
customisation, extending functionality, or more extensive data collection.
test2
"""

from typing import List
import groupGenerators as gen

def load_boat(line: List[int]) -> List[int]:
    """
    Tries to load a single boat with the groups in the line and the solo_groups.
    Returns the new line, and the new amount of groups.
    """
    remaining = 8
    while len(line) > 0 and remaining >= line[0]:
        remaining -= line.pop(0)
    return line


def step_time(line: List[int], time: int) -> List[int]:
    """
    Generates new groups and loads a single boat.
    """
    line.extend(gen.generate_groups(time))
    line = load_boat(line)
    return line

def perf_timesteps(n: int)->None:
    line = []
    for time in range(n):
        line = step_time(line, time)
        print(line)

if __name__ == "__main__":
    perf_timesteps(100)
