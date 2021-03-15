import constants as const
import pandas as pd
from typing import List

class Group:
    
    def __init__(self, size: int, arrival_time: int):
        self.size = size
        self.arrival_time = arrival_time
    
    size: int
    arrival_time: int

    def __repr__(self) -> str:  # called by repr(...)
        return "Group({}, {})".format(self.size, self.arrival_time)

    def __str__(self) -> str:  # (optional) called by str(...)
        return "Group({}, {})".format(self.size, self.arrival_time)
    
    
class RunResult:
    
    def __init__(self):
        self.timesteps = pd.DataFrame(columns = const.COLS_TIMESTEPS, dtype='float')
        self.timesteps.set_index('time')
        self.groups = pd.DataFrame(columns = const.COLS_GROUPS, dtype='float')
    
    timesteps: pd.DataFrame
    groups: pd.DataFrame
    
    def add_timestep(self, time: int, line: List[Group], departed_groups: List[Group]):
        timestep_row = {'time': time, 
                   'line length': len(line), 
                   'boat occupancy': sum(t.size for t in departed_groups)
                   }
        self.timesteps = self.timesteps.append(timestep_row, ignore_index=True)
        
    def add_groups(self, time: int, departed_groups: List[Group]):
        group_rows = []
        for group in departed_groups:
            group_rows.append({'size': group.size,
                               'arrival time': group.arrival_time,
                               'departure time': time,
                               'wait time': time - group.arrival_time
                })
        self.groups = self.groups.append(group_rows, ignore_index=True)

