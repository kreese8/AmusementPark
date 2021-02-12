from typing import List
import random

def generate_groups(time: int) -> List[int]:
    """
    Generates the groups to be added to the line.
    """
    return [random.randint(1,7) for _ in range(random.randint(1,2))]