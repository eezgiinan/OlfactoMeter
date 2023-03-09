import enum

# Define the different modes of operation and the corresponding pin values
# 0 ON / 1 OFF
CLOSE = 1
OPEN = 0

class Modes(enum.Enum):
    """
    Enumeration of the different modes that the system can be IN
    """
    Resting = (CLOSE, CLOSE, CLOSE, CLOSE)  # No valves activated
    Purging = (OPEN, OPEN, CLOSE, CLOSE)  # Valve S1 and S2 activated to purge the system
    Odor_1 = (OPEN, CLOSE, OPEN, CLOSE)  # Valve SB and S1 activated to deliver odor 1
    Odor_2 = (OPEN, CLOSE, CLOSE, OPEN)  # Valve SB and S2 activated to deliver odor 2
    # The XLSX file needs to have the same names as here, you call the function with user input
