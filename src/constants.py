
# In minutes
BOAT_LOAD_TIME = 0.25
DAY_LENGTH = 12*60
BOAT_CAPACITY = 8

COLS_TIMESTEPS = ['time', 'line length', 'boat occupancy']
COLS_GROUPS = ['size', 'arrival time', 'departure time', 'wait time']

def timesteps_in_day() -> int:
    return DAY_LENGTH // BOAT_LOAD_TIME